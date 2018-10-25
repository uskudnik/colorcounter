# -*- coding: utf-8 -*-
"""Error handler module"""
from logger import logger


def print_error(errors):
    for err in errors:
        # Logger for some reason outputs double output
        print(err)


async def handler(sem, progress_bar, failed_queue):
    """Handle error that got pushed into failed / error queue"""
    errors = []
    num_errors = 0
    while True:
        error = await failed_queue.coro_get()
        num_errors += 1
        if error == '__done_writing':
            break
        logger.debug(error)
        err = f'Failed analyzing {error.url_item.url}, reason: {error.pretty_error}'
        errors += [err]
        sem.release()
        progress_bar.update(error.url_item.pointer_diff)

        if num_errors == 100:
            print_error(errors)
            errors = []
            num_errors = 0

    print_error(errors)