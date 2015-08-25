#-*- coding: utf-8 -*-

def get_unicode(character):
    if character is None:
        return None
    return character if type(character) == unicode else character.decode("utf-8")


class CharData(object):
    """Metadata for chinese character
    """

    special_characters = [
        "。", "，", "?", "；", "？", "！",
    ]
    line_break = "\n"
    strange_character = "\r"

    def __init__(self, character_simplified, character_traditional,
                 pinyin, translation):
        """ Class for character metadata handling
            Character_traditional can be None, not character_simplified
        """
        super(CharData, self).__init__()
        character_simplified = get_unicode(character_simplified)
        character_traditional = get_unicode(character_traditional)
        if character_simplified is None:
            raise Exception("wrong character data")
        self.character_simplified = character_simplified
        self.character_traditional = character_traditional \
            if character_traditional is not None else character_simplified
        self.is_line_break = character_simplified == self.line_break
        self.is_special_character = \
            character_simplified in [get_unicode(char) for char in self.special_characters]
        self.translation = translation
        self.pinyin = pinyin

    @classmethod
    def from_json(cls, item_json):
        "Initialize CharData from a json serialization"
        character_simplified = item_json[0]
        if len(item_json) < 4:
            character_traditional = None
            pinyin = None
            translation = None
        else:
            character_traditional = item_json[1]
            pinyin = item_json[2]
            translation = item_json[3]
        return cls(character_simplified, character_traditional,
                   pinyin, translation)

    @classmethod
    def from_line_break(cls):
        return cls("\n", None, None, None)

    @classmethod
    def from_special_character(cls, character_simplified):
        return cls(character_simplified, None, None, None)

    def get_JSONable_item(self):
        if self.is_line_break:
            return [self.character_simplified]
        else:
            return [self.character_simplified, self.character_traditional,
                    self.pinyin, self.translation]
