import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'chinese_texts.settings'
import django
django.setup()
from texts.models import CharData, Text


def print_ratio(texts_list, name_test):
    ratio = float(len(texts_list)) / float(len(Text.objects.all()))
    print name_test, ":", ratio * 100., "missing"

texts_no_char_data = Text.objects.filter(chars_data=None)
print_ratio(texts_no_char_data, "CharData")

texts_bad_check_line = [text for text in Text.objects.all() if not text.check_lines()]
print_ratio(texts_bad_check_line, "check_lines")
for text in texts_bad_check_line:
    print "   Bad check_lines for:", text.title_english
