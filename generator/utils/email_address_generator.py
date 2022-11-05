from logging import getLogger
from random import choice
from string import ascii_letters, digits
from typing import Optional, List

from .random_strings_generator import random_ascii_letters_generator

logger = getLogger("info_logger")

DEFAULT_LOCAL_NAME_LENGTH = 32
DEFAULT_EMAIL_SERVICE_NAME_LENGTH = 8
DEFAULT_DOMAIN_LENGTH = 3


def random_email_local_name_generator(length: int) -> str:
    """
        Generating username or email local name with got length.
        Using all ascii letters digits and "." "_" "-" symbols.
    :param length: length of generating email local name ( email's username )
    :return: generated email username with got length
    """
    if length > 64:
        logger.warning("Email address local name length should be smaller than 65. Value changed to 64")
        length = 64
    return "".join(choice(ascii_letters) + choice(ascii_letters + digits + "._-") for _ in range(length - 1))


def random_email_address_generator(email_local_name_length: Optional[int], email_service_name_length: Optional[int],
                                   domain_length: Optional[int],
                                   email_service_list: Optional[List[str]] = None) -> str:
    """
        Generating random email address.
    :param email_local_name_length: email_local_name or email's username length
    :param email_service_name_length: generating email service name length or subdomain length
    :param domain_length: generating domain length
    :param email_service_list: email subdomain and domains list. If got this property
    email_service_name_length and domain_length will be ignored.
    :return: generated email address.
    """
    if email_service_list:
        email_local_name_length = email_local_name_length if email_local_name_length else DEFAULT_LOCAL_NAME_LENGTH
        return "".join(
            [random_email_local_name_generator(email_local_name_length), "@", choice(email_service_list)])
    else:
        email_local_name_length = email_local_name_length if email_local_name_length else DEFAULT_LOCAL_NAME_LENGTH
        email_service_name_length = email_service_name_length if email_service_name_length else DEFAULT_LOCAL_NAME_LENGTH
        domain_length = domain_length if domain_length else DEFAULT_DOMAIN_LENGTH
        return "".join([random_email_local_name_generator(email_local_name_length), "@",
                        random_ascii_letters_generator(email_service_name_length).lower(), ".",
                        random_ascii_letters_generator(domain_length).lower()])
