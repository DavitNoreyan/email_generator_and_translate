# Generate Received Header.
from email.header import Header
from random import randint, choice
from string import ascii_lowercase, digits
from typing import Optional

from generator.utils.random_strings_generator import random_ascii_letters_generator
from .email_date_generator import generate_date


def generate_receiver_by_part(domain: Optional[str] = None, smtp_protocol: bool = True,
                              receiving_year: Optional[int] = None,
                              receiving_month: Optional[int] = None, receiving_day: Optional[int] = None,
                              receiving_hour: Optional[int] = None, receiving_minute: Optional[int] = None,
                              receiving_second: Optional[int] = None) -> str:
    """
    Generating 'by' part for Received header.
    :param domain: will be used in generating process , if not described will be generated randomly
    :param smtp_protocol: set receiver protocol smtp or http
    :param receiving_year: generating date year
    :param receiving_month: generating date month
    :param receiving_day: generating date day
    :param receiving_hour: generating date hour
    :param receiving_minute: generating date minute
    :param receiving_second: generating date second
    :return: 'by' part for received header
    """
    if domain:
        received_by_agent = f"{random_ascii_letters_generator(10).lower()}.{domain}"
    else:
        received_by_agent = ".".join(str(randint(0, 255)) for _ in range(4))
    if smtp_protocol:
        received_with = f"SMTP id {''.join(str(choice(ascii_lowercase + digits)) for _ in range(20))}.{randint(0, 255)}.{randint(1, 10000000)}"
    else:
        received_with = "HTTP"

    content = f"by {received_by_agent} with {received_with}; {generate_date(receiving_year, receiving_month, receiving_day, receiving_hour, receiving_minute, receiving_second)}"

    return content


def generate_received_header(header_name: str, receiving_type: str = "by", from_domain: Optional[str] = None,
                             with_ip: bool = True,
                             domain: Optional[str] = None,
                             smtp_protocol: bool = True, receiving_year: Optional[int] = None,
                             receiving_month: Optional[int] = None, receiving_day: Optional[int] = None,
                             receiving_hour: Optional[int] = None, receiving_minute: Optional[int] = None,
                             receiving_second: Optional[int] = None,
                             ) -> Header:
    """
    Generating Received header according RFC standards.

    :param header_name: email.headers.Header.header_name value
    :param receiving_type: can be 'from' or 'by'. If value is invalid or not described will be used by value.
    :param from_domain: if receiving_type is 'from' will be used in from domain generating process.
    :param with_ip: use if receiving_type is 'from',
    in generating process also will be generated random ip receiver ip.
    :param domain: will be used in generating process , if not described will be generated randomly
    :param smtp_protocol: set receiver protocol smtp or http
    :param receiving_year: generating date year
    :param receiving_month: generating date month
    :param receiving_day: generating date day
    :param receiving_hour: generating date hour
    :param receiving_minute: generating date minute
    :param receiving_second: generating date second
    :return: emaill.header.Header instance with generated values.
    """
    content = generate_receiver_by_part(domain, smtp_protocol, receiving_year, receiving_month,
                                        receiving_day, receiving_hour, receiving_minute,
                                        receiving_second)
    if receiving_type.lower() == "from":
        if not from_domain:
            raise Exception("Cannot generate received hedaer."
                            "For 'from' type should be specified from_domain property.Check logs and header.json file")
        content_from_part = f"from {random_ascii_letters_generator(10).lower()}.{from_domain}"
        if with_ip:
            content_from_part += f" ([{'.'.join(str(randint(0, 255)) for _ in range(4))}]:{randint(0, 65535)})"
        content = f"{content_from_part} {content}"
    return Header(s=content, header_name=header_name)
