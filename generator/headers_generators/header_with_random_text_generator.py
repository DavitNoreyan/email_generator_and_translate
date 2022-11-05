from email.header import Header

from generator.utils.random_strings_generator import random_text_generator


# Functions in this file generating header with random text.

def header_with_random_text_generator(header_name: str, language: str, length: int) -> Header:
    """
    Generating random text and returning email.headers.Header instance with generated value.
    :param header_name: will be used as header_name property for email.header.Header instance
    :param language: describes in which language text should be generated
    :param length: describes generating text characters count
    :return: emails.header.Header
    """
    content = random_text_generator(language, length)
    return Header(s=content, header_name=header_name)
