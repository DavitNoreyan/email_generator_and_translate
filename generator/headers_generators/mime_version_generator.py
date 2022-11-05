# Generating MIme_version header

from email.header import Header
from logging import getLogger
from typing import Optional

logger = getLogger("info_logger")


def generate_mime(header_name: str, version: Optional[int] = None, subversion: Optional[int] = None) -> Header:
    """
    Generated mime version and returns email.header.Header with generated value.
    :param header_name: describes email.header.Header.header_name property
    :param version: generating mime version
    :param subversion: generating mime subversion
    :return: email.header.Header with generated mime version
    """
    if version and subversion:
        content = fr"{version}.{subversion}"
    else:
        logger.info("There is no configured version and subversion for MIME-Version , will be set 1.0 value.")
        content = "1.0"
    return Header(s=content, header_name=header_name)
