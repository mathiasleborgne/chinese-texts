import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'chinese_texts.settings'
import django
django.setup()
from texts.models import Author, Text


print "Making slugs for texts:"
for text in Text.objects.all():
    text.slug = None
    text.save_no_parsing()
for text in Text.objects.all():
    text.save_override_slug()
    print "   ", text.title_english, ":", text.slug

print
print "Making slugs for authors:"
for author in Author.objects.all():
    author.slug = None
    author.save()
for author in Author.objects.all():
    author.save_override_slug()
    print "   ", author.name_pinyin, ":", author.slug
