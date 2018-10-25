# -*- coding: utf-8 -*-
"""Writer - asynchronously write out results to a csv file."""
import csv
import os

import aiofiles

from logger import logger
import utils


async def write_result(semaphore, progress_bar, args, queues):
    """Write out results"""
    if not args.output_file:
        in_file_abs = os.path.abspath(args.file[0])
        out_f = f'{in_file_abs}-colors.csv'
    else:
        out_f = os.path.abspath(args.output_file[0])

    async with aiofiles.open(out_f, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile, delimiter=',')
        while True:
            result = await queues.results.coro_get()
            if result == '__finished_counting':
                break
            logger.debug(f'Writer got result: {result}')
            row = [result.url] + [utils.rgb_to_hex(color)
                                  for color, count in result.colors]
            await csv_writer.writerow(row)
            semaphore.release()
            progress_bar.update(result.pointer_diff)
    await queues.failed.coro_put('__done_writing')
