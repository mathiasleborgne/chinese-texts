#-*- coding: utf-8 -*-

import os
import urllib2
os.environ['DJANGO_SETTINGS_MODULE'] = 'chinese_texts.settings'
from texts.models import Text, Author
import django
django.setup()

from django.db.utils import DataError
from texts.scraping.scraping_tools import get_parser, get_html, get_soup
from texts.scraping.pinyin import MetadataParser


class TextScraper(object):
    """ abstract class for scraping
    """

    scraping_name = NotImplementedError

    def __init__(self, args):
        super(TextScraper, self).__init__()
        self.content_english_raw = None
        self.content_chinese_raw = None
        self.content_pinyin_raw = None
        self.args = args
        print "Find all URLs"
        poem_urls = self.get_all_poems_urls()
        if self.args.verbose:
            print "Got", len(poem_urls), "urls:", poem_urls[:6]
        if self.args.few_items:
            poem_urls = poem_urls[:3]
        print "parsing", len(poem_urls), "urls"
        for index_url, poem_url in enumerate(poem_urls):
            print "Getting poem at:", poem_url
            self.index_url = index_url
            self.soup = get_soup(poem_url)
            try:
                self.parse_html()
            except AttributeError, error:
                print "parsing problem for url:", poem_url, " / error:", error
                continue
            try:
                self.get_pretty_content()
            except RuntimeError, error:
                continue
            self.print_info()
            self.make_text()
            if not self.text.check_lines():
                print "Bad lines alignement for text:", \
                    self.text.title_english, "- not saving"
                continue
            if not self.args.no_metadata:
                self.get_text_metadata()

            if not self.args.print_only:
                self.add_text_to_db()

    def get_all_poems_urls(self, url_root):
        raise NotImplementedError

    def get_pretty_content(self):
        (self.title_chinese, self.title_pinyin) = self.get_titles_content()
        self.content_english_pretty = \
            self.pretty_content(self.content_english_raw, False)
        self.content_chinese_pretty = \
            self.pretty_content(self.content_chinese_raw, True)
        self.content_pinyin_pretty = None if self.content_pinyin_raw is None else \
            self.pretty_content(self.content_pinyin_raw, True)

    @staticmethod
    def pretty_content(content, remove_title, save_first_line=False):
        raise NotImplementedError

    def get_titles_content(self):
        raise NotImplementedError

    def print_info(self):
        if not self.args.verbose:
            print "title:", self.title_english
            print "content:", (self.content_english_pretty[:20] + "...") \
                if not self.args.print_only else self.content_english_pretty
        else:
            print
            print "content english:", self.content_english_pretty
            print "-"
            if self.content_english_raw is not None:
                print "content english raw:", self.content_english_raw
                print "-"
            print "content chinese:", self.content_chinese_pretty
            print "-"
            if self.content_chinese_raw is not None:
                print "content chinese raw:", self.content_chinese_raw
                print "-"
            print "content pinyin:", self.content_pinyin_pretty
            print "-"
            if self.content_pinyin_raw is not None:
                print "content pinyin raw:", self.content_pinyin_raw
                print "-"

    def parse_html(self):
        """ should set self.name_pinyin amongst other variables """
        raise NotImplementedError

    def get_author(self):
        try:
            author = Author.objects.filter(name_pinyin=self.name_pinyin)[0]
            return author
        except IndexError:
            self.make_author()
            return self.get_author()

    def make_author(self):
        raise NotImplementedError

    def make_text(self):
        author = self.get_author()
        self.text = Text(title_english=self.title_english,
                         title_chinese=self.title_chinese,
                         title_pinyin=self.title_pinyin,
                         author=author,
                         content_english=self.content_english_pretty,
                         content_chinese=self.content_chinese_pretty,
                         content_pinyin=self.content_pinyin_pretty)
        print "current text:", self.text

    def get_text_metadata(self):
        metadata_parser = MetadataParser(self.text, None, args)
        metadata_parser.make_metadata()


    def add_text_to_db(self):
        texts = Text.objects.filter(title_english=self.title_english)
        if texts and self.args.preserve_db:
            print "Not replacing text:", self.title_english
            return
        else:
            try:
                remove_text_duplicate(texts)
                print "save text:", self.title_english
                self.text.save_no_parsing()
            except DataError, error:
                print "DB error, couldn't save text:", self.title_english, \
                    "-", error



class ZhuangScraper(TextScraper):

    scraping_name = "zhuangzi"

    def get_all_poems_urls(self):
        url_suffixes = [
            "enjoyment-in-untroubled-ease",
            "adjustment-of-controversies",
            "nourishing-the-lord-of-life",
            "man-in-the-world-associated-with",
            "seal-of-virtue-complete",
            "great-and-most-honoured-master",
            "normal-course-for-rulers-and-kings",
        ]
        global_urls_lists = [self.find_sub_text(url_suffix)
                             for url_suffix in url_suffixes]
        global_urls = []
        self.titles = []

        for global_urls_list, _ in global_urls_lists:
            global_urls += global_urls_list
        for global_urls_list, title_global in global_urls_lists:
            for index_url, url in enumerate(global_urls_list):
                self.titles.append(title_global + " " + str(index_url + 1))
        print self.titles
        return global_urls

    def find_sub_text(self, url_suffix):
        try:
            url_root = "http://ctext.org/"
            url_zhuang = "zhuangzi/"
            global_url = url_root + url_zhuang + url_suffix
            if self.args.verbose:
                print "parsing global_url:", global_url
            sub_soup = get_soup(global_url)


            sub_texts_links = sub_soup.find_all(title="Jump to dictionary")
            # <meta property="og:title" content="Enjoyment in Untroubled Ease"/>
            title_english = sub_soup.find_all(property="og:title")[0].get("content")
            sub_texts_urls = [url_root + link.get("href") for link in sub_texts_links]
            return sub_texts_urls, title_english
        except urllib2.HTTPError, error:
            print "couldn't parse", global_url, ". Got:", error, "/", \
                error.fp.read()
            return [], None


    def make_author(self):
        name_chinese = "庄子"
        year_birth = -369
        year_death = -286
        author = Author(name_chinese=name_chinese,
                        name_pinyin=self.name_pinyin)
        author.save()

    def parse_html(self):
        self.name_pinyin = "Zhuangzi"

        def is_chinese_char(tag):
            return tag.name == 'a' and "#char" in tag["href"] \
                and tag.get("class") is not None and "popup" in tag.get("class")

        def is_english_line(tag):
            return tag.name == 'td' \
                and tag.get("class") is not None and "etext" in tag.get("class")

        def is_char_or_english(tag):
            return is_chinese_char(tag) or is_english_line(tag)

        tags_candidates = self.soup.find_all(is_char_or_english)
        lines = []
        current_chinese_line = ""
        for tag in tags_candidates:
            if is_chinese_char(tag):
                char = tag.decode_contents()[0]
                current_chinese_line += char
            elif is_english_line(tag) and current_chinese_line != "":
                english_line = tag.decode_contents()
                lines.append((current_chinese_line, english_line))
                current_chinese_line = ""

        title_url = self.titles[self.index_url]
        self.title_english = title_url
        self.title_chinese = title_url
        self.content_chinese_pretty = "\n".join([chinese_line
                                                 for chinese_line, _ in lines])
        self.content_english_pretty = "\n".join([english_line
                                                 for _, english_line in lines])
        self.title_pinyin = None
        self.content_pinyin_pretty = None

    def get_pretty_content(self):
        pass

class WenguScraper(TextScraper):

    scraping_name = "wengu"

    def get_all_poems_urls(self):
        url_root = "http://wengu.tartarie.com/wg/wengu.php?l=Tangshi&no="
        number_poems = 320
        return [url_root + str(id_poem) for id_poem in range(number_poems)[1:]]

    def parse_html(self):
        self.content_english_raw = self.soup.find(id="Bynner1").p.decode_contents()
        self.content_chinese_raw = self.soup.find(id="Horizontal1").p.decode_contents()
        self.content_pinyin_raw = None
        self.title_english = self.soup.select(".sousTitre br")[0].decode_contents()
        self.name_pinyin = self.soup.select(".sousTitre b")[0].decode_contents()
        chars_name = self.soup.select(".sousTitre a")
        self.name_chinese = ''.join([char.decode_contents() for char in chars_name])

    def print_info(self):
        super(WenguScraper, self).print_info()
        if self.args.verbose:
            print "Author:"
            print "  name_pinyin:", self.name_pinyin
            print "  name_chinese:", self.name_chinese

    def get_titles_content(self):

        def split_linebreak(content):
            new_content = content.split("<br>")[0]
            return remove_str(new_content, "\n ")

        return (split_linebreak(self.content_chinese_raw), None)

    @staticmethod
    def pretty_content(content, remove_title, save_first_line=False):
        new_content = remove_str(content, "</br>")
        if remove_title:
            new_content = remove_str(new_content, "<br>", 1)
            new_content = new_content.replace("\r", "").replace(" ", "\n")\
                .replace("\n\n", "\n")
            new_content = new_content[1:]

        else:
            new_content = remove_str(new_content, "<br>\n")
        return new_content

    def make_author(self):
        author = Author(name_chinese=self.name_chinese,
                        name_pinyin=self.name_pinyin)
        author.save()


class DuFuScraper(TextScraper):

    scraping_name = "dufu"
    sample_poem_url = "http://www.chinese-poems.com/d16.html"
    poem_url_prefix = "http://www.chinese-poems.com/"

    def make_author(self):
        name_chinese = "杜甫"
        year_birth = 712
        year_death = 770
        author = Author(name_chinese=name_chinese,
                        name_pinyin=self.name_pinyin,
                        year_birth=year_birth,
                        year_death=year_death)
        author.save()

    def get_all_poems_urls(self):
        url_root = "http://www.chinese-poems.com/du.html"
        soup = get_soup(url_root)

        def is_poem_link(tag):
            return tag.name == 'a' and tag["href"][0] == 'd'

        poem_links = soup.find_all(is_poem_link)
        poem_url_suffixs = [tag["href"] for tag in poem_links]

        def make_poem_full_url(poem_url_suffix):
            return self.poem_url_prefix + poem_url_suffix

        return [make_poem_full_url(poem_url_suffix)
                for poem_url_suffix in poem_url_suffixs]

    def parse_html(self):
        self.content_english_raw = self.soup.find(id="translation").decode_contents()
        self.content_chinese_raw = self.soup.find(id="characters").decode_contents()
        self.content_pinyin_raw = self.soup.find(id="pinyin").decode_contents()
        self.name_pinyin = "Du Fu"

        def is_title(tag):
            return tag.name == "span" and tag["class"][0] == "title"

        self.title_english = self.soup.find(is_title).decode_contents()
        # author_english = self.soup.find(class="poet").decode_contents()

    def check_length(self, content_english, content_chinese):

        def count_lines(content):
            return len(content.split("\n"))

        if count_lines(content_english) != count_lines(content_chinese):
            print "Bad alignment for text:", self.title_english
            print ">>> english:", count_lines(content_english)
            print ">>> chinese:", count_lines(content_chinese)
            return False
        else:
            return True

    def get_pretty_content(self):
        super(DuFuScraper, self).get_pretty_content()
        if not self.check_length(self.content_english_pretty, self.content_chinese_pretty):
            self.content_chinese_pretty = self.pretty_content(self.content_chinese_raw, True, True)
            if self.check_length(self.content_english_pretty, self.content_chinese_pretty):
                print "Successfully resized chinese content"
            else:
                raise RuntimeError("Bad alignment")

    @staticmethod
    def pretty_content(content, remove_title, save_first_line=False):
        # remove </br>
        new_content = remove_str(content, "</br>")
        new_content = remove_str(new_content, "<br>", 2 if remove_title else 0)
        # remove first \n
        if remove_title and not save_first_line:
            new_content = new_content.split("\n")[2:]
        else:
            new_content = new_content.split("\n")[1:]
        new_content = remove_all(new_content, "")
        new_content = "\n".join(new_content)
        # remove spans
        new_content = remove_str(new_content, "<span class=\"chinese\">")
        new_content = remove_str(new_content, "</span>")

        return new_content

    def get_titles_content(self):

        def split_linebreak(content):
            return content.split("<br>")[0]

        return (split_linebreak(self.content_chinese_raw),
                split_linebreak(self.content_pinyin_raw))


def remove_all(list_filter, element):
    return filter(lambda a: a != element, list_filter)


def remove_str(content, str_to_remove, start_at=0):
    new_content = content.split(str_to_remove)[start_at:]
    return "".join(new_content)


def remove_text_duplicate(texts):
    for text in texts:
        print "removing:", text.title_english
        text.delete()


scraping_classes = [
    DuFuScraper,
    ZhuangScraper,
    WenguScraper,
]


def get_texts_parser():
    sources = [scraping_class.scraping_name
               for scraping_class in scraping_classes]
    parser = get_parser()
    parser.add_argument("--source", default="wengu",
                        help="Scraping Source, amongst: " + str(sources))
    parser.add_argument("--no_metadata",
                        action="store_true",
                        help="Don't collect metadata")
    return parser


if __name__ == "__main__":
    print "running scraper"
    args = get_texts_parser().parse_args()
    # todo: hoave a selection arg
    sources_dict = {scraping_class.scraping_name: scraping_class
                    for scraping_class in scraping_classes}
    ScraperClass = sources_dict[args.source]
    print "Scraping website:", args.source
    scraper = ScraperClass(args)