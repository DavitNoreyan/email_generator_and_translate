# generate multipart/mixed
import os
from email.mime.multipart import MIMEMultipart
from logging import getLogger

from generator.body_generators.attachements_handler import create_attachments
from generator.body_generators.multipart_generators.multipart_alternative_generator import GenerateAlternative
from generator.body_generators.multipart_generators.multipart_related_generator import GenerateRelated
from generator.body_generators.text_ct_generator import GenerateTextBody

logger = getLogger("info_logger")


class GenerateMixed:
    def __init__(self, generating_configs):
        self.type = "multipart"
        self.sub_type = "mixed"
        self.text_body_generator = GenerateTextBody
        self.generating_configs = generating_configs
        self.configs = generating_configs.get("configs")
        self.charset = self.configs.get("charset")
        self.content_transfer_encoding = self.configs.get("content_transfer_encoding")
        self.plain_text_folder = self.configs.get("plain_text_folder")
        self.html_text_folder = self.configs.get("html_text_folder")
        self.image_folder = self.configs.get('image_folder')  # TODO
        self.language = self.configs.get("language")
        self.html_doc_path = self.configs.get('')  # TODO
        self.html_tag_count = self.configs.get("html_tags_count")
        self.html_sentence_words_max_count = self.configs.get("html_sentence_words_max_count")
        self.plain_length = self.configs.get('plain_length')
        self.attachments_folder = self.configs.get('attachments_folder')
        self.image_file_ex = ['.jpeg', '.jpg', '.png', '.gif', 'tiff', '.tiff', '.psd', '.pdf', '.esp', '.al', '.indd',
                              '.cr2', '.crw', '.nef', '.pef']
        self.html_file_ex = ['.html']
        self.text_file_ex = ['.txt']

    @staticmethod
    def attach_file_path_list(folder_path: str):
        file_name_list = os.listdir(folder_path)
        file_path_list = [os.path.join(folder_path, name) for name in file_name_list]
        return file_path_list

    def generate(self):
        message_list = []
        if self.image_folder or self.html_text_folder:
            root_message_list = GenerateRelated(self.generating_configs).generate()
        elif (self.plain_text_folder and self.html_text_folder) or (
                self.plain_text_folder and self.html_sentence_words_max_count and self.html_tag_count) or (
                self.html_text_folder and self.plain_length):
            root_message_list = GenerateAlternative(self.generating_configs).generate()
        elif self.plain_text_folder or self.html_text_folder:
            if self.html_text_folder:
                root_message_list = [GenerateTextBody({**self.generating_configs, 'sub_type': 'html'}).generate()]
            else:
                root_message_list = [GenerateTextBody({**self.generating_configs, 'sub_type': 'plain'}).generate()]
        elif self.html_tag_count and self.html_sentence_words_max_count:
            root_message_list = [GenerateTextBody({**self.generating_configs, 'sub_type': 'html'}).generate_text_html()]
        elif self.plain_length:
            root_message_list = [GenerateTextBody({**self.generating_configs, 'sub_type': 'plain'}).generate_text()]
        else:
            logger.error("Invalid properties for multipart/mixed generation. Not enough data for body generation.")
            raise Exception("Invalid defaults")
        attach_file_list = self.attach_file_path_list(self.attachments_folder)
        created_attachments = create_attachments(attach_file_list)
        for massage in root_message_list:
            root_message = MIMEMultipart(_subtype=self.sub_type)
            for attachment in created_attachments:
                massage.attach(attachment)
            root_message.attach(massage)
            message_list.append(root_message)
        return message_list
