import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'chinese_texts.settings'
import django
django.setup()
from texts.models import Author, Text
from django.db.utils import DataError


print "Making slugs for texts:"
for text in Text.objects.all():
    try:
        text.slug = None
        text.save_no_parsing()
    except DataError, e:
        pass
for text in Text.objects.all():
    try:
        text.save_override_slug()
        print "   ", text.title_english, ":", text.slug
    except DataError, e:
        pass

print
print "Making slugs for authors:"
for author in Author.objects.all():
    try:
        author.slug = None
        author.save()
    except DataError, e:
        pass
for author in Author.objects.all():
    try:
        author.save_override_slug()
        print "   ", author.name_pinyin, ":", author.slug
    except DataError, e:
        pass
