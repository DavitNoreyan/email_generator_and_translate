# multipart/relative generator
import os.path
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import getLogger
from os.path import splitext, exists
from typing import Optional, List, Dict, Tuple
from uuid import uuid4

from generator.body_generators.multipart_generators.multipart_alternative_generator import GenerateAlternative
from generator.body_generators.random_html_generator import generate_html
from generator.body_generators.text_ct_generator import GenerateTextBody

logger = getLogger("info_logger")


class GenerateRelated:
    def __init__(self, generating_configs):
        self.type = "multipart"
        self.sub_type = "related"
        self.text_body_generator = GenerateTextBody
        self.generating_configs = generating_configs
        self.configs = generating_configs.get("configs")
        self.charset = self.configs.get("charset")
        self.content_transfer_encoding = self.configs.get("content_transfer_encoding")
        self.plain_text_folder = self.configs.get("plain_text_folder")
        self.html_text_folder = self.configs.get("html_text_folder")
        self.image_folder = self.configs.get('image_folder')
        self.language = self.configs.get("language")
        self.html_tag_count = self.configs.get("html_tags_count")
        self.html_sentence_words_max_count = self.configs.get("html_sentence_words_max_count")
        self.plain_length = self.configs.get('plain_length')
        self.image_file_ex = ['.jpeg', '.jpg', '.png', '.gif', 'tiff', '.tiff', '.psd', '.pdf', '.esp', '.al', '.indd',
                              '.cr2', '.crw', '.nef', '.pef']
        self.html_file_ex = ['.html']
        self.text_file_ex = ['.txt']

    @staticmethod
    def file_paths_list_creator(file_ex: List[str], folder_path: str) -> list:
        """
            Getting direction and required extensions , listing all files in got direction ,
            filtering and returning file's absolute paths.
        :param file_ex: required extension
        :param folder_path: searching directory
        :return: absolute paths list
        """
        file_path_list = []
        file_name_list = os.listdir(folder_path)
        for name in file_name_list:
            extension = os.path.splitext(name)[1]
            if extension in file_ex:
                file_path_list.append(os.path.join(folder_path, name))
        return file_path_list

    @staticmethod
    def html_image_paths_extractor(content: str) -> list:
        # todo write docs
        img_paths = []
        searching_start_index = 0
        while searching_start_index < len(content):
            img_tag_index = content.find("img", searching_start_index)
            if img_tag_index == -1:
                break
            path_starting_index = content.find("src=", img_tag_index) + 5
            path_ending_index = content.find(content[path_starting_index - 1], path_starting_index)
            if exists(content[path_starting_index:path_ending_index]):
                img_paths.append(content[path_starting_index:path_ending_index])
            searching_start_index = path_ending_index
        return img_paths

    @staticmethod
    def replace_html_paths_to_cid(content: str, image_path_id_mapping: Dict[str, str]) -> str:
        # todo write docs
        # { cid:path }
        for cid in image_path_id_mapping:
            content = content.replace(image_path_id_mapping[cid], f"cid:{cid}", 1)
        return content

    @staticmethod
    def attache_inline_images(root_message: MIMEMultipart, cid_image_path_mapping: Dict[str, str]) -> None:
        # todo write docs
        for c_id in cid_image_path_mapping:
            image_path = cid_image_path_mapping[c_id]
            if exists(image_path):
                with open(image_path, "rb") as image_data:
                    image_bytes: bytes = image_data.read()
                    image = MIMEImage(_imagedata=image_bytes, _subtype=splitext(image_path)[1][1:])
                    image.add_header('Content-ID', c_id)
                    image.add_header('Content-Disposition', "inline")
                    root_message.attach(image)
            else:
                logger.error(f"Cannot find with {image_path} path.")
        return None

    @staticmethod
    def image_cid_generator(image_paths_list) -> Dict[str, str]:
        # todo  write docs
        image_cid_paths_mapping = {}
        for image_path in image_paths_list:
            image_cid_paths_mapping[str(uuid4())] = image_path
        return image_cid_paths_mapping

    # todo change the name to path or something like that ( we dont use links!! )
    def html_content_creator_from_path(self, html_path_list: list) -> list:
        # todo poxel grel folderi logika
        html_content_list = []
        for html_path in html_path_list:
            with open(html_path) as html_file:
                html_content_for_parse = html_file.read()
                image_paths = self.html_image_paths_extractor(html_content_for_parse)
                image_path_id_mapping = self.image_cid_generator(image_paths)
                html_content = self.replace_html_paths_to_cid(html_content_for_parse, image_path_id_mapping)
                html_content_list.append((html_content, image_path_id_mapping))
        return html_content_list

    def generate_single_multipart_related(self, html_content_tuple: Optional[tuple] = None,
                                          image_paths: Optional[List[str]] = None) -> MIMEMultipart:
        if not image_paths:
            if html_content_tuple:
                html_content, image_path_id_mapping = html_content_tuple
            else:
                logger.error("image_paths and  html_file_path not specified."
                             "For generating multipart/relative provide one of them.")
                raise Exception("Invalid arguments.")
        else:
            path_list = self.file_paths_list_creator()
            image_path_id_mapping = self.image_cid_generator(path_list)
            html_content = generate_html(self.language,
                                         self.html_tag_count,
                                         self.html_sentence_words_max_count,
                                         image_path_id_mapping)
        if self.plain_text_folder or self.plain_length:
            related_content = GenerateAlternative(generating_configs=self.generating_configs)
            related_messages = related_content.generate_for_related(html_content_tuple[0])
        else:
            related_content = GenerateTextBody({**self.generating_configs, 'sub_type': 'html'})
            related_content = related_content.generate_text(html_content)
        for related_message in related_messages:
            root_message = MIMEMultipart(_subtype=self.sub_type)
            root_message.attach(related_message)
            self.attache_inline_images(root_message, image_path_id_mapping)
        return root_message

    def generate_html_body_and_cid(self) -> Tuple[str, Dict[str, str]]:
        """
            Generating content ides , and after generating html using the cids.
            Returning tuple , which the first item is generated html , the second c_id-paths mapping dict
        :return: ( gen_html_content_str , cid_abs_path_mapping_dict )
        """
        image_paths = self.file_paths_list_creator(self.image_file_ex, self.image_folder)
        image_cid_mapping = self.image_cid_generator(image_paths)
        generated_html = generate_html(self.language, self.html_tag_count, self.html_sentence_words_max_count,
                                       image_cid_mapping)
        return generated_html, image_cid_mapping

    def read_htmls_from_folder(self) -> List[Tuple[str, Dict[str, str]]]:
        """
            Getting files from self.html_text_folder folder , reading content , generating c_ides for inline images,
            replacing file paths ith generated content ides and returning tuple with content and mapping.
        :return: [ ( html_content , content_id_path_mapping ) , ... ]
        """
        html_and_cid_mapping_list = []
        paths = self.file_paths_list_creator(self.html_file_ex, self.html_text_folder)
        for path in paths:
            with open(path) as html_file:
                html_file_content = html_file.read()
                inline_image_paths = self.html_image_paths_extractor(html_file_content)
                cid_image_mapping = self.image_cid_generator(inline_image_paths)
                html_file_content = self.replace_html_paths_to_cid(html_file_content, cid_image_mapping)
                html_and_cid_mapping_list.append((html_file_content, cid_image_mapping))
        return html_and_cid_mapping_list

    def generate_or_read_html_body(self) -> List[Tuple[str, Dict[str, str]]]:
        """
            Checking self.html_text_folder property if got then reading and parsing,
            modifying and returning the files content.
            Otherwise generating html content using images from self.image_folder direction.
        :return: [ ( html_content , c_id_path_mapping ) , ...  ]
        """
        if not self.html_text_folder:
            return [self.generate_html_body_and_cid()]
        return self.read_htmls_from_folder()

    def generate_with_html_body(self) -> List[Tuple[MIMEText, Dict[str, str]]]:
        """
            Generating html body , after creating MIMEText with html subtype , and returning
        :return: [(MIMEText( generated_html ) , cid_abs_path_mapping ) , ... ]
        """
        bodies = self.generate_or_read_html_body()
        mime_bodies = []
        for body_configs in bodies:
            mime_bodies.append(
                (MIMEText(_text=body_configs[0], _subtype="html", _charset=self.charset), body_configs[1]))
        return mime_bodies

    def generate_with_alternative_body(self) -> List[Tuple[MIMEMultipart, Dict[str, str]]]:
        html_contents = self.generate_or_read_html_body()
        mime_bodies = []
        for html_content_info in html_contents:
            generated_alternatives = GenerateAlternative(
                generating_configs=self.generating_configs).generate_for_related(html_content_info[0])
            for generated_alternative in generated_alternatives:
                mime_bodies.append((generated_alternative, html_content_info[1]))
        return mime_bodies

    def detect_body_type_handler(self):
        """
            Checking configs and returning generator.
            Can be 2 cases: html or Alternative.
            In case if described properties for plain text will be generated alternative body with inline images.
        :return: mime generator function
        """
        if self.plain_text_folder or self.plain_length:
            return self.generate_with_alternative_body
        return self.generate_with_html_body

    def generate(self):
        body_sub_part_generator = self.detect_body_type_handler()
        generated_bodies = body_sub_part_generator()
        root_message_list = []
        for generated_body in generated_bodies:
            root_message = MIMEMultipart(_subtype=self.sub_type)
            root_message.attach(generated_body[0])
            self.attache_inline_images(root_message, generated_body[1])
            root_message_list.append(root_message)
        return root_message_list
