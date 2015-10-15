import urllib2
import argparse
from bs4 import BeautifulSoup


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--few_items",
                        action="store_true",
                        help="Run test on a few items")
    parser.add_argument("--print_only",
                        action="store_true",
                        help="Don't actually change the database")
    parser.add_argument("--preserve_db",
                        action="store_true",
                        help="Only re-fetch data for texts without data")
    parser.add_argument("--few_characters",
                        action="store_true",
                        help="Get only a few characters from the texts")
    parser.add_argument("--verbose",
                        action="store_true",
                        help="A lot of logs")
    return parser


def get_html(url):
    request = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    response = urllib2.urlopen(request)
    return response.read()


def get_soup(url):
    return BeautifulSoup(get_html(url), 'html.parser')
