#-*- coding: utf-8 -*-

import operator
import json
import itertools
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from texts.text_processing import check_process_text
from texts.char_data import CharData, get_unicode


class Text(models.Model):
    title_english = models.CharField(max_length=100)
    title_chinese = models.CharField(max_length=100)
    title_pinyin = models.CharField(max_length=100, null=True)
    author = models.ForeignKey('Author')
    content_english = models.TextField(null=True)
    content_chinese = models.TextField(null=True)
    content_pinyin = models.TextField(null=True)
    date_release = models.DateTimeField(auto_now_add=True, auto_now=False,
                                        verbose_name="Release Date")
    date_writing = models.DateTimeField(auto_now_add=False, auto_now=False,
                                        null=True,
                                        verbose_name="Writing Date")
    chars_data = models.TextField(null=True) # JSON-serialized (text) version of your list
    # see explanation for JSON serialization here:
    # http://stackoverflow.com/questions/1110153/what-is-the-most-efficent-way-to-store-a-list-in-the-django-models
    view_count = models.PositiveIntegerField(default=0)
    slug = models.SlugField(null=True)


    class Meta:
        ordering = ['chars_data', 'content_pinyin']

    def __str__(self):
        return self.title_english

    @staticmethod
    def search_texts(keyword):
        search_fields = [
            "content_english",
            "content_chinese",
            "title_english",
            "title_chinese",
            "author__name_pinyin",
            "author__name_chinese",
        ]
        objects_q = [Q((search_field + "__contains", keyword))
                     for search_field in search_fields]
        return Text.objects.filter(reduce(operator.or_, objects_q))

    @staticmethod
    def count_texts():
        return len(Text.objects.all())

    @staticmethod
    def count_all_views():
        views_sum = 0
        for text in Text.objects.all():
            views_sum += text.view_count
        return views_sum


    def get_lines(self):
        lines_chinese = split_lines(self.content_chinese)
        if self.content_pinyin is None:
            lines_pinyin = [None for _ in lines_chinese]
        else:
            lines_pinyin = split_lines(self.content_pinyin)
        lines_english = split_lines(self.content_english)

        return (lines_chinese, lines_english, lines_pinyin)


    def check_lines(self):
        (lines_chinese, lines_english, lines_pinyin) = self.get_lines()
        return (len(lines_chinese) == len(lines_pinyin) == \
                len(lines_english))

    def content_lines(self):
        chars_data_decoded = self.get_all_chars_data()
        (lines_chinese, lines_english, lines_pinyin) = self.get_lines()

        def print_lines(lines):
            """for debug"""
            for index_line, line in enumerate(lines):
                print index_line, "-", line

        if not self.check_lines():
            return None
        if chars_data_decoded is not None:
            lines_char_data = split_lines_chardata(chars_data_decoded)
            lines_char_data = [line for line in lines_char_data if line != []]
            if len(lines_english) != len(lines_char_data):
                return None
        else:
            lines_char_data = None
        lines = [(lines_chinese[index], lines_pinyin[index],
                  lines_english[index],
                  lines_char_data[index] if lines_char_data is not None else None)
                 for index in range(len(lines_chinese))]
        return lines

    def get_all_chars_data(self):
        chars_data_json = self.chars_data
        json_decoder = json.decoder.JSONDecoder()
        if chars_data_json is not None:
            return [CharData.from_json(char_data_raw) for char_data_raw
                    in json_decoder.decode(chars_data_json)]
        else:
            return None

    def make_json(self, get_char_data, all_characters=True):
        """ get_char_data must be a function: char -> CharData
        """

        all_characters_str = self.content_chinese
        if all_characters:
            all_characters = list(all_characters_str)
        else:
            all_characters = list(all_characters_str)[:2]

        char_objects = [get_char_data(char) for char in all_characters]
        chars_data = [char_object.get_JSONable_item()
                      for char_object in char_objects
                      if char_object is not None]
        self.chars_data = json.dumps(chars_data)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original_text = Text.objects.get(pk=self.pk)
            check_process_text(self, original_text)
            self.save_no_parsing()
        else:
            super(Text, self).save(*args, **kwargs)

    def make_slug(self):
        self.slug = make_slug(self, self.title_english, Text)

    def save_no_parsing(self):
        """ every generic save will run the characters parsing, so we can
            use this function to avoid it
        """
        if not self.id:
            self.make_slug()
        super(Text, self).save()

    def save_override_slug(self, *args, **kwargs):
        self.slug = None
        self.make_slug()
        self.save_no_parsing(*args, **kwargs)


class TextLine(object):
    """docstring for TextLine"""
    def __init__(self, lines_chinese, lines_pinyin, lines_english):
        super(TextLine, self).__init__()
        self.arg = arg


def split_lines(content):
    splitted_lines = content.split('\n')
    return [line for line in splitted_lines if line != ""]


def split_lines_chardata(chars_data):
    # [char_1, char_linebreak, char_2] -> [[char_1],[char_2]]
    index_linebreak = None
    for index, char_data in enumerate(chars_data):
        if char_data.is_line_break:
            index_linebreak = index
            break
    if index_linebreak is None:
        return [chars_data]
    else:
        head = chars_data[:index_linebreak]
        try:
            queue = chars_data[index_linebreak + 1:]
            return [head] + split_lines_chardata(queue)
        except IndexError, error:
            return [head]


class Author(models.Model):
    name_chinese = models.CharField(max_length=42)
    name_pinyin = models.CharField(max_length=42)
    year_birth = models.CharField(null=True, max_length=100)
    year_death = models.CharField(null=True, max_length=100)
    biography = models.TextField(null=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        # todo replace by name_chinese
        return self.name_pinyin

    def count_texts(self):
        return len(Text.objects.filter(author__name_chinese=self.name_chinese))

    def make_slug(self):
        self.slug = make_slug(self, self.name_pinyin, Author)

    def save(self, *args, **kwargs):
        if not self.id:
            self.make_slug()
        super(Author, self).save(*args, **kwargs)

    def save_override_slug(self, *args, **kwargs):
        self.slug = None
        self.make_slug()
        self.save(*args, **kwargs)


def make_slug(instance, data_slugify, class_data):
    max_length = class_data._meta.get_field('slug').max_length
    slug_unnumbered = slugify(data_slugify)
    slug_numbered = slug_unnumbered
    for number_slug in itertools.count(1):
        if not class_data.objects.filter(slug=slug_numbered).exists():
            break
        index_truncate = max_length - len(str(number_slug)) - 1
        slug_numbered = "%s-%d" % (slug_unnumbered[:index_truncate],
                                   number_slug)
    return slug_numbered


class Profile(models.Model):
    user = models.OneToOneField(User)
    user_image = models.ImageField(null=True, blank=True,
                                   upload_to="user_images/")
    chinese_name = models.CharField(max_length=42)

    def __str__(self):
        return "Profile for {0}".format(self.user.username)
