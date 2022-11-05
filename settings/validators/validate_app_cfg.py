from os import environ
from os.path import exists
from typing import Any, Dict

from settings.utils.logger import configure_logger
from utils.constants import DEFAULT_APP_CONFIG_FILE, DEFAULT_SAVING_DIRECTION
from utils.constants import DEFAULT_BODY_CONFIG_FILE, DEFAULT_HEADER_CONFIG_FILE
from utils.read_json import get_json_data


def check_is_environ_contains(app_configs: Dict[str, Any], cfg_name: str, default_value: str):
    if cfg_name in environ:
        if exists(environ.get(cfg_name)):
            app_configs[cfg_name] = environ.get(cfg_name)
            return app_configs
    app_configs[cfg_name] = default_value
    return app_configs


def check_cfg_paths(arg_parser_configs: Dict[str, str], app_configs: Dict[str, Any], cfg_name: str, default_value: str):
    if arg_parser_configs.get(cfg_name):
        if exists(arg_parser_configs.get(cfg_name)):
            app_configs[cfg_name] = arg_parser_configs.get(cfg_name)
            return app_configs
    if cfg_name in app_configs:
        if exists(app_configs.get(cfg_name)):
            return app_configs
    return check_is_environ_contains(app_configs, cfg_name, default_value)


def validate_application_configs(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracting application configurations file path. File path can be pass from cli arguments or environment.
    If there is no app_cfg will be used default path.
    :param arguments: Arguments provided via cli.
    :return: Application configs or raising exception.
    If raising exception description about fail will be write into logs.
    """
    if arguments.get("app_cfg"):
        app_cfg = arguments.get("app_cfg")
    else:
        app_cfg = environ.get("app_cfg", DEFAULT_APP_CONFIG_FILE)
    try:
        app_configs = get_json_data(app_cfg)
    except Exception as e:
        print(e)
        raise e
    try:
        configure_logger(app_configs["logger"], arguments["log_handler"])
    except Exception as e:
        print("Error in configuring process. Error message:")
        print()
        print(e)
        print()
        raise e
    check_cfg_paths(arguments, app_configs, "body_cfg", DEFAULT_BODY_CONFIG_FILE)
    check_cfg_paths(arguments, app_configs, "saving_direction", DEFAULT_SAVING_DIRECTION)
    check_cfg_paths(arguments, app_configs, "headers_cfg", DEFAULT_HEADER_CONFIG_FILE)
    return app_configs
