#!/usr/bin/env python
# coding=utf-8
import abc
import re

from dfactory.core import LoaderMixin


class Match(LoaderMixin):
    """
    Match class to tell if an item is matched
    """

    @abc.abstractmethod
    def match(self, item: dict):
        """
        match function, tell if an item is match
        :param item: item to check
        :return: True if match otherwise False
        """
        raise NotImplementedError('virtual function called')


class KeyMatch(Match):
    """
    a Match to tell if an item has key with some value
    """

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    def match(self, item: dict):
        if isinstance(self.value, list):
            return item.get(self.key) in self.value
        return item.get(self.key) == self.value

    def load_data(self, cfg: dict):
        """
        load data from config
        :param cfg: config data
        :return: None
        """
        self.key = cfg["key"]
        self.value = cfg["value"]


class TrueMatch(Match):
    """
    TrueMatch match on every item
    """

    def match(self, item: dict):
        """
        match function
        :param item: item to be check
        :return: True
        """
        return True


class RegexMatch(Match):
    """
    match by regex
    """

    def __init__(self, key=None, pattern=None, flag=0):
        self.key = key
        self.pattern = self.fill_pattern(pattern, flag)

    @staticmethod
    def fill_pattern(pattern, flag=0):
        """
        get a re.Pattern
        :param pattern: string or a re.Pattern
        :param flag: regex flag
        :return: re.Pattern
        """
        if isinstance(pattern, str):
            return re.compile(pattern, flag)
        elif isinstance(pattern, re.Pattern):
            return pattern
        else:
            raise ValueError("invalid pattern type, only str or re.Pattern allowed")

    def match(self, item: dict):
        return self.pattern.match(item.get(self.key))

    def load_data(self, cfg: dict):
        """
        load key, and patten from config
        :param cfg: config data
        :return: None
        """
        self.key = cfg["key"]
        self.pattern = self.fill_pattern(cfg["pattern"], cfg.get('flag', 0))


class AndMatch(Match):
    def __init__(self, a: Match = None, b: Match = None):
        self.a = a
        self.b = b

    def match(self, item: dict):
        return self.a.match(item) and self.b.match(item)

    def load_data(self, cfg: dict):
        self.a = self.from_dict(cfg["a"])
        self.b = self.from_dict(cfg["b"])


class OrMatch(Match):
    def __init__(self, a: Match = None, b: Match = None):
        self.a = a
        self.b = b

    def match(self, item: dict):
        return self.a.match(item) or self.b.match(item)

    def load_data(self, cfg: dict):
        self.a = self.from_dict(cfg["a"])
        self.b = self.from_dict(cfg["b"])


class NotMatch(Match):
    def __init__(self, a: Match = None):
        self.a = a

    def match(self, item: dict):
        return not self.a.match(item)

    def load_data(self, cfg: dict):
        self.a = self.from_dict(cfg["a"])
