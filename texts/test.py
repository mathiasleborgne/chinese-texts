#-*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from texts.models import Text, Author


def create_author():
    return Author.objects.create(name_chinese="李商隱",
                                 name_pinyin="Li Shangyin")


def create_text():
    author = Author.objects.all()[0]
    return Text.objects.create(
        title_english="Cithare ornée de brocart",
        title_chinese="錦瑟",
        content_chinese="錦瑟無端五十弦",
        content_pinyin="Jǐn sè wúduān wǔshí xián",
        content_english="cithare ornée pur hasard / avec cinquante cordes",
        author=author
        )


class AllViewsTests(TestCase):

    def test_all_views_work(self):

        create_author()
        create_text()
        all_authors = Author.objects.all()
        self.assertTrue(all_authors != [])
        author_id = all_authors[0].id
        all_texts = Text.objects.all()
        self.assertTrue(all_texts != [])
        text_id = all_texts[0].id

        print "IDs:", text_id, author_id

        view_adresses_dict = {
            "highlighted_texts": None,
            "texts_list": None,
            "read_text": text_id,
            "authors": None,
            "author_page": author_id,
            "contact": None,
            "create_user": None,
            "create_user_success": None,
            "log_in": None,
            "create_author": None,
            "new_text": None,
            "about": None,
            "poll": None,
            "search_texts": None,
        }
        for view_adress, arguments in view_adresses_dict.iteritems():
            print "Testing address:", view_adress
            if arguments is None:
                response = self.client.get(reverse(view_adress))
            else:
                response = self.client.get(reverse(view_adress,
                                                   args=(arguments,)))
            self.assertEqual(response.status_code, 200)