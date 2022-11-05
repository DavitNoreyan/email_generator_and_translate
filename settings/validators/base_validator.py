from abc import abstractmethod
from logging import getLogger
from os.path import exists

from utils.read_json import get_json_data

logger = getLogger("info_logger")


class BaseValidator:
    def __init__(self, cfg_file_path):
        if not exists(cfg_file_path):
            logger.error(f"{cfg_file_path} not existing. CHeck configurations.")
            raise Exception("Cannot find cfg file.")
        self.configs = get_json_data(cfg_file_path)

    @abstractmethod
    def check_contains_valid_options(self):
        ...

    @abstractmethod
    def check_custom_validators(self):
        ...

    def validate(self):
        self.check_contains_valid_options()
        self.check_custom_validators()
        return self.configs
