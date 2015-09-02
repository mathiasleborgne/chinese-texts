#-*- coding: utf-8 -*-
import argparse
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'chinese_texts.settings'
from texts.models import Text, Author
import django
django.setup()


parser = argparse.ArgumentParser()
parser.add_argument("--remove",
                    action="store_true",
                    help="Remove bad texts")
args = parser.parse_args()

for text in Text.objects.all():
    if not text.check_lines():
        print "Bad line check for text:", text.title_english, "/", \
            text.author.name_pinyin
        if args.remove:
            print "removing test from the db!"
            text.delete()