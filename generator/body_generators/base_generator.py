from abc import abstractmethod
from typing import Any, Dict


class BaseGenerator:
    def __init__(self, generating_configs: Dict[str, Any]):
        self.type = generating_configs.get("type")
        self.sub_type = generating_configs.get("sub_type")
        self.configs = generating_configs.get("configs")
        self.generating_configs = generating_configs
        self.charset = self.configs.get("charset")
        self.content_transfer_encoding = self.configs.get("content_transfer_encoding")
        self.report_type = self.configs.get("report_type")

    @abstractmethod
    def generate(self):
        ...

    @abstractmethod
    def detect_handler(self):
        ...
