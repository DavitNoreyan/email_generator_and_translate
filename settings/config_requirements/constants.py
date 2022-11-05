from email.charset import QP, BASE64

from typing import Dict

SUPPORTED_CHARSETS = {"us-ascii",
                      "utf-8",
                      "utf-16LE",
                      "utf-16BE",
                      "utf-16",
                      "ascii",
                      "windows-1250",
                      "windows-1251",
                      "windows-1252"
                      "iso-8859-1",
                      "iso-8859-2",
                      "iso-8859-5",
                      "iso-8859-15"
                      "koi8-r",
                      "big5",
                      "GB2312",
                      "GB18030",
                      }
DEFAULT_CHARSET = "utf-8"
SUPPORTED_LANGUAGES = {
    "en",
    "fr"
}
DEFAULT_LANGUAGE = "en"
encodings_mapping: Dict[str, int] = {
    "qp": QP,
    "q": QP,
    "quoted-printable": QP,
    "base64": BASE64,
    "b": BASE64,
    "base-64": BASE64,
    "ns": None,
    "7bit": "7bit",
    "7-bit": "7bit",
    "7b": "7bit",
    "8b": "8bit",
    "8bit": "8bit"
}
SUPPORTED_ENCODINGS = encodings_mapping.keys()
DEFAULT_ENCODING = "base64"
