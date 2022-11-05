from logging.config import dictConfig
from os import mkdir
from os.path import exists, join
from pathlib import Path
from typing import Any, Dict

from utils.constants import ROOT_DIRECTORY


def check_or_create_directory(path: str) -> bool:
    """
        Checking is logger file existing or not.
        If file not existing trying to create directory.
    :param path: .log file's path.
    :return: True if file existing or the log directory created successfully
    """
    if not exists(path):
        dir_path = Path(path).parent.resolve()
        if not exists(dir_path):
            try:
                mkdir(dir_path)
            except Exception:
                return False
            else:
                return True
    return True


def configure_logger(logger_config: Dict[str, Any], handler: str) -> Any:
    """
    Configuring logger using the settings got from application configs (app_cfg file).
    If handler is console all logs will be outputted in cli ,
    if handler is file_handler , logs will be wrote in log file.
    :param handler: Log handler which should be used.
    :param logger_config: logger configuration
    :return: raising exception if cannot find configs or correctly configure logger ,
    or returning loggers configurations
    """
    logger_config["loggers"]["info_logger"]["handlers"] = [handler]
    if handler == "file_handler":
        if "handlers" in logger_config:
            if "file_handler" in logger_config["handlers"]:
                if "filename" in logger_config["handlers"]["file_handler"]:
                    log_file_path = join(ROOT_DIRECTORY, logger_config["handlers"]["file_handler"]["filename"])
                    if not check_or_create_directory(log_file_path):
                        raise Exception("Cannot create directory for log files.")
                    logger_config["handlers"]["file_handler"]["filename"] = log_file_path
    dictConfig(logger_config)
    return logger_config
