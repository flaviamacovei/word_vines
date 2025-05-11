import yaml
import os

dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config_path = os.path.join(dir, 'config.yaml')

class ConfigManager:
    _instance = None

    def __new__(cls, dir = dir):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load(dir)
        return cls._instance

    def _load(self, dir):
        with open(dir + '/config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
        return self.config

    def get(self, key, default=None):
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            elif isinstance(value, list) and k.isdigit():
                index = int(k)
                if index < len(value):
                    value = value[index]
                else:
                    return default
            else:
                return default
        return value
