# -*- coding: utf-8 -*-
"""Logging module"""

import logging

logger = logging.getLogger('Color counter')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())
