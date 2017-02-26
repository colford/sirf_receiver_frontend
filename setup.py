# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 16:10:03 2017

@author: CFord
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'SiRF Controller',
    'author': 'Colin Ford',
    'url': 'http://github.com/colford/',
    'download_url': 'http://github.com/colford/',
    'author_email': 'col.r.ford@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['sirfcontrol'],
    'scripts': [],
    'name': 'sirfcontroller'
}

setup(**config)