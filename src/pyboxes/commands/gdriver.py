# !/usr/bin/env python
# @Filename:    cli.py
# @Author:      li002252
# @Time:        12/2/21 9:42 PM
"""the command line interface for pybox."""
import re
import subprocess

import click
from loguru import logger


@click.command(options_metavar="[options]")
@click.argument("url", type=click.STRING, metavar="<url>")
@click.argument("name", type=click.STRING, metavar="<name>")
@click.argument("size", type=click.INT, metavar="<size>")
def cli(url: str, name: str, size: int) -> None:
    """Download file in Google Driver. You need to provide the sharing url,
    and estimated size of the file. The config is in terms of the file
    size so you need to be careful! Specify the size is divided into 2 classes:\n
    \b
    the large file : file size > 100mb
    the small file : file size < 100mb
    """
    pattern = re.compile(r"\/([0-9a-zA-Z-_]+)[\/a-z=\?]+?$")

    file_id = re.findall(pattern, url)[0]

    if int(size) > 100:
        link = (
            f'wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget '
            f"--quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "
            f"'https://docs.google.com/uc?export=download&id={file_id}' -O- | sed -rn 's/.*confirm=(["
            f"0-9A-Za-z_]+).*/\\1\\n/p')&id={file_id}\" -O {name} && rm -rf /tmp/cookies.txt "
        )
        subprocess.check_call(link, shell=True)
        logger.success(f"downloaded {name}  Size about {size}mb")

    else:
        link = f"wget --no-check-certificate 'https://docs.google.com/uc?export=download&id={file_id}' -O {name}"
        subprocess.check_call(link, shell=True)
        logger.success(f"downloaded {name} Size about {size}mb")


if __name__ == "__main__":
    cli()
