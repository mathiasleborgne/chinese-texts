# get some extra info on authors using wikipedia API
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'chinese_texts.settings'
import django
django.setup()
from texts.models import Text, Author
import wikipedia
import argparse
from scraper import get_parser


def get_wiki_parser():
    parser = get_parser()
    parser.add_argument("--save_dates",
                        action="store_true",
                        help="Save the author dates too")
    return parser


def get_authors_names(fill_db, many_items):  # usused for now
    if fill_db:
        authors_db = get_all_authors()
        print authors_db
        authors_list = [author.name_pinyin for author in authors_db]
    else:
        if many_items:
            authors_list = \
                ["Tao Yuanming", "Meng Haoran", "Zhang Jiuling", "Meng Haoran",
                 "Wang Changling", "Qiwu Qian", "Wei Yingwu", "Liu Zongyuan",
                 "Bai Juyi", "Li Shangyin"]
        else:
            authors_list = ["Du Fu", "Zhuangzi", "Tao Yuanming"]
    return authors_list


def get_all_authors(many_items):
    all_authors = Author.objects.all()
    return all_authors if many_items else all_authors[:3]


def find_dates(categories):
    year_birth = None
    year_death = None
    for category in categories:
        keyword = "births"
        if keyword in category:
            year_birth = category.split(" " + keyword)[0]

        keyword = "deaths"
        if keyword in category:
            year_death = category.split(" " + keyword)[0]

    return year_birth, year_death


def save_author_infos(author, biography, year_birth, year_death,
                      save_dates=True):
    author.biography = biography
    author.year_birth = year_birth
    author.year_death = year_death
    author.save()


def print_dates_bio(name_pinyin, biography, year_birth, year_death):
    print name_pinyin
    print "dates:", str(year_birth) + "-" + str(year_death)
    if biography is not None:
        print "bio:", biography[:100] + "..."
    else:
        print "biography wasn't found"
    print


if __name__ == "__main__":
    args = get_wiki_parser().parse_args()

    for author in get_all_authors(args.many_items):
        # fetch wikipedia page
        name_author = author.name_pinyin
        try:
            print "Searching wikipedia for author:", name_author
            page_author = wikipedia.page(name_author)
            biography = wikipedia.summary(name_author)
        except wikipedia.exceptions.PageError, error:
            continue
        except wikipedia.exceptions.DisambiguationError, error:
            print "Several possibilities for", name_author, ":", error
            continue

        # get biography and dates
        (year_birth, year_death) = find_dates(page_author.categories)
        print_dates_bio(name_author, biography, year_birth, year_death)

        if args.fill_db:
            save_author_infos(author, biography,
                              year_birth, year_death, args.save_dates)
            print "Checking Database:"
            for author in get_all_authors(args.many_items):
                print_dates_bio(author.name_pinyin, author.biography,
                                author.year_birth,author.year_death)
