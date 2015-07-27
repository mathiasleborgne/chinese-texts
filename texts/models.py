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


class Author(models.Model):
    name_chinese = models.CharField(max_length=42)
    name_pinyin = models.CharField(max_length=42)

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
