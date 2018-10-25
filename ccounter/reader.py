# -*- coding: utf-8 -*-
"""Module for reading the input file"""

import aiofiles
import datastructures

from logger import logger


def clean_line(url):
    """Clean input line"""
    return url.rstrip('\n')


async def get_file_size(in_f):
    """Get input file size"""
    async with aiofiles.open(in_f) as infile:
        # Figure out how many bytes do we need to read in total
        return await infile.seek(0, 2)


async def read_input(semaphore, in_f, queue):
    """Read file

    Reads file line by line to ensure we don't consume bazillon items that
    can't be processed as fast because we're network-bound.
    """
    async with aiofiles.open(in_f) as infile:
        # Go to file start
        await infile.seek(0, 0)

        previous_position = 0

        line = await infile.readline()
        while line:
            # Calculate current position in file
            current_position = await infile.tell()
            diff_pos = current_position - previous_position
            previous_position = current_position

            url = clean_line(line)
            item = datastructures.URLItem(url, diff_pos)

            logger.debug(f'Adding item {item} to queue')

            await semaphore.acquire()
            await queue.coro_put(item)
            line = await infile.readline()

        # Signal that we're done reading input file
        await queue.coro_put('__finished_reading_urls')
