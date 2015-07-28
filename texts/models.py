#-*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
import operator


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
            "author__name_pinyin",
            "author__name_chinese",
        ]
        objects_q = [Q((search_field + "__contains", keyword))
                     for search_field in search_fields]
        return Text.objects.filter(reduce(operator.or_, objects_q))

    @staticmethod
    def count_texts():
        return len(Text.objects.all())


class CharData(object):
    """Metadata for chinese character
       We don't do the parsing here to avoid too heavy dependency
       between this storage class and the parsing system
    """

    special_characters = [
        "。", "，", "?", "；", "？",
    ]
    line_break = "\n"

    def __init__(self, character, translation, pinyin):
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
            translation = None
            pinyin = None
        else:
            translation = item_json[1]
            pinyin = item_json[2]
        return cls(character, translation, pinyin)

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
            return [self.character, self.translation, self.pinyin]



class Author(models.Model):
    name_chinese = models.CharField(max_length=42)
    name_pinyin = models.CharField(max_length=42)
    year_birth = models.CharField(null=True, max_length=100)
    year_death = models.CharField(null=True, max_length=100)
    biography = models.TextField(null=True)

    def __str__(self):
        # todo replace by name_chinese
        return self.name_pinyin


class Profile(models.Model):
    user = models.OneToOneField(User)
    user_image = models.ImageField(null=True, blank=True,
                                   upload_to="user_images/")
    chinese_name = models.CharField(max_length=42)

    def __str__(self):
        return "Profile for {0}".format(self.user.username)
