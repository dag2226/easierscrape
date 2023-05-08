# Welcome to easierscrape's documentation!

## Overview
easierscrape is a library which helps users do some basic web scraping operations. Oftentimes when doing webscraping code is written and re-written with slightly changed parameters to fit the website to be scraped from. This library is an easy to use tool that can scrape essentials from websites (tables, links, files, etc.). It also has the ability to generate hyperlink trees using [anytree](https://github.com/c0fec0de/anytree).

## Basic Usage
Install with pip: `pip install easierscrape`

Import `Scraper` from `easierscrape` and instantiate it with a url (and optionally a download_path) as seen below:
```python
from easierscrape import Scraper

scraper = Scraper("https://quotes.toscrape.com/login", "download_dir")
```
From there, call class methods to scrape varying resources.

Usage examples:
```
>>> scraper.parse_text()
["Quotes to Scrape", "Quotes to Scrape", "Login", "Username", "Password", "Quotes by:", "GoodReads.com", "Made with", "❤", "by", "Scrapinghub",]

>>> scraper.print_tree(1)
https://quotes.toscrape.com/login
├── https://quotes.toscrape.com
├── https://goodreads.com/quotes
└── https://scrapinghub.com

>>> scraper.print_tree(1, blacklist=["quotes.toscrape.com"])
https://quotes.toscrape.com/login
├── https://goodreads.com/quotes
└── https://scrapinghub.com

>>> scraper.get_screenshot()
True
```
Screenshot example:
```eval_rst
.. image:: images/screenshot.png
```

### Downloads
Using `get_screenshot`, `parse_files`, `parse_images`, or `parse_tables` will result in downloads to the `download_path` specified in the `Scraper` instantiation. If no path is specified, it will default to downloading to an "easierscrape_downloads" folder.

Usage example:
```eval_rst
.. image:: images/demo_recording.gif
```

## Command Line Usage
When installed, you can invoke easierscrape from the command-line to generate a hyperlink tree, get a screenshot, download all image, txt, and pdf files, and scrape any tables for a given url and depth:
```
usage: python -m easierscrape [-h] url depth download_path

positional arguments:
  url            the url to scrape
  depth          the depth of the scrape tree
  download_path  the location to download files to

optional arguments:
  -h, --help  show this help message and exit
```
Usage example:
```
>>> python -m  easierscrape https://toscrape.com/ 1 example_down_path
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
```eval_rst
.. image:: images/cli_recording.gif
```


```eval_rst
.. toctree::
   :maxdepth: 1
   :caption: Contents

   source/modules
```
