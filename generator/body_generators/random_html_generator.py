# random html generator
from random import randint, choice
from typing import Optional, Dict

from generator.utils.random_strings_generator import random_text_generator

HTML_WORD_MAX_LENGTH = 25
HTML_DEFAULT_TAGS_COUNT = 10
HTML_DEFAULT_SENTENCE_WORDS_COUNT = 5
HTML_TEXT_TAGS = [
    "p",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "strong",
    "em",
    "abbr",
    "address",
    "bdo",
    "blockquote",
    "cite",
    "q",
    "code",
    "ins",
    "del",
    "dfn",
    "kbd",
    "pre",
    "samp",
    "var",
    "br",
    "div",
    "a",
    "base",
    "img",
    "area",
    "map",
    "param",
    "object",
    "ul",
    "ol",
    "li",
    "dl",
    "dt",
    "dd"
]


def generate_sentence(language: str, sentence_words_count: int) -> str:
    # TODO write docs
    sentence = ""
    for _ in range(sentence_words_count):
        sentence += f"{random_text_generator(language, randint(1, HTML_WORD_MAX_LENGTH))} "
    sentence += "."
    sentence.capitalize()
    return sentence


def tag_generator(tag_name: str, sentence: str) -> str:
    # TODO write docs
    return f"<{tag_name}>{sentence}</{tag_name}>"


def generate_random_tag(language: str, sentence_words_max_count: int) -> str:
    # TODO write docs
    tag_name = choice(HTML_TEXT_TAGS)
    words_count = randint(1, sentence_words_max_count)
    sentence = generate_sentence(language, words_count)
    return tag_generator(tag_name, sentence)


def generate_image_tag(content_id: str) -> str:
    # TODO write docs
    return f"<img src='cid:{content_id}'>"


def generate_body(language: str, tags_count: int, sentence_words_max_count: int,
                  inline_images_mapping: Optional[Dict[str, str]] = None) -> str:
    # TODO write docs
    body_elements = []
    for _ in range(tags_count):
        body_elements.append(generate_random_tag(language, sentence_words_max_count))
    if inline_images_mapping:
        for img_cid in inline_images_mapping:
            body_elements.insert(randint(0, len(body_elements)), generate_image_tag(img_cid))
    return "".join(body_elements)


def generate_html(language: str, tags_count: int = HTML_DEFAULT_TAGS_COUNT,
                  sentence_words_max_count: int = HTML_DEFAULT_SENTENCE_WORDS_COUNT,
                  inline_images_mapping: Optional[Dict[str, str]] = None) -> str:
    # TODO write docs
    return f"<html><body>" \
           f"{generate_body(language, tags_count, sentence_words_max_count, inline_images_mapping)}" \
           f"</body></html>"
