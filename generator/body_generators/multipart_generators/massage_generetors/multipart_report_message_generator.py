import os
from email.message import Message
from email.mime.multipart import MIMEMultipart
from random import choice

import requests
from requests_toolbelt.utils import dump

import generator.body_generators.multipart_generators as multipart_generators
from generator.body_generators.multipart_generators.massage_generetors.multipart_report_message_base_generator import \
    BaseMessageGenerator
from generator.body_generators.text_ct_generator import GenerateTextBody
from generator.body_generators.text_ct_generator import random_text_generator


class GenerateReport(BaseMessageGenerator):
    def __init__(self, generating_configs):
        super().__init__(generating_configs)
        self.configs = generating_configs.get("configs")
        self.report_type = self.configs.get('report_type')
        self.charset = self.configs.get("charset")
        self.message_charset = self.configs.get("message_charset")
        self.content_transfer_encoding = self.configs.get("content_transfer_encoding")
        self.content_type = self.configs.get('content_type')
        self.plain_text_folder = self.configs.get("plain_text_folder")
        self.html_text_folder = self.configs.get("html_text_folder")
        self.image_folder = self.configs.get("image_folder")
        self.language = self.configs.get("language")
        self.plain_length = self.configs.get("plain_length")
        # self.html_text_content = self.configs.get("html_text_content")
        self.html_sentence_words_max_count = self.configs.get("html_sentence_words_max_count")
        self.html_tags_count = self.configs.get("html_tags_count")
        self.action = self.configs.get("action")
        self.body_type = self.configs.get("body_type")
        self.external_file_path = self.configs.get("external_file_path")
        self.text_content_for_message = self.configs.get("text_content_for_message")
        self.partial_files_folder = self.configs.get("partial_files_folder")
        self.max_symbols_count = self.configs.get("max_symbols_count")
        self.request_link = self.configs.get("request_link")
        self.request_headers = self.configs.get("request_headers")
        self.request_body = self.configs.get("request_body")
        self.request_method: str = self.configs.get("request_method")
        self.request_params = self.configs.get("request_params")
        self.request_part = self.configs.get("request_part")

    @staticmethod
    def get_random_action():
        action_list = ['failed', 'delayed', 'delivered', 'relayed',
                       'expanded']
        value = choice(action_list)
        return value

    def generate_message(self, content_description='Notification', content='', content_type='text/plain',
                         charset='utf-8', action=None):
        if content_type not in ['text/plain', 'text/html', 'message/delivery-status', 'message/rfc822',
                                'message/disposition-notification']:
            raise Exception('Not correct content type')
        part_of_message = Message()
        if content_description:
            part_of_message.add_header('Content_Description', content_description)
        part_of_message.set_payload(content)
        part_of_message.set_type(content_type)
        part_of_message.set_charset(self.message_charset)
        if action:
            part_of_message['Action'] = action
        return part_of_message

    def content_type_validator(self):
        valid_report_type = ['delivery-status', 'disposition-notification-to']
        if self.report_type not in valid_report_type:
            return
        if self.report_type == 'delivery-status':
            content_type = 'message/delivery-status'
        else:
            content_type = 'message/disposition-notification'
        content_description = self.report_type.replace('-', ' ')
        return content_type, content_description

    def create_message_list(self):
        valid_content_type_list = ['message/delivery-status',
                                   'message/disposition-notification-to',
                                   'message/external-body', 'message/http',
                                   'message/partial', 'message/rfc822']
        valid_sub_type_list = ['text', 'alternative', 'related']
        if self.content_type not in valid_content_type_list:
            raise Exception("Not supported conetent type")
        if self.content_type == 'message/delivery-status' or self.content_type == 'message/disposition-notification-to':
            body_type, body_sub_type = self.body_type.split("/")
            if body_sub_type not in valid_sub_type_list:
                raise Exception('not valid subtype')
            if body_sub_type == "text":
                message = GenerateTextBody({**self.generating_configs, "type": body_type, "sub_type": body_sub_type
                                            }).detect_handler().generate()

            elif body_sub_type == "related":
                message = multipart_generators.GenerateRelated(
                    {**self.generating_configs, "type": body_type, "sub_type": body_sub_type
                     }).generate()
            else:
                message = multipart_generators.GenerateAlternative(
                    {**self.generating_configs, "type": body_type, "sub_type": body_sub_type
                     }).generate()
        elif self.content_type == 'message/external-body':
            message = [self.generate_external_body_message(self.external_file_path)]
        elif self.content_type == 'message/http':
            resp = requests.request(self.request_method.upper(), self.request_link, headers=self.request_headers,
                                    data=self.request_body, params=self.request_params)
            data = dump.dump_all(resp)
            full_request = data.decode('utf-8')
            req_res_dividing_index = full_request.find("\n>")

            msg = Message()
            msg.add_header('Content-type', 'message/http')
            if self.request_part == "request":
                msg.set_payload(full_request[:req_res_dividing_index])
            else:
                msg.set_payload(full_request[req_res_dividing_index:])
            message = [msg]
        elif self.content_type == 'message/partial':
            message = self.partial_generator(self.partial_files_folder, self.max_symbols_count)
        else:
            content = self.create_text_content_for_message()
            message = [self.generate_rfc_822_message(content)]
        return message

    def generate_rfc_822_message(self, content):
        message = Message()
        message.add_header('Content-type', 'message/rfc822')
        message.set_payload(content)
        return message

    @staticmethod
    def generate_partial_part(part_number: int, parts_count: int, content: str):
        msg = Message()
        msg.set_payload(content)
        msg.add_header("Content-Type", "message/partial", number=str(part_number), total=str(parts_count))
        return msg

    def partial_generator(self, folder: str, max_symbols_count: int):
        messages = []
        files = os.listdir(folder)
        for file_path in files:
            with open(os.path.join(folder, file_path), "r") as file:
                content = file.read()
            parts_count: int = int(len(content) / max_symbols_count) + 1
            for part_number in range(1, parts_count + 1):
                part = self.generate_partial_part(part_number, parts_count, content[(
                                                                                            part_number - 1) * max_symbols_count:part_number * max_symbols_count])
                messages.append(part)
        return messages

    def create_text_content_for_message(self):
        if self.plain_text_folder:
            list_of_file_names = os.listdir(self.plain_text_folder)
            list_of_file_paths = [os.path.join(self.plain_text_folder, name) for name in list_of_file_names]
            path = choice(list_of_file_paths)
            with open(path, 'r') as f:
                content = f.read()
        else:
            content = random_text_generator(self.language, self.plain_length)
        return content

    def generate_external_body_message(self, path):
        message = Message()
        message.set_payload('')
        message.add_header('Content-type', 'message/external-body')
        message.add_header('access-type', 'local-file', name=f'{path}')
        return message

    @staticmethod
    def create_file_list_from_folder_path(path):
        list_of_file_names = os.listdir(path)
        list_of_file_paths = [os.path.join(path, name) for name in list_of_file_names]
        return list_of_file_paths

    def generate(self):
        content_list = self.create_message_list()
        all_message_list = []
        action = self.action if self.action else self.get_random_action()
        if self.report_type == "disposition-notification-to" or self.report_type == "delivery-status":
            content_type, content_description = self.content_type_validator()
        else:
            content_type, content_description = None, None
        for message_content in content_list:
            if self.report_type == "disposition-notification-to" or self.report_type == "delivery-status":
                root_mail = MIMEMultipart(_subtype=self.subtype, report_type=self.report_type)
            else:
                root_mail = MIMEMultipart(_subtype=self.subtype)
            if self.content_type == 'message/delivery-status':
                message_content["Action"] = action
            root_mail.attach(message_content)
            if self.report_type == "disposition-notification-to" or self.report_type == "delivery-status":
                description_part = self.generate_message(content_description=content_description,
                                                         content_type=content_type, charset=self.message_charset)
                root_mail.attach(description_part)
            all_message_list.append(root_mail)
        return all_message_list
