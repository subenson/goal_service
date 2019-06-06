import yaml


class Config:

    _configuration = None

    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            self._configuration = yaml.load(file, Loader=yaml.SafeLoader)

    def get(self, *args):
        config = self._configuration
        for arg in args:
            config = config.get(arg)
        return config
