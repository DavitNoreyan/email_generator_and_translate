from datetime import datetime
from email.header import Header
from email.utils import format_datetime
from logging import getLogger
from typing import Optional

logger = getLogger("info_logger")


def generate_date(year: Optional[int] = None, month: Optional[int] = None, day: Optional[int] = None,
                  hour: Optional[int] = None, minute: Optional[int] = None, second: Optional[int] = None):
    """
    Generating date with got arguments.
    If there are mistakes or errors in arguments will be returned datetime now and will be logged alert for user.
    :param year: generating date year
    :param month: generating date month
    :param day: generating date day
    :param hour: generating date hour
    :param minute: generating date minute
    :param second: generating date second
    :return: date with got parameters or date now.
    """
    if year and month and day and hour and second:
        try:
            email_date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        except Exception as e:
            logger.warning(e)
            email_date = datetime.now()
    else:
        email_date = datetime.now()
    return format_datetime(email_date)


def generate_date_header(header_name: str, year: Optional[int] = None, month: Optional[int] = None,
                         day: Optional[int] = None, hour: Optional[int] = None, minute: Optional[int] = None,
                         second: Optional[int] = None) -> Header:
    """

    Generating date with got arguments and returning email.headers.Header instance with generated value.
    :param header_name: will be set as header_name property for email.headers.Header instance
    :param year: generating date year
    :param month: generating date month
    :param day: generating date day
    :param hour: generating date hour
    :param minute: generating date minute
    :param second: generating date second
    :return: email.headers.Header with generated date
    """
    content = generate_date(year, month, day, hour, minute, second)
    return Header(s=content, header_name=header_name)
