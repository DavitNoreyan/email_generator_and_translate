from generator.body_generators.base_generator import BaseGenerator
from generator.body_generators.multipart_generators.massage_generetors.multipart_report_message_generator import \
    GenerateReport
from generator.body_generators.multipart_generators.multipart_alternative_generator import GenerateAlternative
from generator.body_generators.multipart_generators.multipart_mixed_generator import GenerateMixed
from generator.body_generators.multipart_generators.multipart_related_generator import GenerateRelated


class GenerateMultipart(BaseGenerator):
    sub_type_handler_mapping = {
        "alternative": GenerateAlternative,
        "related": GenerateRelated,
        "mixed": GenerateMixed,
        "report": GenerateReport
    }

    def __init__(self, configs):
        super(GenerateMultipart, self).__init__(configs)

    def detect_handler(self):
        return self.sub_type_handler_mapping.get(self.sub_type)

    def generate(self):
        handler_class = self.detect_handler()
        handler = handler_class(self.generating_configs)
        return handler.generate()
