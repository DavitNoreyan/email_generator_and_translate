from email.charset import add_charset
from logging import getLogger

from settings.config_requirements.constants import encodings_mapping

logger = getLogger("info_logger")


def change_charset_encoding(changing_charset: str, encoding: str) -> None:
    """
    Getting charset and changing its content-transfer-encoding.
    If there are errors will be logged and exception will be raised.

    :param changing_charset: charset which 'content-transfer-encoding' should be changed.
    :param encoding: encoding which should be used as new 'content-transfer-encoding' for got charset
    :return: None or raise Exception
    """
    if encoding.lower() in encodings_mapping:
        return add_charset(changing_charset, encodings_mapping[encoding], encodings_mapping[encoding])
    else:
        logger.error("Check the generator.utils.change_charset_encoding.encodings_mapping.")
        raise Exception("Encoding not supported. For more information check the logs.")
