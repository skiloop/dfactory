#!/usr/bin/env python
# coding=utf-8
from .converters import new_converter_from_dict
from .writers import new_writer_from_dict

__config__ = {
    "converter": new_converter_from_dict,
    "writer": new_writer_from_dict
}


def new_operator_from_dict(data: dict):
    func = __config__.get(data['type'])
    if func is not None:
        return func(data)
