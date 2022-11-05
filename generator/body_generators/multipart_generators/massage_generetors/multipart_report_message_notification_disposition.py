from email.message import Message

from generator.body_generators.multipart_generators.massage_generetors.multipart_report_message_base_generator import \
    BaseMessageGenerator


class GenerateNotificationDisposition(BaseMessageGenerator):
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
        self.language = self.configs.get("language")
        self.plain_length = self.configs.get("plain_length")
        self.html_text_content = self.configs.get("html_text_content")
        self.html_sentence_words_max_count = self.configs.get("html_sentence_words_max_count")
        self.html_tags_count = self.configs.get("html_tags_count")

    def generate_message(self, content, content_type, charset):
        if content_type not in ['text/plain', 'text/html', 'message/notification-disposition']:
            raise Exception('Not correct content type')
        part_of_message = Message()
        part_of_message.set_payload(content)
        part_of_message.set_type(content_type)
        part_of_message.set_charset(charset)
        return part_of_message
