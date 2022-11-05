import os.path
from email.generator import Generator
from email.message import EmailMessage
from os import mkdir
from os.path import exists
from typing import Optional, Type, List
from uuid import uuid4

from settings.validators import validate_headers_configs, ValidateBodyConfigs
from .body_generators.body_generators import BodyGenerator
from .headers_generators import HEADERS_GENERATORS_MAPPER


class EmailGenerator:
    def __init__(self, configs):
        # todo write documentation
        self.headers_cfg_path = configs.get("headers_cfg")
        self.body_cfg_path = configs.get("body_cfg")
        self.saving_direction = configs.get("saving_direction")
        self.generated_emails: Optional[List[EmailMessage]] = []
        self.generating_headers_configurations = None
        self.generating_body_configurations = None
        self.body_validator = ValidateBodyConfigs(self.body_cfg_path)
        self.body_generator: Optional[Type[BodyGenerator]] = None

    def setup(self):
        # todo write docs
        if not exists(self.saving_direction):
            mkdir(self.saving_direction)
        self.generating_headers_configurations = validate_headers_configs(self.headers_cfg_path)
        self.generating_body_configurations = self.body_validator.validate()
        self.body_generator = BodyGenerator(self.generating_body_configurations)

    def initialize_generation_properties(self):
        ...

    def generate_headers(self):
        # todo add documentation
        generating_headers_list: List[str] = self.generating_headers_configurations.get("headers").keys()
        emails_headers_dict = {}
        for header_name in generating_headers_list:
            header_gen_kwargs = self.generating_headers_configurations.get("headers").get(header_name)
            gen_header = HEADERS_GENERATORS_MAPPER.get(header_name)(
                **{"header_name": header_name,
                   **header_gen_kwargs})
            emails_headers_dict[header_name] = gen_header
        return emails_headers_dict

    def generate_body(self):
        # todo write docs
        # important move to separate file
        # important optimize if else
        # todo on changing body gen allow only one type properties html/plain
        gen_body = self.body_generator.generate()
        return gen_body

    def generate_emails(self):
        # todo finalize docs
        """
        Getting generation configurations and generating email.
        If there are missed configurations will be used default configurations.
        :return:
        """
        generated_headers = self.generate_headers()
        msg = self.generate_body()
        if isinstance(msg, list):
            for message in msg:
                for header in generated_headers:
                    message[header] = generated_headers[header]
                self.generated_emails.append(message)
        else:
            for header in generated_headers:
                msg[header] = generated_headers[header]
            self.generated_emails = [msg]
        self.save_to_file()

    def save_to_file(self):
        # todo write docs
        # todo change the saving functionality
        for msg in self.generated_emails:
            outfile_name = rf"{uuid4()}.eml"
            outfile_name_path = os.path.join(self.saving_direction, outfile_name)
            with open(outfile_name_path, 'w') as outfile:
                gen = Generator(outfile)
                gen.flatten(msg)
