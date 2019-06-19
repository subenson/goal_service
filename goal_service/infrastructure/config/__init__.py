import yaml
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls) \
                .__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):

    _configuration = dict()

    def __init__(self, config_files):
        directory = os.path.dirname(os.path.realpath(__file__))
        for config_file in config_files:
            with open(f"{directory}/{config_file}", 'r') as file:
                self._configuration.update(
                    yaml.load(file, Loader=yaml.SafeLoader))

    def read(self):
        return self._configuration
