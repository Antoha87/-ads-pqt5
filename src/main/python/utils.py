import yaml
import os

from .main import FILE_SETTINGS


class Settings():

    def check_config_file():
        default_settings = {
            'contour_threshold': 1.5,
            'conf_threshold': 0.6,
            'banner_size': 0.2,
            'background': False,
            'allowed_ram_size': 1000,
            'use_segmentation': True,
            'device': 'cpu'
        }

        if not os.path.exists(FILE_SETTINGS):
            with open(r'{FILE_SETTINGS}', 'w') as file:
                settings = yaml.dump(default_settings, file)
                print(settings)


    def get_settings_parametr(param: str):
        with open(FILE_SETTINGS, 'r') as data:
            data_loaded = yaml.safe_load(data)
            if param in data_loaded:
                return data_loaded[param]


    def set_parametr(param: list):
        check_config_file()
        with open(r'{FILE_SETTINGS}', 'w') as file:
            settings = yaml.dump(param, file)
            print(settings)

