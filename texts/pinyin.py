#-*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'chinese_texts.settings'
from texts.models import CharData, Text
import django
django.setup()

import urllib2
from bs4 import BeautifulSoup
from scraper import get_parser, get_html
import json

url_root = "http://www.unicode.org/cgi-bin/GetUnihanData.pl?codepoint="


def get_pinyin_parser():
    parser = get_parser()
    parser.add_argument("--all_characters",
                        action="store_true",
                        help="Get all all characters from the texts")
    parser.add_argument("--reset_db",
                        action="store_true",
                        help="Re-fetch pinyin for all texts in the db, instead"
                             " of only fetching the texts without pinyin")
    return parser


def get_soup(url):
    return BeautifulSoup(get_html(url), 'html.parser')


def get_all_texts(many_items, reset_db):
    all_texts = Text.objects.all()
    if not reset_db:
        for text in all_texts:
            if text.chars_data is not None:
                print "Not processing text:", text.title_english
        all_texts = [text for text in all_texts if text.chars_data is None]
    return all_texts if many_items else all_texts[:2]


def get_characters(text, all_characters):
    all_characters_str = text.content_chinese
    if all_characters:
        return list(all_characters_str)
    else:
        return list(all_characters_str)[:2]


def get_char_data(char):
    if char == "\n":
        print "Linebreak"
        return CharData.from_line_break()
    char_encoded = char.encode('utf-8')
    url_full = url_root + char_encoded
    soup = get_soup(url_full)

    def get_chinese_item(selector):
        hyperlinks = soup.select(selector)
        return hyperlinks[0].parent.parent.select("td code")[0]\
            .decode_contents()

    pinyin = get_chinese_item(
        'a[href="http://www.unicode.org/reports/tr38/index.html#kMandarin"]')\
        .encode('utf-8')
    translation = get_chinese_item(
        'a[href="http://www.unicode.org/reports/tr38/index.html#kDefinition"]')
    print "   pinyin:", pinyin, "/ translation:", translation
    return CharData(char_encoded, pinyin, translation)


def make_text_metadata(text, fill_db, all_characters):
    try:
        print "Getting data for text:", text.title_english
        chars_data = [get_char_data(char).get_JSONable_item()
                      for char in get_characters(text, all_characters)]
        text.chars_data = json.dumps(chars_data)
        print "JSON encoding for text:", text.chars_data
        print
        if fill_db:
            text.save()
    except KeyboardInterrupt, error:
        print
        print "Erasing data for text:", text.title_english
        text.chars_data = None
        raise error
    except IndexError, error:
        print "Got an unexpected character in text:", text.title_english, \
            "; parsing on!"


if __name__ == "__main__":
    args = get_pinyin_parser().parse_args()
    try:
        for text in get_all_texts(args.many_items, args.reset_db):
            make_text_metadata(text, args.fill_db, args.all_characters)
    except KeyboardInterrupt, error:
        print "Interrupting"
