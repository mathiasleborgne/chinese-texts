#-*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
import operator
import json


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

    def content_lines(self):
        lines_chinese = split_lines(self.content_chinese)
        chars_data_decoded = CharData.get_all_chars_data(self)
        if self.content_pinyin is None:
            lines_pinyin = [None for _ in lines_chinese]
        else:
            lines_pinyin = split_lines(self.content_pinyin)
        lines_english = split_lines(self.content_english)
        if not (len(lines_chinese) == len(lines_pinyin) == \
                len(lines_english)):
            return None
        if chars_data_decoded is not None:
            lines_char_data = split_lines_chardata(chars_data_decoded)
            if len(lines_english) != len(lines_char_data):
                return None
        else:
            lines_char_data = None
        lines = [(lines_chinese[index], lines_pinyin[index],
                  lines_english[index],
                  lines_char_data[index] if lines_char_data is not None else None)
                 for index in range(len(lines_chinese))]
        return lines

class TextLine(object):
    """docstring for TextLine"""
    def __init__(self, lines_chinese, lines_pinyin, lines_english):
        super(TextLine, self).__init__()
        self.arg = arg



def split_lines(content):
    return content.split('\n')

def split_lines_chardata(chars_data):
    index_linebreak = None
    for index, char_data in enumerate(chars_data):
        if char_data.is_line_break:
            index_linebreak = index
            break
    if index_linebreak is None:
        return [chars_data]
    else:
        head = chars_data[:index_linebreak - 1]
        try:
            queue = chars_data[index_linebreak + 1:]
            return [head] + split_lines_chardata(queue)
        except IndexError, error:
            return [head]



class CharData(object):
    """Metadata for chinese character
    """

    special_characters = [
        "。", "，", "?", "；", "？", "！",
    ]
    line_break = "\n"

    def __init__(self, character, pinyin, translation):
        super(CharData, self).__init__()
        self.character = character
        self.is_line_break = character == self.line_break
        self.translation = translation
        self.pinyin = pinyin

    @classmethod
    def from_json(cls, item_json):
        "Initialize CharData from a json serialization"
        character = item_json[0]
        if len(item_json) == 1:
            pinyin = None
            translation = None
        else:
            pinyin = item_json[1]
            translation = item_json[2]
        return cls(character, pinyin, translation)

    @classmethod
    def from_line_break(cls):
        return cls("\n", None, None)

    @classmethod
    def from_special_character(cls, character):
        return cls(character, None, None)

    def get_JSONable_item(self):
        if self.is_line_break:
            return [self.character]
        else:
            return [self.character, self.pinyin, self.translation]


    @staticmethod
    def get_all_chars_data(text):
        chars_data_json = text.chars_data
        json_decoder = json.decoder.JSONDecoder()
        if chars_data_json is not None:
            return [CharData.from_json(char_data_raw) for char_data_raw
                    in json_decoder.decode(chars_data_json)]
        else:
            return None

    @staticmethod
    def make_json(text, get_char_data, all_characters=True):
        """ get_char_data must be a function: char -> CharData
        """

        def get_characters(text):
            all_characters_str = text.content_chinese
            if all_characters:
                return list(all_characters_str)
            else:
                return list(all_characters_str)[:2]

        chars_data = [get_char_data(char).get_JSONable_item()
                      for char in get_characters(text)]
        return json.dumps(chars_data)


class Author(models.Model):
    name_chinese = models.CharField(max_length=42)
    name_pinyin = models.CharField(max_length=42)
    year_birth = models.CharField(null=True, max_length=100)
    year_death = models.CharField(null=True, max_length=100)
    biography = models.TextField(null=True)

    def __str__(self):
        # todo replace by name_chinese
        return self.name_pinyin

    def count_texts(self):
        return len(Text.objects.filter(author__name_chinese=self.name_chinese))


class Profile(models.Model):
    user = models.OneToOneField(User)
    user_image = models.ImageField(null=True, blank=True,
                                   upload_to="user_images/")
    chinese_name = models.CharField(max_length=42)

    def __str__(self):
        return "Profile for {0}".format(self.user.username)
