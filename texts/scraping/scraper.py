#-*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'chinese_texts.settings'
from texts.models import Text, Author
import django
django.setup()

from django.db.utils import DataError
from texts.scraping.scraping_tools import get_parser, get_html, get_soup
from texts.scraping.pinyin import MetadataParser


def get_texts_parser():
    parser = get_parser()
    parser.add_argument("--dufu",
                        action="store_true",
                        help="Parse the du fu site instead of the wengu site")
    return parser


class TextScraper(object):
    """ abstract class for scraping
    """

    def __init__(self, args):
        super(TextScraper, self).__init__()
        self.args = args
        print "Find all URLs"
        poem_urls = self.get_all_poems_urls()
        if self.args.few_items:
            poem_urls = poem_urls[:3]
        print "parsing", len(poem_urls), "urls"
        for poem_url in poem_urls:
            print "Getting poem at:", poem_url
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
            self.get_text_metadata()

            if not self.args.print_only:
                self.add_text_to_db()

    def get_author(self):
        pass

    def get_all_poems_urls(self, url_root):
        pass

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
        pass

    def get_titles_content(self):
        pass

    def print_info(self):
        if not self.args.print_only:
            print "title:", self.title_english
            print "content:", (self.content_english_pretty[:20] + "...") \
                if not self.args.print_only else self.content_english_pretty
        else:
            print
            print "content english:", self.content_english_pretty
            print "-"
            print "content english raw:", self.content_english_raw
            print "-"
            print "content chinese:", self.content_chinese_pretty
            print "-"
            print "content chinese raw:", self.content_chinese_raw
            print "-"
            print "content pinyin:", self.content_pinyin_pretty
            print "-"
            print "content pinyin raw:", self.content_pinyin_raw
            print "-"


    def get_author(self):
        try:
            author = Author.objects.filter(name_pinyin=self.name_pinyin)[0]
            return author
        except IndexError:
            self.make_author()
            return self.get_author()

    def make_author(self):
        pass

    def make_text(self):
        author = self.get_author()
        self.text = Text(title_english=self.title_english,
                         title_chinese=self.title_chinese,
                         title_pinyin=self.title_pinyin,
                         author=author,
                         content_english=self.content_english_pretty,
                         content_chinese=self.content_chinese_pretty,
                         content_pinyin=self.content_pinyin_pretty)

    def get_text_metadata(self):
        metadata_parser = MetadataParser(self.text, None, args)
        metadata_parser.make_metadata()


    def add_text_to_db(self):
        texts = Text.objects.filter(title_english=self.title_english)
        if texts and self.args.preserve_db:
            print "Not replacing text:", self.title_english
            return
        try:
            remove_text_duplicate(texts)
            print "save text:", self.title_english
            self.text.save()
        except DataError, error:
            print "DB error, couldn't save text:", self.title_english, "-", error


class WenguScraper(TextScraper):

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


if __name__ == "__main__":
    print "running scraper"
    args = get_texts_parser().parse_args()
    ScraperClass = DuFuScraper if args.dufu else WenguScraper
    scraper = ScraperClass(args)