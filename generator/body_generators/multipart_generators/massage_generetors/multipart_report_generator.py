import os.path
from email.message import Message
from email.mime.multipart import MIMEMultipart
from logging import getLogger

from generator.body_generators.random_html_generator import generate_html
from generator.body_generators.text_ct_generator import GenerateTextBody
from generator.utils.random_strings_generator import random_text_generator

logger = getLogger("info_logger")


class GenerateMultipartReport:
    REPORT_TYPE_LIST = ["disposition-notification", "delivery-status"]

    def __init__(self, generating_configs):
        self.type = "multipart"
        self.sub_type = "report"
        self.text_body_generator = GenerateTextBody
        self.generating_configs = generating_configs
        self.configs = generating_configs.get("configs")
        self.charset = self.configs.get("charset")
        self.message_charset = self.configs.get("message_charset")
        self.content_transfer_encoding = self.configs.get("content_transfer_encoding")
        self.report_type = self.configs.get("report_type")
        self.plain_text_folder = self.configs.get("plain_text_folder")
        self.html_text_folder = self.configs.get("html_text_folder")
        self.language = self.configs.get("language")
        self.html_doc_path = self.configs.get('')
        self.html_tag_count = self.configs.get("html_tags_count")
        self.html_sentence_words_max_count = self.configs.get("html_sentence_words_max_count")
        self.plain_length = self.configs.get('plain_length')
        self.html_file_ex = ['.html']
        self.text_file_ex = ['.txt']

    def generate_configs(self, file_type_in_folder):
        file_type_list = ["plain", "html"]
        if file_type_in_folder not in file_type_list:
            raise Exception('not correct subtype')
        plain_text_generator_configs = {
            "type": "text",
            "sub_type": "plain",
            "configs": {"charset": self.charset,
                        "content_transfer_encoding": self.content_transfer_encoding,
                        "folder_path": self.plain_text_folder
                        }
        }
        html_text_generator_configs = {
            "type": "text",
            "sub_type": "html",
            "configs": {"charset": self.charset,
                        "content_transfer_encoding": self.content_transfer_encoding,
                        }
        }
        if file_type_in_folder == 'plain':
            return plain_text_generator_configs
        else:
            return html_text_generator_configs

    def create_message(self, message: Message, content: dict) -> Message:
        for cont in content.keys():
            message.set_payload(content.get(cont))
            if cont == 'plain_text_content':
                message.set_type('text/plain')
                message.set_charset(self.message_charset)
            elif cont == 'html_text_content':
                message.set_type('text/html')
                message.set_charset(self.message_charset)
        return message

    def create_notification_or_delivery_message(self, message: Message, content: list):
        for cont in content:
            message.set_payload(cont)
        message['Content-Transfer-Encoding'] = self.content_transfer_encoding
        message.set_type(self.report_type)
        message.set_charset(self.charset)
        return message

    def generate_content_for_disposition_notification(self):
        if self.plain_text_folder:
            config_for_plain_generate = self.generate_configs('plain')
            config_for_plain_generate["configs"]["folder_path"] = self.plain_text_folder
            plain_text_content = self.text_body_generator(
                config_for_plain_generate).generate_text_from_folder()
        elif self.plain_length and not self.plain_text_folder:
            config_for_plain_generate = self.generate_configs('plain')
            config_for_plain_generate["configs"]["language"] = self.language
            config_for_plain_generate["configs"]["text_length"] = self.plain_length
            plain_text_content = self.text_body_generator(config_for_plain_generate).generate_text()
        else:
            raise Exception('')
        return plain_text_content

    def open_text_file_from_folder(self, path):
        list_of_file_names = os.listdir(path)
        list_of_file_paths = [os.path.join(path, name) for name in list_of_file_names]
        text = ''
        for fl in list_of_file_paths:
            with open(fl) as file:
                txt = file.read()
                text += txt
        return u'{}'.format(text)

    def generate(self):
        root_report = MIMEMultipart(_subtype=self.sub_type, report_type=self.report_type)
        if self.html_text_folder or (self.html_tag_count or self.html_sentence_words_max_count):
            if self.html_text_folder:
                if self.plain_text_folder or self.plain_length:
                    if self.plain_text_folder:
                        plain_text_content = self.open_text_file_from_folder(self.plain_text_folder)
                        html_text_content = self.open_text_file_from_folder(self.html_text_folder)
                        content = {
                            'plain_text_content': plain_text_content,
                            'html_text_content': html_text_content
                        }
                    else:
                        html_text_content = self.open_text_file_from_folder(self.html_text_folder)
                        plain_text_content = random_text_generator(self.language, self.plain_length)

                        content = {
                            'plain_text_content': plain_text_content,
                            'html_text_content': html_text_content
                        }
                else:
                    html_text_content = self.open_text_file_from_folder(self.html_text_folder)
                    content = {
                        'html_text_content': html_text_content
                    }
            else:
                if self.plain_text_folder or self.plain_length:
                    if self.plain_text_folder:
                        html_text_content = generate_html(self.language, self.html_tag_count,
                                                          self.html_sentence_words_max_count)
                        plain_text_content = self.open_text_file_from_folder(self.plain_text_folder)

                        content = {
                            'plain_text_content': plain_text_content,
                            'html_text_content': html_text_content
                        }
                    else:
                        plain_text_content = random_text_generator(self.language, self.plain_length)
                        html_text_content = generate_html(self.language, self.html_tag_count,
                                                          self.html_sentence_words_max_count)
                        content = {
                            'plain_text_content': plain_text_content,
                            'html_text_content': html_text_content
                        }
        elif not self.html_text_folder and not self.html_tag_count and not self.html_sentence_words_max_count and (
                self.plain_text_folder or self.plain_length):
            if self.plain_text_folder:
                plain_text_content = self.open_text_file_from_folder(self.plain_text_folder)
                content = {
                    'plain_text_content': plain_text_content
                }
            else:
                plain_text_content = random_text_generator(self.language, self.plain_length)
                content = {
                    'plain_text_content': plain_text_content,
                }
        else:
            raise Exception()
        message = Message()
        root_message = self.create_message(message, content)
        root_message_cont = self.open_text_file_from_folder(self.plain_text_folder)
        root_confirm_message = self.create_notification_or_delivery_message(message, root_message_cont)
        root_report.attach(root_message)
        root_report.attach(root_confirm_message)

        return [root_report]
