# -*- coding: utf-8 -*-
"""datastructures module"""
import collections


Queues = collections.namedtuple('Queues', [
    'in_files',
    'analysis',
    'results',
    'failed'
])


URLItem = collections.namedtuple('URLItem', [
    'url',
    'pointer_diff'
])


FileItem = collections.namedtuple('FileItem', [
    'url',
    'pointer_diff',
    'raw_data'
])


Result = collections.namedtuple('Result', [
    'url',
    'pointer_diff',
    'colors'
])


FailedItem = collections.namedtuple('FailedItem', [
    'url_item',
    'pretty_error',
    'traceback'
])
