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
from unittest.mock import patch


# UNIT TESTS=======================================================================================
def test_parse_anchors():
    assert len(parse_anchors("https://toscrape.com/")) == 13


def test_parse_files_txt():
    assert parse_files("https://www.cs.columbia.edu/~jae/", ["txt"]) == [1]


def test_parse_files_pdf():
    assert parse_files("https://www.cs.columbia.edu/~jae/", ["pdf"]) == [22]


def test_parse_files_txt_pdf():
    assert parse_files("https://www.cs.columbia.edu/~jae/", ["txt", "pdf"]) == [1, 22]


@patch('builtins.print')
def test_parse_files_without_filetype(mock_print):
    parse_files("https://toscrape.com/", [])
    assert mock_print.call_args.args == ("No filetype specified",)


def test_parse_files_without_txt_file():
    assert parse_files("https://toscrape.com/", ["txt"]) == [0]


def test_parse_images_with_image():
    assert parse_images("https://toscrape.com/") == 3


def test_parse_images_without_image():
    assert parse_images("https://quotes.toscrape.com/") == 0


def test_parse_lists():
    assert parse_lists("https://webscraper.io/test-sites/e-commerce/static") == 8


def test_parse_no_lists():
    assert parse_lists("https://toscrape.com/") == 0


def test_parse_tables():
    assert parse_tables("https://toscrape.com/") == 2


def test_parse_no_tables():
    assert parse_tables("https://quotes.toscrape.com/") == 0


def test_parse_text():
    assert parse_text("https://quotes.toscrape.com/login") == [
        "Quotes to Scrape",
        "Quotes to Scrape",
        "Login",
        "Username",
        "Password",
        "Quotes by:",
        "GoodReads.com",
        "Made with",
        "❤",
        "by",
        "Scrapinghub",
    ]


# INTEGRATION TESTS================================================================================
@patch('builtins.print')
def test_print_tree_1(mock_print):
    print_tree(tree_gen("https://toscrape.com/", 1))
    assert mock_print.call_args.args == (
        "https://toscrape.com\n├── http://books.toscrape.com\n├── http://quotes.toscrape.com\n├── http://quotes.toscrape.com/scroll\n├── http://quotes.toscrape.com/js\n├── http://quotes.toscrape.com/js-delayed\n├── http://quotes.toscrape.com/tableful\n├── http://quotes.toscrape.com/login\n├── http://quotes.toscrape.com/search.aspx\n└── http://quotes.toscrape.com/random",
    )


@patch('builtins.print')
def test_print_tree_2(mock_print):
    print_tree(tree_gen("https://toscrape.com", 0))
    assert mock_print.call_args.args == ("https://toscrape.com",)
