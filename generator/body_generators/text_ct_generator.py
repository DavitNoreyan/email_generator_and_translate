# text/plain and text/html generator
from email.mime.text import MIMEText
from logging import getLogger
from os import listdir
from os.path import exists, join
from typing import Optional

from generator.body_generators.base_generator import BaseGenerator
from generator.body_generators.random_html_generator import generate_html
from generator.utils import change_charset_encoding
from generator.utils.random_strings_generator import random_text_generator

logger = getLogger("info_logger")
SUPPORTED_SUBTYPES = ["html", "plain"]
SUPPORTED_CHARSETS = ["utf-8", "utf-16", "UTF-16LE", "utf-16be", "ascii", "windows-1250", "windows-1251",
                      "windows-1252",
                      "iso-8859-1", "iso-8859-2", "iso-8859-5"]


class GenerateTextBody(BaseGenerator):
    def __init__(self, configs):
        super(GenerateTextBody, self).__init__(configs)

    def detect_handler(self):
        if self.configs.get("folder_path"):
            return self.generate_text_from_folder

        if self.sub_type == "html":
            return self.generate_text_html

        if self.sub_type == "plain":
            return self.generate_text
        raise Exception("Cannot find sub_type for text type body.")

    def generate(self):
        handler = self.detect_handler()
        return handler()

    def generate_text(self,
                      content: Optional[str] = None) -> MIMEText:
        """
        Generating random text , encoding and setting as content for email.mime.text.MIMEText instance.
        Returns the created MIMEText instance.
        :param content: will used as content for MimeText
        :return: email.mime.text.MIMEText with got or generated content and selected options.
        """
        if self.content_transfer_encoding:
            change_charset_encoding(self.charset, self.content_transfer_encoding)
        if self.sub_type not in SUPPORTED_SUBTYPES:
            logger.error(f"{self.sub_type} for text not supported. Check body configs.")
            raise Exception("Invalid sub_type.")
        if self.charset not in SUPPORTED_CHARSETS:
            logger.error(f"{self.charset} for text not supported. Check body configs.")
            raise Exception("Invalid charset.")
        if not content:
            content = random_text_generator(self.configs.get("language"), self.configs.get("text_length"))
        return MIMEText(_text=content, _subtype=self.sub_type, _charset=self.charset)

    def generate_text_from_file(self, file_path: str) -> MIMEText:
        """
        Reading file and calling generate_text method and returns its result.
        :param file_path: file's path which content should be used as MIMEText content.
        :return: email.mime.text.MIMEText with got or generated content and selected options.
        """
        if exists(file_path):
            with open(file_path, "r") as content:
                return self.generate_text(content=content.read())
        else:
            logger.error(f"No such file {file_path} . Check the file and body configs.")
            raise Exception("Cannot find file")

    def generate_text_html(self) -> MIMEText:
        html_content = generate_html(self.configs.get("language"), self.configs.get("html_tags_count"),
                                     self.configs.get("html_sentence_words_max_count"))
        return self.generate_text(content=html_content)

    def generate_text_from_folder(self):
        folder_path = self.configs.get("folder_path")
        files = listdir(folder_path)
        if self.sub_type == "plain":
            ext = "txt"
        else:
            ext = "html"
        gen_bodies = []
        for file_name in files:
            if file_name.endswith(ext):
                gen_bodies.append(
                    self.generate_text_from_file(join(folder_path, file_name)))
        return gen_bodies
