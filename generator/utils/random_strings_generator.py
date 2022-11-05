# There are described random text generators with its mappings
from random import choice
from string import ascii_letters
from typing import Dict, List

from .languages_chars_in_unicode import FRENCH_CHARACTERS, FRENCH_CHARACTERS_WITHOUT_PUNCTUATION_AND_DIGITS, \
    ENGLISH_WITHOUT_PUNCTUATION_AND_DIGITS, ENGLISH_CHARACTERS

languages_chars_in_unicode_mapping = {
    "en": ENGLISH_CHARACTERS,
    "fr": FRENCH_CHARACTERS,
}
DEFAULT_TEXT_LENGTH = 150


def lang_random_str_generator(language: str, length: int, mapper: Dict[str, List[int]]) -> str:
    """
    Generating random string for got language.
    Mapper will be used to describe wich unicode symbols range should be used.
    :param language: generating text's language
    :param length: generating text's length
    :param mapper: which mapper should be used in generation process.
    :return: generated text
    """
    char_list = mapper.get(language.lower())
    generated_str = ""
    for _ in range(length):
        generated_str += chr(choice(char_list))
    return generated_str


languages_chars_in_unicode_mapping_for_name: Dict[str, List[int]] = {
    "fr": FRENCH_CHARACTERS_WITHOUT_PUNCTUATION_AND_DIGITS,
    "en": ENGLISH_WITHOUT_PUNCTUATION_AND_DIGITS
}


def random_f_name_s_name_generator(language: str, f_name_length: int, s_name_length: int) -> str:
    """
    Generating seperated firstname and lastname.
    :param language: generating firstname and lastname language
    :param f_name_length: firstname length
    :param s_name_length: lastname length
    :return: generated firstname and lastname
    """
    f_name = lang_random_str_generator(language, f_name_length, languages_chars_in_unicode_mapping_for_name)
    l_name = lang_random_str_generator(language, s_name_length, languages_chars_in_unicode_mapping_for_name)
    return f"{f_name} {l_name}"


def random_text_generator(language: str, length: int) -> str:
    """
    Generates random text for got language , also will be used symbols digits etc.
    :param language: generating text's language
    :param length: generating text's length
    :return: generated text
    """
    if not length:
        length = DEFAULT_TEXT_LENGTH
    return lang_random_str_generator(language, length, languages_chars_in_unicode_mapping)


def random_ascii_letters_generator(length: int) -> str:
    """
    Generating string using only ascii letters.
    :param length: generating string's length
    :return: returned randomly generated string
    """
    return ''.join(choice(ascii_letters) for x in range(length))
