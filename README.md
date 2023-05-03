# easierscrape

A library for basic web scraping.

[![PyPI](https://img.shields.io/pypi/v/easierscrape)](https://pypi.org/project/easierscrape/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![Issues](https://img.shields.io/github/issues/dag2226/easierscrape)](https://github.com/dag2226/easierscrape/issues)
[![Build Status](https://github.com/dag2226/easierscrape/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/dag2226/easierscrape/actions?query=workflow%3A%22Build+Status%22)
[![Codecov](https://codecov.io/gh/dag2226/easierscrape/branch/main/graph/badge.svg)](https://codecov.io/gh/dag2226/easierscrape)
[![Docs](https://img.shields.io/readthedocs/easierscrape.svg?label=Read&nbsp;the&nbsp;Docs)](https://easierscrape.readthedocs.io)
[![Deployment](https://img.shields.io/github/deployments/dag2226/easierscrape/github-pages?label=GitHub&nbsp;Pages)](https://dag2226.github.io/easierscrape)

## Overview
easierscrape is a library which helps users do some basic web scraping operations. Oftentimes when doing webscraping code is written and re-written with slightly changed parameters to fit the website to be scraped from. This library is an easy to use tool that can scrape essentials from websites (tables, links, files, etc.). It also has the ability to generate hyperlink trees using [anytree](https://github.com/c0fec0de/anytree).

## Details
This project is a pure python project using modern tooling. It uses a `Makefile` as a command registry, with the following commands:
- `make`: list available commands
- `make develop`: install and build this library and its dependencies using `pip`
- `make build`: build the library using `setuptools`
- `make lint`: perform static analysis of this library with `flake8` and `black`
- `make format`: autoformat this library using `black`
- `make annotate`: run type checking using `mypy`
- `make test`: run automated tests with `pytest`
- `make coverage`: run automated tests with `pytest` and collect coverage information
- `make dist`: package library for distribution

## Basic Usage
Install with pip: `pip install easierscrape`

Import `Scraper` from `easierscrape` and instantiate it with a url as seen below:
```python
from easierscrape import Scraper

scraper = Scraper("https://quotes.toscrape.com/login")
```
From there, call class methods to scrape varying resources.

Usage examples:
```
>>> scraper.parse_text()
["Quotes to Scrape", "Quotes to Scrape", "Login", "Username", "Password", "Quotes by:", "GoodReads.com", "Made with", "❤", "by", "Scrapinghub",]

>>> scraper.print_tree(1)
https://toscrape.com
├── http://books.toscrape.com
├── http://quotes.toscrape.com
├── http://quotes.toscrape.com/scroll
├── http://quotes.toscrape.com/js
├── http://quotes.toscrape.com/js-delayed
├── http://quotes.toscrape.com/tableful
├── http://quotes.toscrape.com/login
├── http://quotes.toscrape.com/search.aspx
└── http://quotes.toscrape.com/random
```

## Command Line Usage
When installed, you can invoke easierscrape from the command-line to generate a hyperlink tree, get a screenshot, download all image, txt, and pdf files, and scrape any tables for a given url and depth:
```
usage: python -m easierscrape [-h] url depth

positional arguments:
  url         the url to scrape
  depth       the depth of the scrape tree

optional arguments:
  -h, --help  show this help message and exit
```
Usage example:
```
>>> python -m  easierscrape https://toscrape.com/ 1
https://toscrape.com
├── http://books.toscrape.com
├── http://quotes.toscrape.com
├── http://quotes.toscrape.com/scroll
├── http://quotes.toscrape.com/js
├── http://quotes.toscrape.com/js-delayed
├── http://quotes.toscrape.com/tableful
├── http://quotes.toscrape.com/login
├── http://quotes.toscrape.com/search.aspx
└── http://quotes.toscrape.com/random
```

## Contributing

See [CONTRIBUTING](https://github.com/dag2226/easierscrape/blob/main/CONTRIBUTING.md) for more information.

## License

This software is licensed under the Apache 2.0 license. Please see [LICENSE](https://github.com/dag2226/easierscrape/blob/main/LICENSE) for more information.
