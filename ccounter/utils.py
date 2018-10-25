# -*- coding: utf-8 -*-
"""utils module"""


def int_to_rgb(int_):
    """Integer to RGB conversion"""
    red = (int_ >> 24) & 255
    green = (int_ >> 16) & 255
    blue = (int_ >> 8) & 255
    return red, green, blue


def rgb_to_hex(rgb):
    """RGB to HEX conversion"""
    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
