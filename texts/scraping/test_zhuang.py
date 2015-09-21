#-*- coding: utf-8 -*-
from texts.scraping.scraping_tools import get_parser, get_html, get_soup
from bs4 import BeautifulSoup
url = "http://ctext.org/dictionary.pl?if=en&id=2717"
soup = get_soup(url)


# html_doc = """
# <a class="tn" href="#char24190" class="popup">幾<span></span></a>
# <a class="tn" href="#char21315" class="popup">千<span></span></a>
# <a class="tn" href="#char40300" class="popup">鵬<span></span></a>。
# </td><td class="etext">with the name of Peng,</td></tr><tr id="s10020950" class="trow">
# """
# soup = BeautifulSoup(html_doc, 'html.parser')


def is_chinese_char(tag):
    return tag.name == 'a' and "#char" in tag["href"] \
        and tag.get("class") is not None and "popup" in tag.get("class")

def is_english_line(tag):
    return tag.name == 'td' \
        and tag.get("class") is not None and "etext" in tag.get("class")

def is_char_or_english(tag):
    return is_chinese_char(tag) or is_english_line(tag)

content_chinese_raw = soup.find_all(is_char_or_english)
lines = []
current_chinese_line = ""
for tag in content_chinese_raw:
    if is_chinese_char(tag):
        char = tag.decode_contents()[0]
        print "chinese tag:", char
        current_chinese_line += char
    elif is_english_line(tag) and current_chinese_line != "":
        english_line = tag.decode_contents()
        print "text:", english_line
        lines.append((current_chinese_line, english_line))
        current_chinese_line = ""
print lines

chinese_lines = "\n".join([chinese_line for chinese_line, _ in lines])
english_lines = "\n".join([english_line for _, english_line in lines])

print chinese_lines
print english_lines


