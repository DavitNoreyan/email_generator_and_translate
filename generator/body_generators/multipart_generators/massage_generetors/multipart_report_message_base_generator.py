import os
from abc import abstractmethod


class BaseMessageGenerator:
    def __init__(self, generating_configs):
        self.subtype = 'report'
        self.generating_configs = generating_configs
        self.report_type = self.generating_configs.get('configs').get('report_type')

    @staticmethod
    def open_text_file_from_folder(path):
        list_of_file_names = os.listdir(path)
        list_of_file_paths = [os.path.join(path, name) for name in list_of_file_names]
        text = ''
        for fl in list_of_file_paths:
            with open(fl, 'r') as file:
                txt = file.read()
                text += txt
        return u'{}'.format(text)

    @abstractmethod
    def generate_message(self, *args):
        ...

    @abstractmethod
    def generate(self, *args):
        ...
