import os
from pathlib import Path

from deep_translator import GoogleTranslator


class Translator:
    def __init__(self, path: str, target: str = 'fr', length: int = 4000):
        """
        This is the constructor for the Translator class.
        :param path: is the path of the file or directory where the files for translation are located
        :param target: is the target language to which the text should be translated
        """
        self.path = path
        self.source = 'auto'
        self.target = target
        self.length = length
        self.translate = GoogleTranslator(source=self.source, target=self.target)

    def path_parser(self) -> list:
        """
        This is a function to parse the path of a directory or file
        :return:
        """
        list_files_path_for_translate = []
        if Path(self.path).is_dir():
            list_files_for_translate = os.listdir(self.path)
            for file_name in list_files_for_translate:
                list_files_path_for_translate.append(os.path.join(self.path, file_name))
        elif Path(self.path).is_file():
            list_files_path_for_translate = [self.path]
        return list_files_path_for_translate

    def split_text(self, text: str) -> list:
        """
        this is a function for parsing text for translation
        :param text: this is the text that will be parsed
        :return:
        """
        list_for_translate = []
        end_index = self.length
        while True:
            if len(text) < self.length:
                list_for_translate.append(text)
                break
            work_text = text[:end_index]
            index_dot = work_text.rfind('.')
            index_new_line = work_text.rfind('\n')
            if index_dot > index_new_line:
                index = index_dot
            else:
                index = index_new_line
            text_for_translate = text[:index]
            list_for_translate.append(text_for_translate)
            text = text[index:]
        return list_for_translate

    def translate_text(self):
        """
        function for translating text,
        then the function writes the translated text to the document in the folder of the original document
        :return:
        """
        file_list = self.path_parser()
        for file in file_list:
            with open(file, 'r') as fl:
                txt = fl.read()
            text_list = self.split_text(txt)
            self.translate.translate_batch(text_list)
            translated_text = ''.join(self.translate.translate_batch(text_list))
            new_file_path = file.replace(f'{Path(file).name}', f'{self.target}-{Path(file).name}')
            with open(new_file_path, 'w') as wf:
                wf.write(translated_text)
