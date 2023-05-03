# Welcome to easierscrape's documentation!

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

### Downloads
Using `get_screenshot`, `parse_files`, `parse_images`, or `parse_tables` will result in an "easierscrape_downloads" directory being created in the working directory.

Usage example:
```eval_rst
.. image:: images/demo_recording.gif
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
└── http://quotes.toscrape.com/random"
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
