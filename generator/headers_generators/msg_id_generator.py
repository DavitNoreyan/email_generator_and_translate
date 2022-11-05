# Generate msg_id and multiple msg_ides

from email.header import Header
from email.utils import make_msgid
from typing import Optional


def generate_message_id(header_name: str, idstring: Optional[str] = None, domain: Optional[str] = None) -> Header:
    """
    Generating unique message id for got domain.
    :param header_name: describes email.header.Header.header_name property
    :param idstring: will be used in msg_generating process
    :param domain: will be used in msg_generating process
    :return: email.header.Header instance with generated msg_id
    """
    msg_id = make_msgid(idstring=idstring, domain=domain)
    return Header(s=msg_id, header_name=header_name)


def bulk_msg_id_generator(header_name: str, idstring: str = None, domain: str = None, count: int = None) -> Header:
    """
    Generating unique message ides for got domain.
    :param header_name: describes email.header.Header.header_name property
    :param idstring: will be used in msg_generating process
    :param domain: will be used in msg_generating process
    :param count: generating msg_ides count
    :return: email.header.Header instance with generated msg_ides
    """
    msg_ides = " ".join([make_msgid(idstring=idstring, domain=domain) for _ in range(count)])
    return Header(s=msg_ides, header_name=header_name)
