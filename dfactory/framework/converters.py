#!/usr/bin/env python
# coding=utf-8
from typing import List

from .handlerbase import Handler
from .matches import Match, new_match_from_dict
from .updaters import Updater, new_updater_from_dict


def new_converter_from_dict(data: dict):
    assert data['type'] == 'converter'
    return Converter.from_dict(data)


class Converter(Handler):

    def __init__(self, match: Match, updaters: List[Updater]):
        self.match = match
        self.updaters = updaters

    def handle(self, item: dict) -> dict:
        """
        converter，if match update data otherwise return the origin
        :param item: object to be handle
        :return:
        """
        if self.match.match(item):
            for u in self.updaters:
                item = u.handle(item)
        return item

    @staticmethod
    def from_dict(data):
        assert 'match' in data and 'updater' in data
        m = new_match_from_dict(data['match'])
        updaters = []
        if isinstance(data['updater'], dict):
            u = new_updater_from_dict(data['updater'])
            assert u is not None
            updaters.append(u)
        elif isinstance(data['updater'], list):
            for c in data['updater']:
                assert isinstance(c, dict)
                u = new_updater_from_dict(c)
                assert u is not None
                updaters.append(u)
        return Converter(m, updaters)
