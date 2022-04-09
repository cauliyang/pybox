# !/usr/bin/env python
# @Filename:    cli.py
# @Author:      li002252
# @Time:        12/2/21 9:42 PM
"""the command line interface for pyboxes to send slack messages"""
import json
import sys
import time
from typing import TextIO

import click
import requests
from loguru import logger


@click.command(options_metavar="[options]")
@click.argument("webhook-url", type=click.STRING, metavar="<webhook-url>")
@click.option(
    "-m",
    "--message",
    type=click.STRING,
    metavar="<message>",
    help="the message to send to slack",
    default="No message provided",
    show_default=True,
)
@click.option(
    "-mf",
    "--message-file",
    type=click.File("r"),
    metavar="<message-file>",
    help="read message from file instead of command line",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    show_default=True,
    metavar="<log-level>",
)
def cli(webhook_url: str, message: str, message_file: TextIO, log_level: str) -> None:
    """Send message to Slack. You can either provide a message or a file containing the messages.
    Also, you can provide both a message and a file containing messages. However, if the message
    and message file are both missing, the command will exit with an error.
    """
    logger.remove()
    logger.add(sys.stdout, level=log_level)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    header = {"Content-Type": "application/json"}
    logger.debug(f"{current_time=}, {message=}, {message_file=} ")
    message = "" if message == "No message provided" else message

    current_message = (
        message + " " + "".join(message_file.readlines())
        if message_file is not None
        else message
    )

    if current_message == "":
        logger.error("No message provided")
        raise SystemExit
    current_message = current_message.replace("\\n", "\n")
    data = {
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": current_time}},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": current_message},
            },
        ]
    }

    response = requests.post(webhook_url, data=json.dumps(data), headers=header)

    if response.status_code == 200:
        logger.success("Successfully sent message to Slack")
    else:
        logger.error("Failed to send message to Slack, please check your webhook url")
        raise SystemExit
