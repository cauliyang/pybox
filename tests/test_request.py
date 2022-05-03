# !/usr/bin/env python
"""Test request submodule.

Download Test Data from https://fastest.fish/test-files

@Filename:    test_request.py
@Author:      YangyangLi
@contact:     li002252@umn.edu
@license:     MIT Licence
@Time:        3/05/22 9:56 AM
"""
from pathlib import Path

from click.testing import CliRunner

import pyboxes


def test_cli_url(
    tmp_path,
    url="https://www.dundeecity.gov.uk/sites/default/files/publications/civic_renewal_forms.zip",
):
    """Test cli for request with a url."""
    output_file = tmp_path / "test_5m.zip"
    runner = CliRunner()
    result = runner.invoke(
        pyboxes.main, ["request", "-u", url, "-o", output_file.as_posix()]
    )
    assert result.exit_code == 0
    assert output_file.exists()


def test_cli_no_para():
    """Test cli for request with no parameters."""
    runner = CliRunner()
    result = runner.invoke(pyboxes.main, ["request"])
    assert result.exit_code != 0


def test_cli_two_para():
    """Test cli for request with conflict parameters."""
    runner = CliRunner()
    result = runner.invoke(pyboxes.main, ["request", "-u", "link", "-f", "file"])
    assert result.exit_code != 0


def test_cli_url_file(tmp_path):
    """Test cli for request with a url file."""
    output_file1 = tmp_path / "test_1m.zip"
    output_file2 = tmp_path / "test_10m.zip"
    url_file = Path(tmp_path / "test_url.txt")
    url_file.write_text(
        f"{output_file1.as_posix()} "
        "https://www.dundeecity.gov.uk/sites/default/files/publications/civic_renewal_forms.zip\n"
        f"{output_file2.as_posix()} "
        "https://github.com/yourkin/fileupload-fastapi/raw/a85a697cab2f887780b3278059a0dd52847d80f3/tests/data/test-10mb.bin\n"
    )
    runner = CliRunner()
    help_result = runner.invoke(
        pyboxes.main, ["request", "-f", f"{url_file.as_posix()}"]
    )
    assert help_result.exit_code == 0
    assert output_file1.exists()
    assert output_file2.exists()
