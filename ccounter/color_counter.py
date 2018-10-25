# -*- coding: utf-8 -*-
"""Color counter script"""
import asyncio
import sys

import tqdm
import aioprocessing

import cli_parser
import counter
import datastructures
import errorhandler
import fetcher
import reader
import writer


MAX_CONCURRENT_ITEMS = 100


async def amain(args):
    """Async main to run the event loop and related functionality"""
    # Initialize queues for communication between pipeline stages
    manager = aioprocessing.managers.AioSyncManager()
    manager.start()

    queues = datastructures.Queues(
        manager.AioQueue(maxsize=MAX_CONCURRENT_ITEMS),
        manager.AioQueue(maxsize=MAX_CONCURRENT_ITEMS),
        manager.AioQueue(maxsize=MAX_CONCURRENT_ITEMS),
        manager.AioQueue(),
    )

    # Get total file size so that we can show lovely progress bar
    in_file = args.file[0]
    in_file_size = await reader.get_file_size(in_file)
    progress_bar = tqdm.tqdm(total=in_file_size)

    # There's no point in having bazillion items in random stages since the
    # program is network bound anyway, semaphore to limit how many items in
    # total are in the pipeline.
    items_sem = asyncio.BoundedSemaphore(value=50)

    await asyncio.gather(
        reader.read_input(items_sem, in_file, queues.in_files),
        fetcher.fetcher(queues),
        counter.count(args.num_colors, queues),
        writer.write_result(items_sem, progress_bar, args, queues),
        errorhandler.handler(items_sem, progress_bar, queues.failed)
    )


def main():
    """main function to initialize the parser and start the event loop"""
    parser = cli_parser.get_cli_parser()
    args = parser.parse_args()

    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(amain(args))


if __name__ == '__main__':
    sys.exit(main())
