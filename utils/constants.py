from os import getcwd
from os.path import join

ROOT_DIRECTORY = getcwd()
DEFAULT_CONFIGS_DIRECTORY = join(getcwd(), "settings", "defaults")
DEFAULT_HEADER_CONFIG_FILE = join(DEFAULT_CONFIGS_DIRECTORY, "headers_cfg.json")
DEFAULT_BODY_CONFIG_FILE = join(DEFAULT_CONFIGS_DIRECTORY, "body_cfg.json")
DEFAULT_SAVING_DIRECTION = join(ROOT_DIRECTORY, "generated_files")
DEFAULT_APP_CONFIG_FILE = join(DEFAULT_CONFIGS_DIRECTORY, "app_cfg.json")
DEFAULT_LOG_FILE_NAME = join(ROOT_DIRECTORY, "logger", "generator.log")
