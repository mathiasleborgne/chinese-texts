#-*- coding: utf-8 -*-

# Manually execute pinyin parsing
# NB: we need to split the files (pinyin lib/manual) to avoid circular
#     dependency with Models

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'chinese_texts.settings'
import django
django.setup()

from texts.models import CharData, Text
from texts.scraping.pinyin import MetadataParser, get_pinyin_parser


def get_all_texts(args):
    if args.select_text is not None:
        return Text.objects.filter(title_english=args.select_text)
    all_texts = Text.objects.all()
    if not args.reset_db:
        for text in all_texts:
            if text.chars_data is not None:
                print "Not processing text:", text.title_english
        all_texts = [text for text in all_texts if text.chars_data is None]
    return all_texts if args.many_items else all_texts[:2]


def get_texts_with_metadata(args):
    all_texts =  [text for text in Text.objects.all()
                  if text.chars_data is not None
                  and (text.content_pinyin is None or args.reset_db)]
    return all_texts if args.many_items else all_texts[:2]


if __name__ == "__main__":
    args = get_pinyin_parser().parse_args()
    if args.content_pinyin:
        texts = get_texts_with_metadata(args)
        print "Filling pinyin for", len(texts), "texts"
        for text in texts:
            MetadataParser(text, args).fill_content_pinyin()
    else:
        texts = get_all_texts(args)
        print "Getting metadata for", len(texts), "texts"
        for text in texts:
            MetadataParser(text, args).make_metadata()
