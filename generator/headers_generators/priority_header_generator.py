# generate priority header

from email.header import Header
from logging import getLogger
from random import choice
from typing import Optional, List

logger = getLogger("info_logger")
PRIORITY_HEADER_POSSIBLE_VALUES: List[str] = ["normal", "urgent", "non-urgent"]


def generate_priority_header(header_name: str, value: Optional[str] = None) -> Header:
    """
    If there is no value or value is invalid randomly selecting priority from PRIORITY_HEADER_POSSIBLE_VALUES
    and returning Header with selected value or using 'value' argument.
    :param header_name: describes email.header.Header.header_name property
    :param value: use for set up value manually
    :return: email.header.Header with randomly selected priority or using value.
    """
    if value:
        if value not in PRIORITY_HEADER_POSSIBLE_VALUES:
            logger.error(f"{value} isn't valid value for priority header.")
            raise Exception(f"{value} isn't valid value for priority header. Check the headers.json config file.")
        else:
            content = value
    else:
        content = choice(PRIORITY_HEADER_POSSIBLE_VALUES)
    return Header(s=content, header_name=header_name)
