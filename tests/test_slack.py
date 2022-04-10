# !/usr/bin/env python
"""Test Slack.

@Filename:    test_slack.py
@Author:      YangyangLi
@contact:     li002252@umn.edu
@license:     MIT Licence
@Time:        4/9/22 9:21 PM
"""
import pytest
import requests  # type: ignore
from click.testing import CliRunner

import pyboxes
from . import MockResponse


def test_without_argument():
    """Test the command line interface for slack subcommand."""
    runner = CliRunner()
    result = runner.invoke(pyboxes.main, ["slack"])
    assert result.exit_code == 2
    assert "Missing argument" in result.output
    assert result.exc_info[0] == SystemExit


@pytest.mark.parametrize(
    "error_code, expected_output", [(200, "Successfully"), (404, "Failed")]
)
def test_with_webhook(monkeypatch, error_code, expected_output):
    """Test the command line interface for slack subcommand."""
    monkeypatch.setattr(
        requests,
        "post",
        lambda url, data, headers: MockResponse({"text": "Hello"}, error_code),
    )

    runner = CliRunner()
    result = runner.invoke(pyboxes.main, ["slack", "fake hook", "-m", "test"])
    assert expected_output in result.output
