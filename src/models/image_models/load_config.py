import configparser
from ast import literal_eval


def config_loader(config_path):
    config_file_path = config_path
    config = configparser.ConfigParser()
    config.read(config_file_path)
    all_sections = config.sections()

    CONFIG = {}

    for section in all_sections:
        CONFIG[section] = {}
        current_section = config[section]
        for k, v in current_section.items():
            CONFIG[section][k] = literal_eval(v)
    return CONFIG
