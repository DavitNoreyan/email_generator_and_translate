from logging import getLogger
from typing import Any, Dict, List

from settings.config_requirements.body import TYPE_SUB_TYPE_REQUIREMENTS_MAPPING
from settings.validators.base_validator import BaseValidator

logger = getLogger("info_logger")


class ValidateBodyConfigs(BaseValidator):
    requirements = TYPE_SUB_TYPE_REQUIREMENTS_MAPPING

    def __init__(self, cfg_file_path):
        super(ValidateBodyConfigs, self).__init__(cfg_file_path)
        if "type" not in self.configs or "sub_type" not in self.configs:
            logger.error(f"Should be specified type and sub_type for generating message. Check the {cfg_file_path}")
            raise Exception("Body type not specified.")
        if "configs" not in self.configs:
            logger.error(f"Should be specified configs for generating message. Check the {cfg_file_path}")
            raise Exception("Invalid body configs.")
        self.body_spec = self.configs.get("configs")
        self.type = self.configs.get("type")
        self.sub_type = self.configs.get("sub_type")
        if self.type not in self.requirements:
            logger.error(f"{self.type} not supported yet. Supported types are: {self.requirements.keys()}."
                         f"Check the {cfg_file_path}.")
            raise Exception("Not supported body type.")
        if self.sub_type not in self.requirements.get(self.type):
            if "any" in self.requirements.get(self.type):
                self.sub_type = "any"
            else:
                raise Exception("Not supported body sub_type.")
        self.body_configs_requirements = self.requirements.get(self.type).get(self.sub_type)

    @staticmethod
    def check_contains_required_arguments(initial_configs: Dict[str, Any], requirements: List[str]):
        cleaned_configs: Dict[str, Any] = {}
        for req_arg in requirements:
            if req_arg not in initial_configs:
                logger.error(f"Should be specified {req_arg}. Check configurations.")
                raise Exception("Invalid configs")
            cleaned_configs[req_arg] = initial_configs.get(req_arg)
        return cleaned_configs

    @staticmethod
    def check_contains_optional_arguments(initial_configs: Dict[str, Any], optional_args: List[str]):
        cleaned_args: Dict[str, Any] = {}
        for arg in initial_configs:
            if arg in optional_args:
                cleaned_args[arg] = initial_configs[arg]
        return cleaned_args

    def check_contains_valid_options(self):
        cleaned_configs = {**self.check_contains_required_arguments(self.body_spec,
                                                                    self.body_configs_requirements.get("required")),
                           **self.check_contains_optional_arguments(self.body_spec,
                                                                    self.body_configs_requirements.get("optional"))
                           }
        self.body_spec = cleaned_configs
        self.configs["configs"] = cleaned_configs

    def check_custom_validators(self):
        if "custom_validator" not in self.body_configs_requirements:
            return None
        for custom_validator_properties in self.body_configs_requirements["custom_validator"]:
            custom_validator = custom_validator_properties[0]
            if callable(custom_validator):
                custom_validator(self.body_spec, *custom_validator_properties[1: len(custom_validator_properties)])
