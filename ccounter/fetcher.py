# -*- coding: utf-8 -*-

import io
import traceback

import requests
import aioprocessing

from datastructures import FileItem, FailedItem
from logger import logger


def download_file(url_item, analysis_queue, failed_queue):
    """download file function to be run in parallel process"""
    logger.debug(f'download_file got url item {url_item}')

    try:
        response = requests.get(url_item.url)
    except:
        error = 'Failed to download file.'
        tc = traceback.format_exc()
        logger.warn(f'{error}, traceback: {tc}')
        failed_queue.put(FailedItem(url_item, error, tc))
        return

    logger.debug(
        f'Response for URL {url_item.url}, '
        f'status code: {response.status_code}')
    status_code = response.status_code
    if status_code != 200:
        error = f'Failed to download file, got status code {status_code}'
        failed_queue.put(FailedItem(url_item, error, None))
        logger.warn(f'{error}, traceback: {tc}')
        return

    try:
        logger.debug(f'Putting image to analysis queue {url_item}')
        analysis_queue.put(FileItem(
            url_item.url,
            url_item.pointer_diff,
            io.BytesIO(response.content)
        ))
    except:
        error = 'Unexpected error'
        tc = traceback.format_exc()
        logger.warn(f'{error}, traceback: {tc}')
        failed_queue.put(FailedItem(url_item, error, tc))


def error_download(*args, **kwargs):
    """Error download

    Really shouldn't happen but it's nice to know of bugs."""
    logger.warn('download_file unexpected error', args, kwargs)


async def fetcher(queues):
    """Fetcher performs parallel downloads"""
    # Create multiprocessing pool
    process_poll = aioprocessing.AioPool()
    while True:
        url_item = await queues.in_files.coro_get()
        logger.debug(f'Fetcher got url item {url_item}')
        if url_item == '__finished_reading_urls':
            break
        process_poll.apply_async(
            download_file,
            kwds={
                'url_item': url_item,
                'analysis_queue': queues.analysis,
                'failed_queue': queues.failed
            },
            error_callback=error_download)
    process_poll.close()
    process_poll.join()
    await queues.analysis.coro_put('__finished_downloading')
