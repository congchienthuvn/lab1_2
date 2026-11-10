import configparser
from pathlib import Path


def load_config(filename="database.ini", section="postgresql"):
    parser = configparser.ConfigParser()
    ini_path = Path(__file__).parent / filename
    parser.read(ini_path)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f"Section '{section}' not found in the {filename} file.")

    return config