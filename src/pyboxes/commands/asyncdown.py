# !/usr/bin/env python
"""Asynchronous downloader for files in terms of links.

@Filename:    asyncdown.py
@Author:      YangyangLi
@contact:     li002252@umn.edu
@license:     MIT Licence
@Time:        5/3/22 9:26 AM
"""
import asyncio
import sys
import typing as t
from asyncio import Queue
from pathlib import Path

import aiofiles
import aiohttp
import click
from aiohttp.client import ClientTimeout
from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True,
)


def check_exist(filename: str, url: str, urls: t.Dict[str, str]) -> None:
    """Check if the file exists in the local directory.

    .. note::
                                    If the file exists, it will be overwritten.
                                    If the file name starts with '#', it will be ignored.
    """
    if Path(filename).exists():
        logger.warning(f"{filename} already exists, will be overwritten")

    if not filename.strip().startswith("#"):

        if filename in urls:
            logger.warning(f"{filename} duplicate in url_files, will be overwritten")

        urls[filename] = url


def read_urls(file: t.TextIO) -> t.Dict[str, str]:
    """Read the urls from the file."""
    urls: t.Dict[str, str] = {}
    for line in file:
        try:
            filename, url = line.strip().split()
        except ValueError:
            logger.warning(f"Cannot parse {line!r}, skipped")
        else:
            check_exist(filename, url, urls)
    return urls


class WorkItem:
    """Work item for the worker."""

    def __init__(self, url: str, output: str) -> None:
        """Initialize the work item."""
        self.url = url
        self.output = output


async def download(
    url: str, local_filename: str, session: aiohttp.ClientSession
) -> None:
    """Download a file from `url` and save it locally under `local_filename`."""
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(local_filename, "wb") as f:
                    async for chunk in resp.content.iter_chunked(1024 * 1024):
                        await f.write(chunk)
            else:
                raise RuntimeError(
                    f"Cannot download {url} with status code {resp.status}"
                )
    except Exception as e:
        logger.error(f"Error downloading {local_filename}: {e}")
    else:
        logger.success(f"Finished {local_filename}")


async def worker(worker_id: int, queue: Queue, session: aiohttp.ClientSession) -> None:
    """Download the files in the urls asynchronously."""
    while True:
        item: WorkItem = await queue.get()
        logger.info(f"Worker {worker_id} Processing {item.output}")
        await download(item.url, item.output, session)
        queue.task_done()


async def generate_work_items_non_blocking(
    urls: t.Dict[str, str], queue: Queue
) -> None:
    """Generate the work items."""
    for filename, url in urls.items():
        await queue.put(WorkItem(url, filename))


def generate_work_items_blocking(urls: t.Dict[str, str], queue: Queue) -> None:
    """Generate the work items."""
    for filename, url in urls.items():
        queue.put_nowait(WorkItem(url, filename))


async def main(urls: t.Dict[str, str], timeout: int, max_workers: int) -> None:
    """Download the files in the urls asynchronously."""
    queue: Queue = Queue()
    generate_work_items_blocking(urls, queue)
    logger.info(f"Total Task: {queue.qsize()}")

    max_workers = min(max_workers, len(urls))
    logger.info(f"Starting {max_workers} workers")

    client_timeout = ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=client_timeout) as session:
        _ = [asyncio.create_task(worker(i, queue, session)) for i in range(max_workers)]

        await queue.join()


@click.command(options_metavar="[options]")
@click.option("-u", "--url", type=click.STRING, metavar="<url>", help="URL to download")
@click.option(
    "-o",
    "--out",
    type=click.STRING,
    metavar="<name>",
    default="out",
    show_default=True,
    help="Output name",
)
@click.option(
    "-f",
    "--url-file",
    type=click.File("r"),
    metavar="<url-file>",
    help="File containing URLs to download",
)
@click.option(
    "-t",
    "--time",
    type=click.INT,
    metavar="<time-out>",
    default=40,
    show_default=True,
    help="Time out (min) for each download",
)
@click.option(
    "-w",
    "--workers",
    type=click.INT,
    metavar="<max-worker>",
    default=128,
    show_default=True,
    help="Maximum number of workers",
)
def cli(url: str, out: str, url_file: t.TextIO, time: int, workers: int) -> None:
    """Download files in terms of links asynchronously.

    \b
    Examples:
                                    pybox asyncdown -u url-link  -o book.pdf
                                    pybox asyncdown -f url-file.txt

    \b
    Note:
                                    1. If you want to download multiple files, you can use the url-file.
    """
    if not url and not url_file:
        raise click.BadArgumentUsage("You need to provide a url or a url file")
    if url and url_file:
        raise click.BadArgumentUsage("You can only provide one url or url file")

    urls = {out: url} if url else read_urls(url_file)
    asyncio.run(main(urls, time * 60, workers))


if __name__ == "__main__":
    cli()
