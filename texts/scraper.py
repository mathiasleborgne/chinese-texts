#-*- coding: utf-8 -*-

import os
import urllib2
from bs4 import BeautifulSoup
from django.db.utils import DataError

os.environ['DJANGO_SETTINGS_MODULE'] = 'chinese_texts.settings'
from texts.models import Text, Author
import django
django.setup()

debug = False
few_texts = debug  # run the script on a few texts, to avoid flooding the db
fill_db = not debug

url_root_dufu = "http://www.chinese-poems.com/du.html"
sample_poem_url = "http://www.chinese-poems.com/d16.html"
poem_url_prefix = "http://www.chinese-poems.com/"


def get_du_fu():
    try:
        author = Author.objects.filter(name_pinyin="Du Fu")[0]
        return author
    except IndexError:
        name_chinese = "杜甫"
        name_pinyin = "Du Fu"
        year_birth = 712
        year_death = 770
        author = Author(name_chinese=name_chinese,
                        name_pinyin=name_pinyin,
                        year_birth=year_birth,
                        year_death=year_death)
        author.save()
        return get_du_fu()


def find_all_poems(url_root):
    soup = BeautifulSoup(get_html(url_root), 'html.parser')

    def is_poem_link(tag):
        return tag.name == 'a' and tag["href"][0] == 'd'

    poem_links = soup.find_all(is_poem_link)
    poem_url_suffixs = [tag["href"] for tag in poem_links]

    def make_poem_full_url(poem_url_suffix):
        return poem_url_prefix + poem_url_suffix

    return [make_poem_full_url(poem_url_suffix)
            for poem_url_suffix in poem_url_suffixs]


def get_html(url):
    response = urllib2.urlopen(url)
    print "gettingurl:", url
    return response.read()


def parse_html(url):
    soup = BeautifulSoup(get_html(url), 'html.parser')
    try:
        content_english = soup.find(id="translation").decode_contents()
        content_chinese = soup.find(id="characters").decode_contents()
        content_pinyin = soup.find(id="pinyin").decode_contents()

        def is_title(tag):
            return tag.name == "span" and tag["class"][0] == "title"

        title_english = soup.find(is_title).decode_contents()
        # author_english = soup.find(class="poet").decode_contents()
        make_text(title_english,
                  content_english, content_chinese, content_pinyin)
    except AttributeError, error:
        print "parsing problem for url:", url, " / error:", error


def get_pretty_content_du(title_english, content_english, content_chinese,
                          content_pinyin):

    (title_chinese, title_pinyin) = get_titles_content_du(content_chinese,
                                                          content_pinyin)
    content_english_pretty = pretty_content_du(content_english, False)
    content_chinese_pretty = pretty_content_du(content_chinese, True)
    content_pinyin_pretty = pretty_content_du(content_pinyin, True)

    if not check_length(title_english,
                        content_english_pretty, content_chinese_pretty):
        content_chinese_pretty = pretty_content_du(content_chinese, True, True)
        if check_length(title_english,
                        content_english_pretty, content_chinese_pretty):
            print "Successfully resized chinese content"
        else:
            raise RuntimeError("Bad alignment")

    return (title_chinese, title_pinyin,
            content_english_pretty, content_chinese_pretty,
            content_pinyin_pretty)


def make_text(title_english, content_english, content_chinese, content_pinyin):
    author = get_du_fu()
    if fill_db:
        remove_text_duplicate(title_english)

    try:
        (title_chinese, title_pinyin, content_english_pretty,
         content_chinese_pretty, content_pinyin_pretty) = \
            get_pretty_content_du(title_english, content_english,
                                  content_chinese, content_pinyin)
    except RuntimeError, error:
        return
    print "title:", title_english
    print "content:", (content_english_pretty[:20] + "...") if fill_db \
        else content_english_pretty
    if not fill_db:
        print
        print "content english:", content_english_pretty
        print
        print "content english raw:", content_english
        print
        print "content chinese:", content_chinese_pretty
        print
        print "content chinese raw:", content_chinese
        print
        print "content pinyin:", content_pinyin_pretty
        print
        print "content pinyin raw:", content_pinyin
        print

    if fill_db:
        #add to the DB
        try:
            text = Text(title_english=title_english,
                        title_chinese=title_chinese,
                        title_pinyin=title_pinyin,
                        author=author,
                        content_english=content_english_pretty,
                        content_chinese=content_chinese_pretty,
                        content_pinyin=content_pinyin_pretty)
            print "save text:", title_english
            text.save()
        except DataError, error:
            print "DB error, couldn't save text:", title_english, "-", error


def get_titles_content_du(content_chinese, content_pinyin):

    def split_linebreak(content):
        return content.split("<br>")[0]

    return (split_linebreak(content_chinese), split_linebreak(content_pinyin))


def remove_all(list_filter, element):
    return filter(lambda a: a != element, list_filter)


def pretty_content_du(content, remove_title, save_first_line=False):

    # todo use remove_str

    def remove_str(content, str_to_remove, start_at=0):
        new_content = content.split(str_to_remove)[start_at:]
        return "".join(new_content)

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


def check_length(title_english, content_english, content_chinese):

    def count_lines(content):
        return len(content.split("\n"))

    if count_lines(content_english) != count_lines(content_chinese):
        print "Bad alignment for text:", title_english
        print ">>> english:", count_lines(content_english)
        print ">>> chinese:", count_lines(content_chinese)
        return False
    else:
        return True


def remove_text_duplicate(title_english):
    texts = Text.objects.filter(title_english=title_english)
    for text in texts:
        print "removing:", title_english
        text.delete()

print "Find all URLs"
poem_urls = find_all_poems(url_root_dufu)
if few_texts:
    poem_urls = poem_urls[:3]
for poem_url in poem_urls:
    print "Getting poem at:", poem_url
    parse_html(poem_url)
