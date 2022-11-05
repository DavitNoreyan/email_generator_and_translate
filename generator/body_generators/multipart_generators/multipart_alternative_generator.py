# multipart alternative generator
from email.mime.multipart import MIMEMultipart
from logging import getLogger
from random import choice
from typing import List

from generator.body_generators.text_ct_generator import GenerateTextBody

logger = getLogger("info_logger")


class GenerateAlternative:
    def __init__(self, generating_configs):
        self.type = "multipart"
        self.sub_type = "alternative"
        self.text_body_generator = GenerateTextBody

        self.generating_configs = generating_configs
        self.configs = generating_configs.get("configs")
        self.charset = self.configs.get("charset")
        self.content_transfer_encoding = self.configs.get("content_transfer_encoding")
        self.plain_text_folder = self.configs.get("plain_text_folder")
        self.html_text_folder = self.configs.get("html_text_folder")
        self.language = self.configs.get("language")
        self.html_text_content = self.configs.get("html_text_content")
        self.plain_length = self.configs.get("plain_length")
        self.html_sentence_words_max_count = self.configs.get("html_sentence_words_max_count")
        self.html_tags_count = self.configs.get("html_tags_count")

    def generate_parts(self):
        # important checking that both are provided should be check using custom validator in validation process
        plain_text_generator_configs = {
            "type": "text",
            "sub_type": "plain",
            "configs": {"charset": self.charset,
                        "content_transfer_encoding": self.content_transfer_encoding,
                        }
        }
        html_text_generator_configs = {
            "type": "text",
            "sub_type": "html",
            "configs": {"charset": self.charset,
                        "content_transfer_encoding": self.content_transfer_encoding,
                        }
        }
        if self.plain_text_folder and self.html_text_folder:
            plain_text_generator_configs["configs"]["folder_path"] = self.plain_text_folder
            html_text_generator_configs["configs"]["folder_path"] = self.html_text_folder
        else:
            html_text_generator_configs["configs"]["language"] = self.language
            html_text_generator_configs["configs"]["html_tags_count"] = self.html_tags_count
            html_text_generator_configs["configs"]["html_sentence_words_max_count"] = self.html_sentence_words_max_count
            plain_text_generator_configs["configs"]["language"] = self.language
            plain_text_generator_configs["configs"]["text_length"] = self.plain_length

        plain_text_generator = self.text_body_generator(plain_text_generator_configs)
        html_text_generator = self.text_body_generator(html_text_generator_configs)
        return plain_text_generator.generate(), html_text_generator.generate()

    def generate_mime_from_parts(self, html_part, plain_part):
        mime_msg = MIMEMultipart(_subtype=self.sub_type)
        mime_msg.attach(html_part)
        mime_msg.attach(plain_part)
        return mime_msg

    def generate_for_related(self, html_content: str) -> List[MIMEMultipart]:
        plain_text_generator_configs = {
            "type": "text",
            "sub_type": "plain",
            "configs": {"charset": self.charset,
                        "content_transfer_encoding": self.content_transfer_encoding,
                        }
        }
        if self.plain_text_folder:
            plain_text_generator_configs["configs"]["folder_path"] = self.plain_text_folder
            plain_generator = self.text_body_generator(plain_text_generator_configs)
            plain_mime_parts = plain_generator.generate()
        else:
            plain_text_generator_configs["configs"]["text_length"] = self.plain_length
            plain_text_generator_configs["configs"]["language"] = self.language
            plain_generator = self.text_body_generator(plain_text_generator_configs)
            plain_mime_parts = [plain_generator.generate()]

        html_text_generator_configs = {
            "type": "text",
            "sub_type": "html",
            "configs": {"charset": self.charset,
                        "content_transfer_encoding": self.content_transfer_encoding,
                        }
        }

        html_part = self.text_body_generator(html_text_generator_configs).generate_text(html_content)
        gen_messages = []
        for plain_mime_part in plain_mime_parts:
            gen_messages.append(self.generate_mime_from_parts(html_part, plain_mime_part))
        return gen_messages

    def generate(self):
        generated_plain, generated_html = self.generate_parts()
        generated_messages = []
        if isinstance(generated_plain, list) and isinstance(generated_html, list):
            for gen_html in generated_html:
                generated_messages.append(self.generate_mime_from_parts(gen_html, choice(generated_plain)))
        else:
            generated_messages.append(self.generate_mime_from_parts(generated_html, generated_plain))
        return generated_messages
