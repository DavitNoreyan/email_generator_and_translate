from typing import Any, Type, Dict

from generator.body_generators.base_generator import BaseGenerator
from generator.body_generators.multipart_generators import GenerateMultipart
from generator.body_generators.text_ct_generator import GenerateTextBody


class BodyGenerator(BaseGenerator):
    type_handler_mapping: Dict[str, Type[BaseGenerator]] = {
        "text": GenerateTextBody,
        "multipart": GenerateMultipart
    }

    def __init__(self, generating_configs: Dict[str, Any]):
        super(BodyGenerator, self).__init__(generating_configs)


    def detect_handler(self):
        return self.type_handler_mapping.get(self.type)

    def generate(self):
        generator_class = self.detect_handler()
        generator = generator_class(self.generating_configs)
        return generator.generate()
