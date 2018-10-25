# -*- coding: utf-8 -*-
"""CLI parser"""

import argparse


def get_cli_parser():
    """Creates CLI parser"""
    parser = argparse.ArgumentParser(
        description='Find N most common colors in images.')
    parser.add_argument('file', metavar='<INPUT FILE>', type=str, nargs=1,
                        help='File with list of urls separated by new line')
    parser.add_argument('--output_file',
                        metavar='<OUTPUT FILE>', type=str, nargs=1,
                        help='CSV file that will contain a list of urls '
                             'with hex encoded colors. Default is '
                             'INPUT FILE-colors.csv')
    parser.add_argument('--number-of-colors', dest='num_colors',
                        action='store', default=3,
                        help='Number of colors to output. Default is 3')
    return parser
