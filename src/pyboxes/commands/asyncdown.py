# !/usr/bin/env python
"""Asynchronous downloader for files in terms of links.

@Filename:    request.py
@Author:      YangyangLi
@contact:     li002252@umn.edu
@license:     MIT Licence
@Time:        5/3/22 9:26 AM
"""
import asyncio
import typing as t
from pathlib import Path

import aiofiles
import aiohttp
import click
from aiohttp.client import ClientTimeout
from loguru import logger


async def download(url: str, local_filename: str, session: t.Any) -> None:
    """Download a file from `url` and save it locally under `local_filename`."""
    logger.info(f"Downloading {local_filename}")
    async with session.get(url) as resp:
        if resp.status == 200:
            async with aiofiles.open(local_filename, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 1024):
                    await f.write(chunk)
    logger.success(f"Finished {local_filename}")


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


async def worker(urls: t.Dict[str, str], timeout: int) -> None:
    """Download the files in the urls asynchronously."""
    client_timeout = ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=client_timeout) as session:
        tasks = []
        for filename, url in urls.items():
            tasks.append(download(url, filename, session))
        await asyncio.gather(*tasks)


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
    default=40 * 60,
    show_default=True,
    help="Time out for each download",
)
def cli(url: str, out: str, url_file: t.TextIO, time: int) -> None:
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
    asyncio.run(worker(urls, time))


if __name__ == "__main__":
    cli()
