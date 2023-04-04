from easierscrape import Scraper
from unittest.mock import patch


scraper = Scraper()


# UNIT TESTS=======================================================================================
def test_parse_anchors():
    assert len(scraper.parse_anchors("https://toscrape.com/")) == 13


def test_parse_files_txt():
    assert scraper.parse_files("https://www.cs.columbia.edu/~jae/", ["txt"]) == [1]


def test_parse_files_pdf():
    assert scraper.parse_files("https://www.cs.columbia.edu/~jae/", ["pdf"]) == [22]


def test_parse_files_txt_pdf():
    assert scraper.parse_files("https://www.cs.columbia.edu/~jae/", ["txt", "pdf"]) == [1, 22]


@patch('builtins.print')
def test_parse_files_without_filetype(mock_print):
    scraper.parse_files("https://toscrape.com/", [])
    assert mock_print.call_args.args == ("No filetype specified",)


def test_parse_files_without_txt_file():
    assert scraper.parse_files("https://toscrape.com/", ["txt"]) == [0]


def test_parse_images_with_image():
    assert scraper.parse_images("https://toscrape.com/") == 3


def test_parse_images_without_image():
    assert scraper.parse_images("https://quotes.toscrape.com/") == 0


def test_parse_lists():
    assert scraper.parse_lists("https://webscraper.io/test-sites/e-commerce/static") == [
        [
            'Web Scraper',
            'Cloud Scraper',
            'Pricing',
            'Learn',
            'Documentation',
            'Video Tutorials',
            'How to',
            'Test Sites',
            'Forum',
            'Install',
            'Login',
        ],
        ['Documentation', 'Video Tutorials', 'How to', 'Test Sites', 'Forum'],
        ['Home', 'Phones', 'Computers'],
        ['Products', 'Web Scraper browser extension', 'Web Scraper Cloud'],
        ['Company', 'Contact', 'Website Privacy Policy', 'Browser Extension Privacy Policy', 'Media kit', 'Jobs'],
        ['Resources', 'Blog', 'Documentation', 'Video Tutorials', 'Screenshots', 'Test Sites', 'Forum'],
        ['CONTACT US', 'info@webscraper.io', 'Rupniecibas iela 30,', 'Riga, Latvia, LV-1045'],
    ]


def test_parse_no_lists():
    assert scraper.parse_lists("https://toscrape.com/") == []


def test_parse_tables():
    assert scraper.parse_tables("https://toscrape.com/") == 2


def test_parse_no_tables():
    assert scraper.parse_tables("https://quotes.toscrape.com/") == 0


def test_parse_text():
    assert scraper.parse_text("https://quotes.toscrape.com/login") == [
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
    scraper.print_tree(scraper.tree_gen("https://toscrape.com/", 1))
    assert mock_print.call_args.args == (
        "https://toscrape.com\n├── http://books.toscrape.com\n├── http://quotes.toscrape.com\n├── http://quotes.toscrape.com/scroll\n├── http://quotes.toscrape.com/js\n├── http://quotes.toscrape.com/js-delayed\n├── http://quotes.toscrape.com/tableful\n├── http://quotes.toscrape.com/login\n├── http://quotes.toscrape.com/search.aspx\n└── http://quotes.toscrape.com/random",
    )


@patch('builtins.print')
def test_print_tree_2(mock_print):
    scraper.print_tree(scraper.tree_gen("https://toscrape.com", 0))
    assert mock_print.call_args.args == ("https://toscrape.com",)


@patch('builtins.print')
def test_dynamic_tree(mock_print):
    scraper.print_tree(scraper.tree_gen("http://quotes.toscrape.com/js/", 1))
    assert mock_print.call_args.args == (
        "http://quotes.toscrape.com/js\n├── http://quotes.toscrape.com/js/login\n├── http://quotes.toscrape.com/js/js/page/2\n├── https://goodreads.com/quotes\n└── https://scrapinghub.com",
    )
