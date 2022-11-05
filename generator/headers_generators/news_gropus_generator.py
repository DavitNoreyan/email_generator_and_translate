# Generating news groups header

from email.header import Header
from typing import Optional, List

from generator.utils.random_strings_generator import random_ascii_letters_generator


def generate_news_groups(header_name: str, count: int = 1, domain_length: int = 10, subdomain_length: int = 5,
                         news_groups: Optional[List[str]] = None) -> Header:
    """
    If there is no news_groups generating random news groups and returning Header wiht generated value,
    otherwise news_groups will be used as value.
    :param header_name: describes email.header.Header.header_name property
    :param count: generating news_groups count
    :param domain_length: generating domain length
    :param subdomain_length: generating subdomain length
    :param news_groups: use for manually set up value
    :return: email.headers.Header instance with generated or got news_groups
    """
    if news_groups:
        if len(news_groups) == 0:
            content = news_groups[0]
        else:
            content = " , ".join(news_groups)
    else:
        if count == 1:
            content = \
                f"{random_ascii_letters_generator(domain_length)}.{random_ascii_letters_generator(subdomain_length)}"
        else:
            news_groups_list = []
            for _ in range(count):
                news_groups_list.append(
                    f"{random_ascii_letters_generator(domain_length)}.{random_ascii_letters_generator(subdomain_length)}")
            content = " , ".join(news_groups_list)
    return Header(s=content, header_name=header_name)
