#!/usr/bin/env python
# coding=utf-8
import abc


class Handler(object):

    @abc.abstractmethod
    def handle(self, item: dict) -> dict:
        raise NotImplementedError("virtual function called")
