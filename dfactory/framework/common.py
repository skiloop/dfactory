#!/usr/bin/env python
# coding=utf-8

from .converters import new_converter_from_dict
from .handlerbase import Handler
from .writers import new_writer_from_dict

__config__ = {
    "converter": new_converter_from_dict,
    "writer": new_writer_from_dict
}


def import_module(name: str):
    """
    import a module
    :param name: module name with path
    :return: module
    """
    components = name.rsplit(".", 1)
    if len(components) == 1 or "" == components[0]:
        return __import__(name)
    mod = __import__(components[0])
    mod = getattr(mod, components[1])
    return mod


def new_operator_from_dict(data: dict):
    """
    create a new operator object from dict
    :param data: data to load operator
    :return: operator object or None
    """
    func = __config__.get(data['type'])
    if func is not None:
        return func(data)
    my_class = import_module(data["class"])
    if issubclass(my_class, Handler):
        if hasattr(my_class, 'from_dict'):
            return my_class.from_dict(data)
        return my_class()
