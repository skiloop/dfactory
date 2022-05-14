#!/usr/bin/env python
# coding=utf-8

from dfactory.core import Handler


def new_writer_from_dict(cfg: dict):
    if cfg['class'] == 'csv':
        return CsvWriter.from_dict(cfg)
    raise ValueError(f"unknown writer: {cfg['class']}")


class CsvWriter(Handler):
    def __init__(self, **kwargs):
        self.filename = kwargs["file"]
        self.file = None
        self.sep = kwargs.get('separator', ",")
        self.headers = kwargs.get('headers')
        self.keys = kwargs.get('keys')
        self.format = None

    def is_created(self) -> bool:
        return self.file is not None

    def on_create(self):
        try:
            self.file = open(self.filename, "w")
            self.prepare_format_fun()
            if self.headers is not None:
                self.file.write(self.sep.join(self.headers) + "\n")
        except IOError:
            pass

    def prepare_format_fun(self):
        if self.keys is not None:
            self.format = lambda a: self.sep.join([str(a[k]) for k in self.keys])
        else:
            self.format = lambda a: self.sep.join([str(a[k]) for k in a])

    def on_destroy(self):
        if self.file is not None:
            self.file.close()
        self.file = None

    @staticmethod
    def from_dict(data: dict):
        kwargs = data.copy()
        kwargs.pop('key')
        return CsvWriter(data['path'], **kwargs)

    def load_data(self, cfg: dict):
        self.on_destroy()
        self.filename = cfg.get("path")
        self.keys = cfg.get("keys")
        self.headers = cfg.get("headers")
        self.sep = cfg.get('separator', ",")

    def handle(self, item: dict):
        try:
            self.file.write(self.format(item))
            self.file.write("\n")
        except IOError:
            pass
        return item
