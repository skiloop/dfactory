"""
JsonSeeder which generate item from json file
"""
from copy import deepcopy

from dfactory.core import Seeder
from dfactory.utils.jsonutils import read_json, read_json_by_line


class JsonSeeder(Seeder):
    """
    JsonSeeder generate items from json file
    """
    KEY_NAME = "__KEY__"

    def __init__(self, path: str = None, key: str = None, is_list: bool = False):
        super().__init__()
        self.path = path
        self.__key = self.KEY_NAME if key is None else key
        self.__is_list = is_list

    def iter(self) -> dict:
        if self.__is_list:
            yield from read_json_by_line(self.path)
        else:
            data = read_json(self.path)
            for key, values in data.items():
                item = deepcopy(values)
                if self.__key not in item:
                    item[self.__key] = key
                yield item

    def load_data(self, cfg: dict):
        self.path = cfg['path']
        self.__key = cfg.get('key', self.KEY_NAME)
        self.__is_list = cfg.get('is_list', False)
