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
    parser.add_argument("--content_pinyin",
                        action="store_true",
                        help="Only fill content_pinyin from texts with "
                             "metadata")
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


def get_texts_with_metadata(args):
    all_texts =  [text for text in Text.objects.all()
                  if text.chars_data is not None
                  and (text.content_pinyin is None or args.reset_db)]
    return all_texts if args.many_items else all_texts[:2]


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
        get_char_data_no_arg = (lambda char: get_char_data(char, args))
        text.chars_data = CharData.make_json(text, get_char_data_no_arg,
                                             args.all_characters)
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


def fill_content_pinyin(args):
    texts = get_texts_with_metadata(args)
    print "Filling pinyin for", len(texts), "texts"
    for text in texts:
        chars_data = CharData.get_all_chars_data(text)

        def get_pinyin_content(char_data):
            if char_data.pinyin is not None:
                return char_data.pinyin
            else:
                return char_data.character

        content_pinyin = " ".join([get_pinyin_content(char_data)
                                   for char_data in chars_data])
        text.content_pinyin = content_pinyin
        print "got content_pinyin:", content_pinyin[:50], "..."
        if args.fill_db:
            text.save()



if __name__ == "__main__":
    args = get_pinyin_parser().parse_args()
    if args.content_pinyin:
        fill_content_pinyin(args)
    else:
        try:
            all_texts = get_all_texts(args)
            print "Parsing", len(all_texts), "texts"
            for text in all_texts:
                make_text_metadata(text, args)
        except KeyboardInterrupt, error:
            print "Interrupting"
        fill_content_pinyin(args)


