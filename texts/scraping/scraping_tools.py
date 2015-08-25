import urllib2
import argparse
from bs4 import BeautifulSoup


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--many_items",
                        action="store_true",
                        help="Run test on many items")
    parser.add_argument("--fill_db",
                        action="store_true",
                        help="Actually change the database")
    parser.add_argument("--reset_db",
                        action="store_true",
                        help="Re-fetch pinyin for all texts in the db, instead"
                             " of only fetching the texts without pinyin")
    return parser


def get_html(url):
    response = urllib2.urlopen(url)
    return response.read()


def get_soup(url):
    return BeautifulSoup(get_html(url), 'html.parser')
