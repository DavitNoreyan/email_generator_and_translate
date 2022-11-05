from logging import getLogger
from os import listdir
from typing import Any, Dict

logger = getLogger("info_logger")


def check_directory_contains_file_with_extension(initial_config: Dict[str, Any], direction_arg_name: str,
                                                 extension: str):
    """
    Checking is got direction containing files with required extension.
    :param initial_config: Body configuration which providing validator
    :param direction_arg_name: Which key is describing containing folder
    :param extension: required extension
    :return: None or raising Exception.
    """
    if direction_arg_name not in initial_config:
        return True
    direction = initial_config.get(direction_arg_name)
    content = listdir(direction)
    for f_name in content:
        if f_name.endswith(f".{extension}"):
            return
    logger.error(f"{direction} doesn't contain file with .{extension} extension.")
    raise Exception("Error in generator configuring process.")


def check_directory_contains_files_with_extension(initial_config: Dict[str, Any], direction_arg_name: str,
                                                  extension_list: list):
    # todo write docs
    count = 0
    if direction_arg_name not in initial_config:
        return True
    direction = initial_config.get(direction_arg_name)
    content = listdir(direction)
    for extension in extension_list:
        for f_name in content:
            if f_name.endswith(f".{extension}"):
                count += 1
        # todo add log
    if count == len(content):
        return
    else:
        raise Exception("Error in generator configuring process.")
