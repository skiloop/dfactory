"""
setup.py
"""

# !/usr/bin/env python
# coding=utf-8
import platform
from os.path import join, dirname

from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
)
