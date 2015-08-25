#-*- coding: utf-8 -*-
from texts.char_data import get_unicode
from texts.char_data import CharData


class CharactersDictionary(object):
    """docstring for CharactersDictionary"""

    def __init__(self):
        super(CharactersDictionary, self).__init__()
        self.characters_dictionary = self.load()

    def load(self):
        # todo: load from JSON in DB
        return {}

    def add_character(self, char_data):
        if self.has_character(char_data.character_simplified) or \
                self.has_character(char_data.character_traditional):
            return
        self.characters_dictionary[char_data.character_simplified] = char_data
        self.characters_dictionary[char_data.character_traditional] = char_data

    def has_character(self, character_simpl_or_trad):
        return get_unicode(character_simpl_or_trad) in self.characters_dictionary

    def get_character(self, character_simpl_or_trad):
        return self.characters_dictionary[get_unicode(character_simpl_or_trad)]

    def save(self):
        # todo: save as JSON in DB
        pass

    def get_unknown_characters_number(self, text):
        return len([character for character in text.content_chinese
                    if not self.has_character(character)
                    and not character in CharData.special_characters
                    and not character in CharData.line_break
                    and not character in CharData.strange_character])
