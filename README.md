# easierscrape

A library for basic web scraping.

[![PyPI](https://img.shields.io/pypi/v/easierscrape)](https://pypi.org/project/easierscrape/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![Issues](https://img.shields.io/github/issues/dag2226/easierscrape)](https://github.com/dag2226/easierscrape/issues)
[![Build Status](https://github.com/dag2226/easierscrape/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/dag2226/easierscrape/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/dag2226/easierscrape/branch/main/graph/badge.svg)](https://codecov.io/gh/dag2226/easierscrape)

## Overview
easierscrape is a library which helps users do some basic web scraping operations. Oftentimes when doing webscraping code is written and re-written with slightly changed parameters to fit the website to be scraped from. This library is an easy to use tool that can scrape essentials from websites (tables, links, files, etc.). It also has the ability to generate hyperlink trees.

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

Import needed methods from `easierscrape` as seen below:
```
from easierscrape import (
    parse_anchors,
    parse_files,
    parse_images,
	parse_lists,
    parse_tables,
	parse_text,
    print_tree,
    tree_gen,
)
```
`parse_anchors`
- Takes in one argument: The `url` to scrape from
- Returns a list of anchor tag references

`parse_files`
- Takes in two arguments:
  - The `url` to scrape from
  - A `List` of file extensions to parse (ex: `['pdf', 'txt']`)
- Downloads results to an `easierscrape_downloads` folder in the current working directory

`parse_images`
- Takes in one argument: The `url` to scrape from
- Downloads results to an `easierscrape_downloads` folder in the current working directory

`parse_lists`
- Takes in one argument: The `url` to scrape from
- Downloads results to an `easierscrape_downloads` folder in the current working directory

`parse_tables`
- Takes in one argument: The `url` to scrape from
- Downloads results to an `easierscrape_downloads` folder in the current working directory

`parse_text`
- Takes in one argument: The `url` to scrape from
- Returns a list of strings from the website's text content

`print_tree`
- Takes in an [anytree](https://github.com/c0fec0de/anytree) `Node` structure (head of a tree)
- Prints the tree

`tree_gen`
- Takes in two arguments;
  - The head `url` to scrape from
  - The `maxdepth` to scrape until
- Returns the head [anytree](https://github.com/c0fec0de/anytree) `Node` of a generated scrape tree

## Command Line Usage
When installed, you can invoke easierscrape from the command-line to generate a hyperlink tree:
```
usage: easierscrape [-h] url depth

positional arguments:
  url         the url to scrape
  depth       the depth of the scrape tree

optional arguments:
  -h, --help  show this help message and exit
```
