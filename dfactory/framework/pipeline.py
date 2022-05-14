#!/usr/bin/env python
# coding=utf-8
#
#
from typing import List, Dict

from .common import new_operator_from_dict
from .handlerbase import Handler
from .seeders import Seeder


class Pipeline:
    """
    data pipeline class
    """

    def __init__(self):
        self.operators = []

    def handle(self, item):
        """
        handle over operators
        :param item: object to handle
        :return: the handled object
        """
        obj = item
        for operator in self.operators:
            obj = operator.handle(obj)
            if obj is None:
                break
        return obj

    def exit(self):
        """
        action on exit
        :return: None
        """
        for operator in self.operators:
            if hasattr(operator, 'on_exit'):
                operator.on_exit()

    def enter(self):
        """
        action before pipeline operator starts up
        :return: None
        """
        for operator in self.operators:
            if hasattr(operator, 'on_enter'):
                operator.on_exit()

    def add(self, operator: Handler):
        """
        add new handler
        :param operator: object of Handler
        :return: None
        """
        self.operators.append(operator)

    def load_from_dict(self, data: List[Dict]):
        """
        load operators from dict data
        :param data: operators config
        :return: None
        """
        for cfg in data:
            obj = new_operator_from_dict(cfg)
            if obj is not None:
                self.add(obj)

    @staticmethod
    def from_dict(data: List[Dict]):
        """
        create Pipeline object from dict data
        :param data: pipeline config
        :return: a new Pipeline object
        """
        pipeline = Pipeline()
        pipeline.load_from_dict(data)
        return pipeline

    def iter(self, seeder: Seeder):
        """
        seeding pipeline and handle item
        :param seeder: pipeline seeder
        :return: item generator
        """
        for item in seeder.iter():
            if item is None:
                break
            obj = self.handle(item)
            if obj is None:
                continue
            yield obj

    def run(self, seeder: Seeder, fun=None):
        """
        start pipeline
        :param seeder: pipeline seeder
        :param fun: item operator out of pipeline
        :return: None
        """
        self.enter()
        for item in self.iter(seeder):
            if fun:
                fun(item)
        self.exit()
