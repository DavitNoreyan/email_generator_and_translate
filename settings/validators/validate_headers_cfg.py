from logging import getLogger
from os.path import exists
from typing import Union, Any, Optional, Dict, Set, List

from settings.config_requirements import SUPPORTED_CHARSETS, DEFAULT_CHARSET, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE, \
    SUPPORTED_ENCODINGS, DEFAULT_ENCODING
from settings.config_requirements.headers import SUPPORTED_HEADERS
from utils.read_json import get_json_data

HEADER_CONFIG_FILE_NAME = "headers_cfg.json"

logger = getLogger("info_logger")


def check_property(headers_config: Dict[str, Union[str, Dict[str, Dict[str, Union[str, int]]]]], property_name: str,
                   supported_values: Set[str], default_value: str) -> None:
    """
    Function for checking headers configuration dict.
    :param headers_config: configurations dict got from headers_cfg.json
    :param property_name: property which value should be checked
    :param supported_values: values set defined in default.headers
    :param default_value: default value which should be assigned property_name in case if checking is failing
    :return: None , the function changing headers_config itself
    """
    if property_name not in headers_config:
        logger.warning(
            f"{property_name} not defined in headers_cfg.json."
            f" {property_name} will be assigned the default '{default_value}' value")
        headers_config[property_name] = default_value
    if headers_config[property_name] not in supported_values:
        logger.warning(
            f"{headers_config[property_name]} not supported."
            f"{property_name} will be changed to the default '{default_value}' value")
        headers_config[property_name] = default_value


def clean_header_config(required_args: List[str], optional_args: List[str], header_configs: Dict[str, Any],
                        header_lower: str, all_configs: Optional[Dict[str, Any]] = None):
    # todo write docs
    cleaned_args = {}
    for optional_property in optional_args:
        if optional_property in header_configs:
            cleaned_args[optional_property] = header_configs.get(optional_property)
    for req_property in required_args:
        if req_property in header_configs:
            cleaned_args[req_property] = header_configs.get(req_property)
        else:
            if all_configs:
                if req_property in all_configs:
                    cleaned_args[req_property] = all_configs.get(req_property)
                else:
                    logger.error(f"{req_property} not specified for {header_lower} in headers_cfg.json file.")
                    return None
            else:
                logger.error(f"{req_property} not specified for {header_lower} in headers_cfg.json file.")
                return None
    return cleaned_args


def replace_value_from_with_dict(headers: Dict[str, Any], header: str, header_lower: str):
    if not exists(headers[header]["value_from"]):
        # todo add logs
        raise Exception("Invalid header configs. Check the logs.")
    file_data = get_json_data(headers[header]["value_from"])
    headers[header].pop("value_from")
    headers[header] = {**headers[header], **file_data}
    supported_arguments = SUPPORTED_HEADERS.get(header_lower)
    supported_arguments["required_arguments"] = supported_arguments[
                                                    "required_arguments"] + supported_arguments.get(
        "fields_providing_via_file")["required_arguments"]
    supported_arguments["optional_arguments"] = supported_arguments.get("fields_providing_via_file")[
        "optional_arguments"]


def validate_headers_configs(headers_configs_file_path: str) -> Dict[str, Any]:
    # TODO add docs
    headers_config: Dict[str, Any] = get_json_data(headers_configs_file_path)
    check_property(headers_config, "charset", SUPPORTED_CHARSETS, DEFAULT_CHARSET)
    check_property(headers_config, "language", SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE)
    check_property(headers_config, "content_transfer_encoding", SUPPORTED_ENCODINGS, DEFAULT_ENCODING)
    headers = headers_config.get("headers", None)
    if headers is None:
        logger.error("Headers not described. Check the headers_cfg.json")
        raise Exception("Error in headers parsing process. For more information check the logs")
    if not isinstance(headers, dict):
        logger.error("headers should be object. Check the headers_cfg.json")
        raise Exception("Error in headers parsing process. For more information check the logs")
    # done make keys insensitive
    # done change key encoding -> cte
    # done for all add high level props
    # todo add functionality for getting val from json From ,To , CC , Bcc , Message-Id , In-Reply-To , References
    # todo add conversation-id header ( index ) [ for future ]
    cleaned_headers = {}
    for header in headers:
        header_lower = header.lower()
        if header_lower not in SUPPORTED_HEADERS:
            logger.warning(f"The {header} header not supported.")
            headers_config["headers"].pop(header, None)
        else:
            if "value_from" in headers[header]:
                replace_value_from_with_dict(headers, header, header_lower)
            supported_arguments = SUPPORTED_HEADERS.get(header_lower)
            cleaned_args = clean_header_config(supported_arguments["required_arguments"],
                                               supported_arguments["optional_arguments"], headers[header],
                                               header_lower,
                                               headers_config)
            cleaned_headers[SUPPORTED_HEADERS[header_lower]["header_name"]] = cleaned_args
    headers_config["headers"] = cleaned_headers
    return headers_config
