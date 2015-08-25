from texts.scraping.pinyin import MetadataParser


def check_process_text(text, original_text):
    if is_chinese_different(original_text, text):
        print "Differences after edit"
        metadata_parser_old = MetadataParser(original_text)
        metadata_parser_old.save_in_dictionary()
        metadata_parser = MetadataParser(
            text, metadata_parser_old.characters_dictionary)
        number_unknown = metadata_parser.get_unknown_characters_number()
        if number_unknown > 0:
            print "Unknown characters:", number_unknown, \
                "- Deleting the metadata"
            text.chars_data = None
            text.content_pinyin = None
        text.save_no_parsing()
    else:
        print "No differences in chinese text after edit"


def is_chinese_different(original_text, instance):
    """ warning: this fails at first edit
    """
    try:
        old_text = instance.content_chinese
        original_text_string = original_text.content_chinese.encode("utf-8")
        differences = [(instance.content_chinese[index].encode('utf-8'), char_original.encode('utf-8'))
                       for index, char_original
                       in enumerate(original_text.content_chinese)
                       if instance.content_chinese[index].encode('utf-8') != char_original.encode('utf-8')]
        print "differences", differences
        return differences != []
    except IndexError, e:
        return True

