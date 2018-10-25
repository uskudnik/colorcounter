# -*- coding: utf-8 -*-
"""Counter module"""

import traceback

from numba import jit
from PIL import Image
import numpy as np
import aioprocessing

from ccounter import datastructures
from ccounter import logger
from ccounter import utils
# from .datastructures import ,, FailedItem
# from .logger import logger
# from .utils import int_to_rgb


@jit(nopython=True, nogil=True)
def image_to_integers(data):
    """Convert image to one dimensional array of integers

    Uses vectorization to speed up calculations."""
    # Flatten pixels to one dimensional array
    data = data.reshape(-1, data.shape[-1])

    # Binary shift of RGB data to convert to integers
    red = np.left_shift(data[:, 0], 24)
    green = np.left_shift(data[:, 1], 16)
    blue = np.left_shift(data[:, 2], 8)
    return np.bitwise_or(np.bitwise_or(red, green), blue)


def load_image(raw_data):
    """Convert numerical values to 64 bit integers."""
    return np.int64(Image.open(raw_data))


def color_counter(raw_data, n_colors):
    """Color counter

    Returns a list of tuples containing pixel value (as RGB tuple) and a count
    of the number of times that pixel is present - [((R, G, B), count), ...].
    Colors are sorted in descending order.

    Converts pixels to integers by binary shifting RGB vales, finds unique
    integers and counts them and then performs partition based to find N most
    common colors.

    """
    img = load_image(raw_data)

    pixel_integers = image_to_integers(img)

    # Count colors
    # Uses mergesort underhood
    colors, counts = np.unique(pixel_integers, return_counts=True)

    # Get indices of n most common colors
    # argpartition is used because it uses introselect (worst case O(n)). While
    # the order of the partition is undefined, we perform a quick sort based on
    # number of counts afterwards to guarantee the order.
    #
    # https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.argpartition.html
    # https://en.wikipedia.org/wiki/Introselect
    indices = np.argpartition(counts, counts.shape[0] - n_colors)
    indices = indices[-n_colors:]

    # Ensure values ars sorted correctly.
    res = [(utils.int_to_rgb(colors[i]), counts[i]) for i in indices]
    res.sort(key=lambda x: x[1], reverse=True)

    return res


def counter(queues, file_item, n_colors):
    """Counter

    Handles queue item processing, queue insertion and errors."""
    try:
        colors = color_counter(file_item.raw_data, n_colors)
        queues.results.put(
            datastructures.Result(
                file_item.url, file_item.pointer_diff, colors))
    except:
        error = 'Failed to download file.'
        tc = traceback.format_exc()
        logger.logger.warn(f'{error}, traceback: {tc}')
        queues.failed.put(datastructures.FailedItem(file_item.url, error, tc))


def error_count(*args, **kwargs):
    """Error count

    Really shouldn't happen but it's nice to know of bugs."""

    logger.logger.warn(f'error_count, args: {args}, kwargs: {kwargs}')


async def count(num_colors, queues):
    """Perform parallel pixel computation"""
    counter_poll = aioprocessing.AioPool()

    while True:
        file_item = await queues.analysis.coro_get()
        if file_item == '__finished_downloading':
            # We're done, let's break out and terminate processes
            break
        logger.logger.debug(f'Counter got item to analyze: {file_item.url}')

        counter_poll.apply_async(
            counter,
            kwds={
                'queues': queues,
                'file_item': file_item,
                'n_colors': int(num_colors),
            },
            error_callback=error_count)
    counter_poll.close()
    counter_poll.join()
    await queues.results.coro_put('__finished_counting')
