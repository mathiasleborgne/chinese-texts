from django.db import models


class Text(models.Model):
    title_french = models.CharField(max_length=100)
    title_chinese = models.CharField(max_length=100)
    auteur = models.ForeignKey('Author')
    content_french = models.TextField(null=True)
    content_chinese = models.TextField(null=True)
    date_release = models.DateTimeField(auto_now_add=True, auto_now=False,
                                        verbose_name="Release Date")
    date_writing = models.DateTimeField(auto_now_add=False, auto_now=False,
                                        null=True,
                                        verbose_name="Writing Date")

    def __str__(self):
        return self.title_french


class Author(models.Model):
    name_chinese = models.CharField(max_length=42)
    name_pinyin = models.CharField(max_length=42)
    year_birth = models.IntegerField(null=True)
    year_death = models.IntegerField(null=True)

    def __str__(self):
        # todo replace by name_chinese
        return self.name_pinyin
