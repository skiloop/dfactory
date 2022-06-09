"""
string cutter handler
"""
from dfactory.core import Handler


class StringCutter(Handler):
    """cut string field with specify size"""

    def __init__(self):
        super().__init__()
        self.keys = {}

    def load_data(self, cfg: dict):
        self.keys = cfg['keys']

    @staticmethod
    def cut(src, start, end):
        """
        cut string
        :param src: string to cut
        :param start: start pos to cut
        :param end: end pos (end not include in sub string)
        :return: is src is None or empty return original else return src[start:end]
        """
        if src is None or src == "":
            return src
        return src[start:end]

    def handle(self, item: dict) -> dict:
        for key in self.keys:
            item[key] = self.cut(item[key], self.keys[key].get('start', 0), self.keys[key]['end'])

        return item
