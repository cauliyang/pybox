# Pybox

<div align="center">

<img src="https://raw.githubusercontent.com/cauliyang/pybox/main/docs/_static/logo.png" width=50% alt="logo">

[![pypi](https://img.shields.io/pypi/v/pyboxes.svg)](https://pypi.org/project/pyboxes/)
[![status](https://img.shields.io/pypi/status/pyboxes.svg)](https://pypi.org/project/pyboxes/)
[![python version](https://img.shields.io/pypi/pyversions/pyboxes)](https://pypi.org/project/pyboxes)
[![license](https://img.shields.io/pypi/l/pyboxes)](https://opensource.org/licenses/MIT)
[![read the docs](https://img.shields.io/readthedocs/pyboxes/latest.svg?label=Read%20the%20Docs)](https://pyboxes.readthedocs.io/)

[![test](https://github.com/cauliyang/pybox/workflows/Tests/badge.svg)](https://github.com/cauliyang/pybox/actions?workflow=Tests)
[![codecov](https://codecov.io/gh/cauliyang/pybox/branch/main/graph/badge.svg)](https://codecov.io/gh/cauliyang/pybox)
[![precommit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

## Aims

![feature1](https://cdn.jsdelivr.net/gh/cauliyang/blog-image@main//img/20211205150625.png)

- **Simple**: A simple and easy to use Python library for many annoy task.
- **Easy to use**: Easy to use, you can use it in your project.
- **extendable**: Extendable, you can add your own function easily.

## Features

<details>

<summary> Google Driver</summary>

[Google-Driver]: A simple and easy to download files by sharing link of Google Driver.

For example:

```bash
$ pybox gdriver <url> <name> <size>
```

Detailed usage please see [Usage Documentation]

</details>

<details>

<summary> Slack</summary>

[Slack]: A simple and easy to send message to Slack Channel.

For example:

```bash
$ pybox slack [options] <webhook-url>
```

Detailed usage please see [Usage Documentation]

</details>

- More to come...

## Installation

You can install _Pybox_ via [pip] from [PyPI]:

```bash
$ pip install pyboxes
```

## Usage

```bash
$ pybox -h
```

Please see the Command-line Reference [Usage] for details.

## Contributing

Contributions are very welcome. To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license],
_Pybox_ is free and open source software.

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[//]: # "link"
[cjolowicz]: https://github.com/cjolowicz
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[mit license]: https://opensource.org/licenses/MIT
[pypi]: https://pypi.org/
[file an issue]: https://github.com/cauliyang/pybox/issues
[pip]: https://pip.pypa.io/
[google-driver]: https://www.google.com/drive/
[usage]: https://pyboxes.readthedocs.io/en/latest/usage.html
[slack]: https://slack.com/

% github-only

[contributor guide]: CONTRIBUTING.md
[usage documentation]: https://pyboxes.readthedocs.io/en/latest/usage.html
