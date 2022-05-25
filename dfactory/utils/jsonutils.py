# -*- coding: utf-8 -*-

"""
json utils
"""
import json
from json import JSONEncoder


class JsonEncoder(JSONEncoder):
    """json encoder"""

    def default(self, o):
        if o.__class__.__name__ in ['int64', "int32"]:
            return int(o)
        if o.__class__.__name__ in ['float64', "float32"]:
            return float(o)
        return JSONEncoder.default(self, o)


def read_json(src: str):
    """
    read json file into dict
    :param src: filename
    :return: dict read from json file
    """
    with open(src, encoding="utf-8") as fin:
        return json.loads((fin.read()))
