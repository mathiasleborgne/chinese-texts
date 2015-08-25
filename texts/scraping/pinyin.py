#-*- coding: utf-8 -*-

from texts.scraping.scraping_tools import get_parser, get_soup
from texts.scraping.characters_dictionary import CharactersDictionary
import json
from texts.char_data import CharData

url_root = "http://www.unicode.org/cgi-bin/GetUnihanData.pl?codepoint="
url_sample = "http://www.unicode.org/cgi-bin/GetUnihanData.pl?codepoint=国"


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


class FakeArgs(object):
    """Argparse faker"""

    def __init__(self, text):
        super(FakeArgs, self).__init__()
        self.many_items = True
        self.fill_db = False
        self.reset_db = True
        self.all_characters = True
        self.select_text = text.title_english
        self.verbose = True
        self.content_pinyin = False


def get_unihan_selector(keyword):
    return 'a[href="http://www.unicode.org/reports/tr38/index.html#{}"]'\
        .format(keyword).encode('utf-8')


def get_chinese_item(soup, keyword):
    hyperlinks = soup.select(get_unihan_selector(keyword))
    return hyperlinks[0].parent.parent.select("td code")[0]\
        .decode_contents()


def get_character_item(soup, keyword):
    hyperlinks = soup.select(get_unihan_selector(keyword))
    try:
        char_id = hyperlinks[0].parent.parent.select("td code")[0].a.\
            decode_contents()
        return char_id.split(" ")[1].encode('utf-8')
    except IndexError:
        return None


class MetadataParser(object):
    """ Metadata Parser: pinyin and traditional/simplified character
    """

    def __init__(self, text, characters_dictionary = None, args=None):
        super(MetadataParser, self).__init__()
        self.text = text
        self.args = args
        if self.args is None:
            self.args = FakeArgs(text)
        self.characters_dictionary = characters_dictionary
        if self.characters_dictionary is None:
            self.characters_dictionary = CharactersDictionary()

    def get_unknown_characters_number(self):
        return self.characters_dictionary.\
            get_unknown_characters_number(self.text)

    def get_char_data(self, char):
        char_encoded = char.encode('utf-8')
        # special characters
        if char_encoded == CharData.line_break:
            if self.args.verbose:
                print "Linebreak"
            return CharData.from_line_break()
        elif char_encoded in CharData.special_characters:
            if self.args.verbose:
                print "special character:", char_encoded
            return CharData.from_special_character(char_encoded)
        elif char_encoded == CharData.strange_character:
            if self.args.verbose:
                print "strange character:", list(char_encoded)
            return None
        try:
            if self.characters_dictionary.has_character(char_encoded):
                return self.characters_dictionary.get_character(char_encoded)
            else:
                char_data = self.handle_normal_character(char_encoded)
                self.characters_dictionary.add_character(char_data)
                return char_data

        except IndexError, error:
            print "Unexpected character:", char
            raise error

    def handle_normal_character(self, char_encoded):
        url_full = url_root + char_encoded
        soup = get_soup(url_full)
        traditional = get_character_item(soup, 'kTraditionalVariant')
        simplified = get_character_item(soup, 'kSimplifiedVariant')
        if simplified is None:
            # traditional has been found, or fallback when nothing found
            simplified = char_encoded
        elif traditional is None:
            traditional = char_encoded
        pinyin = get_chinese_item(soup, 'kMandarin')
        translation = get_chinese_item(soup, 'kDefinition')

        if self.args.verbose:
            print "   " + str(simplified) + "(" + str(traditional) + ")", \
                "pinyin:", pinyin, "/ translation:", translation
        return CharData(simplified, traditional, pinyin, translation)

    def make_metadata(self):
        try:
            print "Getting data for text:", self.text.title_english
            get_char_data_no_arg = \
                (lambda char: self.get_char_data(char))
            self.text.make_json(get_char_data_no_arg, self.args.all_characters)
            if self.args.verbose:
                print "JSON encoding for text:", self.text.chars_data
                print
            if self.args.fill_db:
                self.text.save_no_parsing()
        except KeyboardInterrupt, error:
            print
            print "Interrupting - Erasing data for text:", self.text.title_english
            self.text.chars_data = None
            raise error
        except IndexError, error:
            print "Got an unexpected character in text:", self.text.title_english, \
                "; parsing on!"
            print "     got:", error
        finally:
            self.fill_content_pinyin()

    def fill_content_pinyin(self):
        chars_data = self.text.get_all_chars_data()

        def get_pinyin_content(char_data):
            if char_data.pinyin is not None:
                return char_data.pinyin
            else:
                return char_data.character_simplified

        content_pinyin = " ".join([get_pinyin_content(char_data)
                                   for char_data in chars_data])
        self.text.content_pinyin = content_pinyin
        print "got content_pinyin:", content_pinyin[:50], "..."
        if self.args.fill_db:
            self.text.save_no_parsing()

    def save_in_dictionary(self):
        chars_data = self.text.get_all_chars_data()
        if chars_data is not None:
            for char_data in chars_data:
                if not self.characters_dictionary.\
                        has_character(char_data.character_simplified):
                    self.characters_dictionary.add_character(char_data, )
        print "save_in_dictionary:", \
            len(self.characters_dictionary.characters_dictionary.keys()), \
            "words"


