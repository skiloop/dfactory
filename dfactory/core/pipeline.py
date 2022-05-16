# -*- coding: utf-8 -*-

"""
Pipeline is a data flow pipeline with a group of handlers
to operate actions on a flow of dict data
"""
from typing import Dict

from .base import Handler, Seeder, LoaderMixin


class Pipeline(LoaderMixin):
    """
    data pipeline class
    """

    def __init__(self):
        self.seeder = None
        self.operators = []

    def handle(self):
        """
        handle over operators
        :return:
        """
        for obj in self.seeder.iter():
            if obj is None:
                break
            for operator in self.operators:
                obj = operator.handle(obj)
                if obj is None:
                    break

    def exit(self):
        """
        action on exit
        :return: None
        """
        if hasattr(self.seeder, "on_destroy"):
            self.seeder.on_destroy()
        for operator in self.operators:
            if hasattr(operator, 'on_destroy'):
                operator.on_destroy()

    def enter(self):
        """
        action before pipeline operator starts up
        :return: None
        """
        for operator in self.operators:
            if hasattr(operator, 'on_create'):
                operator.on_create()

    def add(self, operator: Handler):
        """
        add new handler
        :param operator: object of Handler
        :return: None
        """
        self.operators.append(operator)

    def load_data(self, cfg: dict):
        """
        load operators from dict data
        :param cfg: operators config
        :return: None
        """
        self.seeder = Seeder.from_dict(cfg['seeder'])
        for handler_cfg in cfg['handlers']:
            obj = Handler.from_dict(handler_cfg)
            if obj is not None:
                self.add(obj)

    @staticmethod
    def from_dict(cfg: Dict):
        """
        create Pipeline object from dict data
        :param cfg: pipeline config
        :return: a new Pipeline object
        """
        pipeline = Pipeline()
        pipeline.load_data(cfg)
        return pipeline

    def run(self):
        """
        start pipeline
        :return: None
        """
        self.enter()
        if len(self.operators) > 0:
            self.handle()
        self.exit()
