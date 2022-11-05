import json
from os.path import exists


def get_json_data(file_path: str):
    """
    Reading json file , loading data and returning.
    :param file_path: json configuration file
    :return: config file data or exeption ( if fiel not existing or invalid json )
    """
    if not exists(file_path):
        raise Exception(f"{file_path} not exists")
    with open(file_path, "r") as config_file:
        return json.load(config_file)
