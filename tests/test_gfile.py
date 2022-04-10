# !/usr/bin/env python
"""Test gfile submodule.

@Filename:    test_gfile.py
@Author:      YangyangLi
@contact:     li002252@umn.edu
@license:     MIT Licence
@Time:        4/10/22 9:56 AM
"""
import subprocess

import pytest
from click.testing import CliRunner

import pyboxes


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://drive.google.com/file/d/16vMzgQYpSuFAHsgPQltMdMblk-RpML1u/view?usp=sharing",
            "16vMzgQYpSuFAHsgPQltMdMblk-RpML1u",
        )
    ],
)
def test_cli(url, expected, monkeypatch):
    """Test cli for gfile."""
    monkeypatch.setattr(subprocess, "check_call", lambda link, shell, stdout: None)
    runner = CliRunner()
    help_result = runner.invoke(pyboxes.main, ["gfile", "-u", url, "s"])
    assert help_result.exit_code == 0
