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
    parser.add_argument("--select_text", default=None,
                        help="Select an text")
    parser.add_argument("--verbose",
                        action="store_true",
                        help="A lot of logs")
    return parser


def get_soup(url):
    return BeautifulSoup(get_html(url), 'html.parser')


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


def get_characters(text, all_characters):
    all_characters_str = text.content_chinese
    if all_characters:
        return list(all_characters_str)
    else:
        return list(all_characters_str)[:2]


def get_char_data(char, args):
    char_encoded = char.encode('utf-8')
    if char_encoded == CharData.line_break:
        if args.verbose:
            print "Linebreak"
        return CharData.from_line_break()
    elif char_encoded in CharData.special_characters:
        if args.verbose:
            print "special_character:", char_encoded
        return CharData.from_special_character(char_encoded)
    try:
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
        if args.verbose:
            print "   pinyin:", pinyin, "/ translation:", translation
        return CharData(char_encoded, pinyin, translation)
    except IndexError, error:
        print "Unexpected character:", char
        raise error


def make_text_metadata(text, args):
    try:
        print "Getting data for text:", text.title_english
        chars_data = [get_char_data(char, args).get_JSONable_item()
                      for char in get_characters(text, args.all_characters)]
        text.chars_data = json.dumps(chars_data)
        if args.verbose:
            print "JSON encoding for text:", text.chars_data
            print
        if args.fill_db:
            text.save()
    except KeyboardInterrupt, error:
        print
        print "Erasing data for text:", text.title_english
        text.chars_data = None
        raise error
    except IndexError, error:
        print "Got an unexpected character in text:", text.title_english, \
            "; parsing on!"
        print "     got:", error


if __name__ == "__main__":
    args = get_pinyin_parser().parse_args()
    try:
        all_texts = get_all_texts(args)
        print "Parsing", len(all_texts), "texts"
        for text in all_texts:
            make_text_metadata(text, args)
    except KeyboardInterrupt, error:
        print "Interrupting"
