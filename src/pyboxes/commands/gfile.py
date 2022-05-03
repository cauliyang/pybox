# !/usr/bin/env python
# @Filename:    cli.py
# @Author:      li002252
# @Time:        12/2/21 9:42 PM
"""the command line interface for pybox."""
import re
import subprocess
from typing import List

import click
from loguru import logger


# TODO: Need to refactor this file.


def down_large_size(file_id: str, out: str) -> None:
    """Download large size file."""
    link = (
        f'wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget '
        f"--quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "
        f"'https://docs.google.com/uc?export=download&id={file_id}' -O- | sed -rn 's/.*confirm=(["
        f"0-9A-Za-z_]+).*/\\1\\n/p')&id={file_id}\" -O {out} && rm -rf /tmp/cookies.txt "
    )
    subprocess.check_call(link, shell=True, stdout=subprocess.DEVNULL)
    logger.success(f"downloaded {out}")


def down_small_size(file_id: str, out: str) -> None:
    """Download small size file."""
    link = f"wget --no-check-certificate 'https://docs.google.com/uc?export=download&id={file_id}' -O {out}"
    subprocess.check_call(link, shell=True, stdout=subprocess.DEVNULL)
    logger.success(f"downloaded {out}")


def download(field_ids: List[str], size: str, out: str) -> None:
    """Download the file from google drive."""
    for ind, field_id in enumerate(field_ids):
        if size == "l":
            try:
                down_large_size(field_id, f"{out}_{ind}")
            except subprocess.CalledProcessError:
                logger.warning(f"failed to download {field_id} {ind=}")

        else:
            try:
                down_small_size(field_id, f"{out}_{ind}")
            except subprocess.CalledProcessError:
                logger.warning(f"failed to download {field_id} {ind=}")


@click.command(options_metavar="[options]")
@click.option(
    "-u",
    "--url",
    type=click.STRING,
    metavar="<url>",
    help="the sharing link of the google drive file.",
)
@click.option(
    "-o",
    "--out",
    type=click.STRING,
    metavar="<name>",
    default="out",
    show_default=True,
    help="the output file name.",
)
@click.option(
    "-f",
    "--url-file",
    type=click.File("r"),
    metavar="<url-file>",
    help="the file contains the sharing link of the google drive file.",
)
@click.argument("size", type=click.STRING, metavar="<size>")
def cli(url: str, out: str, size: str, url_file: str) -> None:
    """Download file in Google Driver. You need to provide the sharing url,
    and estimated size of the file. The config is in terms of the file
    size so you need to be careful! Specify the size is divided into 2 classes:\n
    \b
    the large file : file size > 100mb -> size parameters: l
    the small file : file size < 100mb -> size parameters: s
    Usage:
    pybox gfile -u https://drive.google.com/file/d/1-2-3-4-5/view?usp=sharing l
    pybox gfile -f url-file.txt l
    """
    if not url and not url_file:
        logger.error("You need to provide a url or a url file")
        raise SystemExit

    pattern = re.compile(r"\/([0-9a-zA-Z-_]+)[\/a-z=\?]+?$")
    if url:
        file_id = re.findall(pattern, url)[0]
        download([file_id], size, out)
    else:
        file_ids = []
        for line in url_file:
            file_ids.append(re.findall(pattern, line.strip())[0])
        download(file_ids, size, out)


if __name__ == "__main__":
    cli()
