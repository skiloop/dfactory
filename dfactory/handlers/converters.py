#!/usr/bin/env python
# coding=utf-8
from typing import List

from dfactory.core import Handler, CondHandler
from dfactory.handlers.matches import Match
from dfactory.handlers.updaters import Updater
from dfactory.utils.json import read_json


class Converter(CondHandler):
    """
    converter to convert one or more fields of object
    """

    def __init__(self, match: Match = None, updaters: List[Updater] = None):
        self.match = match
        self.updaters = updaters

    def check(self, item: dict) -> bool:
        """
        check if the item should be converted
        :param item: src item
        :return: True if the item should be converted else False
        """
        return self.match.match(item) is not None

    def operate(self, item: dict) -> dict:
        """
        converter，if match update data otherwise return the origin
        :param item: object to be handle
        :return: the handled item
        """

        for updater in self.updaters:
            item = updater.handle(item)
        return item

    def load_data(self, cfg: dict):
        """
        construct new Converter from config
        :param cfg: config data
        :return: new Converter or None
        """
        matcher = Match.from_dict(cfg['match'])
        updaters = []
        if isinstance(cfg['updater'], dict):
            updater = Updater.from_dict(cfg['updater'])
            updaters.append(updater)
        elif isinstance(cfg['updater'], list):
            updaters += [Updater.from_dict(updater) for updater in cfg['updater']]
            updaters = list(filter(lambda a: a is not None, updaters))
        self.match = matcher
        self.updaters = updaters


class DictConverter(Handler):
    """
    convert one field of data with dict
    """

    def __init__(self, key: str = None, dst: str = None, mapper: dict = None):
        super().__init__()
        self.key = key
        self.dst = dst
        self.mapper = {} if mapper is None else mapper

    def load_data(self, cfg: dict):
        """
        load data from config
        :param cfg: config data
        :return: None
        """
        mapper = cfg.get("mapper")
        if isinstance(mapper, str):
            mapper = read_json(mapper)
        self.mapper = mapper
        self.key = cfg['key']
        self.dst = cfg.get("dst", cfg["key"])

    def handle(self, item: dict) -> dict:
        """
        convert item with dict mapper
        :param item: item to he convert
        :return: handled item
        """
        item[self.dst] = self.mapper.get(item[self.key], item[self.key])
        return item
