import easierscrape
from easierscrape.__main__ import main
from os import getcwd, listdir, makedirs
from os.path import exists, isfile, join

from unittest.mock import patch
from urllib.request import url2pathname


toscrape = easierscrape.Scraper("https://toscrape.com")
jaescrape = easierscrape.Scraper("https://www.cs.columbia.edu/~jae/", "../jaescrape")
quotescrape = easierscrape.Scraper("https://quotes.toscrape.com", "quotescrape")
webio = easierscrape.Scraper("https://webscraper.io/test-sites/e-commerce/static", "webio")
quoteslogin = easierscrape.Scraper("https://quotes.toscrape.com/login", "quoteslogin")
quotesjs = easierscrape.Scraper("http://quotes.toscrape.com/js/", "quotesjs")

toscrape.clear_downloads()
jaescrape.clear_downloads()
quotescrape.clear_downloads()
webio.clear_downloads()
quoteslogin.clear_downloads()
quotesjs.clear_downloads()


# UNIT TESTS=======================================================================================
def test_get_screenshot():
    assert toscrape.get_screenshot() == True
    assert len(listdir(join(toscrape.download_path, "images", url2pathname("https://toscrape.com")[3:]))) == 1
    assert toscrape.clear_downloads() == True


def test_parse_anchors():
    assert len(toscrape.parse_anchors()) == 13
    assert toscrape.clear_downloads() == False


def test_parse_files_txt():
    assert jaescrape.parse_files(["txt"]) == [1]
    assert (
        len(listdir(join(jaescrape.download_path, "txt", url2pathname("https://www.cs.columbia.edu/~jae/")[3:]))) == 1
    )
    assert jaescrape.clear_downloads() == True


def test_parse_files_pdf():
    assert jaescrape.parse_files(["pdf"]) == [20]
    assert (
        len(listdir(join(jaescrape.download_path, "pdf", url2pathname("https://www.cs.columbia.edu/~jae/")[3:]))) == 20
    )
    assert jaescrape.clear_downloads() == True


def test_parse_files_txt_pdf():
    assert jaescrape.parse_files(["txt", "pdf"]) == [1, 20]
    assert (
        len(listdir(join(jaescrape.download_path, "txt", url2pathname("https://www.cs.columbia.edu/~jae/")[3:]))) == 1
    )
    assert (
        len(listdir(join(jaescrape.download_path, "pdf", url2pathname("https://www.cs.columbia.edu/~jae/")[3:]))) == 20
    )
    assert jaescrape.clear_downloads() == True


@patch("builtins.print")
def test_parse_files_without_filetype(mock_print):
    toscrape.parse_files([])
    assert mock_print.call_args.args == ("No filetype specified",)
    assert toscrape.clear_downloads() == False


def test_parse_files_without_txt_file():
    assert toscrape.parse_files(["txt"]) == [0]
    assert toscrape.clear_downloads() == False


def test_parse_images_with_image():
    assert toscrape.parse_images() == 3
    assert len(listdir(join(toscrape.download_path, "images", url2pathname("https://toscrape.com")[3:]))) == 3
    assert toscrape.clear_downloads() == True


def test_parse_images_without_image():
    assert quotescrape.parse_images() == 0
    assert quotescrape.clear_downloads() == False


def test_parse_lists():
    assert webio.parse_lists() == [
        [
            "Web Scraper",
            "Cloud Scraper",
            "Pricing",
            "Learn",
            "Documentation",
            "Video Tutorials",
            "How to",
            "Test Sites",
            "Forum",
            "Install",
            "Login",
        ],
        ["Documentation", "Video Tutorials", "How to", "Test Sites", "Forum"],
        ["Home", "Phones", "Computers"],
        ["Products", "Web Scraper browser extension", "Web Scraper Cloud"],
        [
            "Company",
            "About us",
            "Contact",
            "Website Privacy Policy",
            "Browser Extension Privacy Policy",
            "Media kit",
            "Jobs",
        ],
        ["Resources", "Blog", "Documentation", "Video Tutorials", "Screenshots", "Test Sites", "Forum"],
        ["CONTACT US", "info@webscraper.io", "Ubelu 5-71,", "Adazi, Latvia, LV-2164"],
    ]
    assert webio.clear_downloads() == False


def test_parse_no_lists():
    assert toscrape.parse_lists() == []
    assert toscrape.clear_downloads() == False


def test_parse_tables_to_csv():
    assert toscrape.parse_tables() == 2
    assert len(listdir(join(toscrape.download_path, "tables", url2pathname("https://toscrape.com")[3:]))) == 2
    assert toscrape.clear_downloads() == True


def test_parse_tables_to_xlsx():
    assert toscrape.parse_tables("xlsx") == 2
    assert len(listdir(join(toscrape.download_path, "tables", url2pathname("https://toscrape.com")[3:]))) == 1
    assert toscrape.clear_downloads() == True


def test_parse_no_tables():
    assert quotescrape.parse_tables() == 0
    assert quotescrape.clear_downloads() == False


@patch("builtins.print")
def test_parse_tables_to_unsupported_type(mock_print):
    assert toscrape.parse_tables("unsup") == 2
    assert mock_print.call_args.args == (
        "output_type = unsup not implemented.\nCurrently supported filetypes are csv and xlsx.",
    )
    assert toscrape.clear_downloads() == False


def test_parse_text():
    assert quoteslogin.parse_text() == [
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
    assert quoteslogin.clear_downloads() == False


# INTEGRATION TESTS================================================================================
@patch("builtins.print")
def test_print_tree_depth_0(mock_print):
    toscrape.print_tree(0)
    assert mock_print.call_args.args == ("https://toscrape.com",)
    assert toscrape.clear_downloads() == False


@patch("builtins.print")
def test_print_tree_depth_1(mock_print):
    toscrape.print_tree(1)
    assert mock_print.call_args.args == (
        "https://toscrape.com\n├── http://books.toscrape.com\n├── http://quotes.toscrape.com\n├── http://quotes.toscrape.com/scroll\n├── http://quotes.toscrape.com/js\n├── http://quotes.toscrape.com/js-delayed\n├── http://quotes.toscrape.com/tableful\n├── http://quotes.toscrape.com/login\n├── http://quotes.toscrape.com/search.aspx\n└── http://quotes.toscrape.com/random",
    )
    assert toscrape.clear_downloads() == False


@patch("builtins.print")
def test_print_tree_depth_2(mock_print):
    quotescrape.print_tree(2)
    assert mock_print.call_args.args == (
        "https://quotes.toscrape.com\n├── https://quotes.toscrape.com/login\n│   ├── https://goodreads.com/quotes\n│   └── https://scrapinghub.com\n├── https://quotes.toscrape.com/author/Albert-Einstein\n├── https://quotes.toscrape.com/tag/change/page/1\n│   ├── https://quotes.toscrape.com/tag/deep-thoughts/page/1\n│   ├── https://quotes.toscrape.com/tag/thinking/page/1\n│   ├── https://quotes.toscrape.com/tag/world/page/1\n│   ├── https://quotes.toscrape.com/tag/love\n│   ├── https://quotes.toscrape.com/tag/inspirational\n│   ├── https://quotes.toscrape.com/tag/life\n│   ├── https://quotes.toscrape.com/tag/humor\n│   ├── https://quotes.toscrape.com/tag/books\n│   ├── https://quotes.toscrape.com/tag/reading\n│   ├── https://quotes.toscrape.com/tag/friendship\n│   ├── https://quotes.toscrape.com/tag/friends\n│   ├── https://quotes.toscrape.com/tag/truth\n│   └── https://quotes.toscrape.com/tag/simile\n├── https://quotes.toscrape.com/author/J-K-Rowling\n├── https://quotes.toscrape.com/tag/abilities/page/1\n│   └── https://quotes.toscrape.com/tag/choices/page/1\n├── https://quotes.toscrape.com/tag/inspirational/page/1\n│   ├── https://quotes.toscrape.com/tag/life/page/1\n│   ├── https://quotes.toscrape.com/tag/live/page/1\n│   ├── https://quotes.toscrape.com/tag/miracle/page/1\n│   ├── https://quotes.toscrape.com/tag/miracles/page/1\n│   ├── https://quotes.toscrape.com/author/Marilyn-Monroe\n│   ├── https://quotes.toscrape.com/tag/be-yourself/page/1\n│   ├── https://quotes.toscrape.com/author/Thomas-A-Edison\n│   ├── https://quotes.toscrape.com/tag/edison/page/1\n│   ├── https://quotes.toscrape.com/tag/failure/page/1\n│   ├── https://quotes.toscrape.com/tag/paraphrased/page/1\n│   ├── https://quotes.toscrape.com/tag/friends/page/1\n│   ├── https://quotes.toscrape.com/tag/heartbreak/page/1\n│   ├── https://quotes.toscrape.com/tag/love/page/1\n│   ├── https://quotes.toscrape.com/tag/sisters/page/1\n│   ├── https://quotes.toscrape.com/author/Elie-Wiesel\n│   ├── https://quotes.toscrape.com/tag/activism/page/1\n│   ├── https://quotes.toscrape.com/tag/apathy/page/1\n│   ├── https://quotes.toscrape.com/tag/hate/page/1\n│   ├── https://quotes.toscrape.com/tag/indifference/page/1\n│   ├── https://quotes.toscrape.com/tag/opposite/page/1\n│   ├── https://quotes.toscrape.com/tag/philosophy/page/1\n│   ├── https://quotes.toscrape.com/tag/death/page/1\n│   ├── https://quotes.toscrape.com/author/George-Eliot\n│   ├── https://quotes.toscrape.com/author/C-S-Lewis\n│   ├── https://quotes.toscrape.com/tag/books/page/1\n│   ├── https://quotes.toscrape.com/tag/reading/page/1\n│   ├── https://quotes.toscrape.com/tag/tea/page/1\n│   ├── https://quotes.toscrape.com/author/Martin-Luther-King-Jr\n│   ├── https://quotes.toscrape.com/tag/hope/page/1\n│   ├── https://quotes.toscrape.com/author/Helen-Keller\n│   └── https://quotes.toscrape.com/tag/inspirational/page/2\n├── https://quotes.toscrape.com/author/Jane-Austen\n├── https://quotes.toscrape.com/tag/aliteracy/page/1\n│   ├── https://quotes.toscrape.com/tag/classic/page/1\n│   └── https://quotes.toscrape.com/tag/humor/page/1\n├── https://quotes.toscrape.com/tag/adulthood/page/1\n│   ├── https://quotes.toscrape.com/tag/success/page/1\n│   └── https://quotes.toscrape.com/tag/value/page/1\n├── https://quotes.toscrape.com/author/Andre-Gide\n├── https://quotes.toscrape.com/author/Eleanor-Roosevelt\n├── https://quotes.toscrape.com/tag/misattributed-eleanor-roosevelt/page/1\n├── https://quotes.toscrape.com/author/Steve-Martin\n├── https://quotes.toscrape.com/tag/obvious/page/1\n│   └── https://quotes.toscrape.com/tag/simile/page/1\n└── https://quotes.toscrape.com/page/2\n    ├── https://quotes.toscrape.com/tag/courage/page/1\n    ├── https://quotes.toscrape.com/tag/simplicity/page/1\n    ├── https://quotes.toscrape.com/tag/understand/page/1\n    ├── https://quotes.toscrape.com/author/Bob-Marley\n    ├── https://quotes.toscrape.com/author/Dr-Seuss\n    ├── https://quotes.toscrape.com/tag/fantasy/page/1\n    ├── https://quotes.toscrape.com/author/Douglas-Adams\n    ├── https://quotes.toscrape.com/tag/navigation/page/1\n    ├── https://quotes.toscrape.com/author/Friedrich-Nietzsche\n    ├── https://quotes.toscrape.com/tag/friendship/page/1\n    ├── https://quotes.toscrape.com/tag/lack-of-friendship/page/1\n    ├── https://quotes.toscrape.com/tag/lack-of-love/page/1\n    ├── https://quotes.toscrape.com/tag/marriage/page/1\n    ├── https://quotes.toscrape.com/tag/unhappy-marriage/page/1\n    ├── https://quotes.toscrape.com/author/Mark-Twain\n    ├── https://quotes.toscrape.com/tag/contentment/page/1\n    ├── https://quotes.toscrape.com/author/Allen-Saunders\n    ├── https://quotes.toscrape.com/tag/fate/page/1\n    ├── https://quotes.toscrape.com/tag/misattributed-john-lennon/page/1\n    ├── https://quotes.toscrape.com/tag/planning/page/1\n    ├── https://quotes.toscrape.com/tag/plans/page/1\n    ├── https://quotes.toscrape.com/page/1\n    └── https://quotes.toscrape.com/page/3",
    )
    assert quotescrape.clear_downloads() == False


@patch("builtins.print")
def test_print_tree_dynamic_website_depth_1(mock_print):
    quotesjs.print_tree(1)
    assert mock_print.call_args.args == (
        "http://quotes.toscrape.com/js\n├── http://quotes.toscrape.com\n├── http://quotes.toscrape.com/login\n├── http://quotes.toscrape.com/js/page/2\n├── https://goodreads.com/quotes\n└── https://scrapinghub.com",
    )
    assert quotesjs.clear_downloads() == False


@patch("builtins.print")
def test_print_tree_blacklist_website_depth_1(mock_print):
    toscrape.print_tree(1, blacklist=["quotes.toscrape.com"])
    assert mock_print.call_args.args == ("https://toscrape.com\n└── http://books.toscrape.com",)
    assert toscrape.clear_downloads() == False


@patch("builtins.print")
def test_print_tree_multiple_blacklist_website_depth_2(mock_print):
    quotescrape.print_tree(2, blacklist=["goodreads.com", "scrapinghub.com"])
    assert mock_print.call_args.args == (
        "https://quotes.toscrape.com\n├── https://quotes.toscrape.com/login\n├── https://quotes.toscrape.com/author/Albert-Einstein\n├── https://quotes.toscrape.com/tag/change/page/1\n│   ├── https://quotes.toscrape.com/tag/deep-thoughts/page/1\n│   ├── https://quotes.toscrape.com/tag/thinking/page/1\n│   ├── https://quotes.toscrape.com/tag/world/page/1\n│   ├── https://quotes.toscrape.com/tag/love\n│   ├── https://quotes.toscrape.com/tag/inspirational\n│   ├── https://quotes.toscrape.com/tag/life\n│   ├── https://quotes.toscrape.com/tag/humor\n│   ├── https://quotes.toscrape.com/tag/books\n│   ├── https://quotes.toscrape.com/tag/reading\n│   ├── https://quotes.toscrape.com/tag/friendship\n│   ├── https://quotes.toscrape.com/tag/friends\n│   ├── https://quotes.toscrape.com/tag/truth\n│   └── https://quotes.toscrape.com/tag/simile\n├── https://quotes.toscrape.com/author/J-K-Rowling\n├── https://quotes.toscrape.com/tag/abilities/page/1\n│   └── https://quotes.toscrape.com/tag/choices/page/1\n├── https://quotes.toscrape.com/tag/inspirational/page/1\n│   ├── https://quotes.toscrape.com/tag/life/page/1\n│   ├── https://quotes.toscrape.com/tag/live/page/1\n│   ├── https://quotes.toscrape.com/tag/miracle/page/1\n│   ├── https://quotes.toscrape.com/tag/miracles/page/1\n│   ├── https://quotes.toscrape.com/author/Marilyn-Monroe\n│   ├── https://quotes.toscrape.com/tag/be-yourself/page/1\n│   ├── https://quotes.toscrape.com/author/Thomas-A-Edison\n│   ├── https://quotes.toscrape.com/tag/edison/page/1\n│   ├── https://quotes.toscrape.com/tag/failure/page/1\n│   ├── https://quotes.toscrape.com/tag/paraphrased/page/1\n│   ├── https://quotes.toscrape.com/tag/friends/page/1\n│   ├── https://quotes.toscrape.com/tag/heartbreak/page/1\n│   ├── https://quotes.toscrape.com/tag/love/page/1\n│   ├── https://quotes.toscrape.com/tag/sisters/page/1\n│   ├── https://quotes.toscrape.com/author/Elie-Wiesel\n│   ├── https://quotes.toscrape.com/tag/activism/page/1\n│   ├── https://quotes.toscrape.com/tag/apathy/page/1\n│   ├── https://quotes.toscrape.com/tag/hate/page/1\n│   ├── https://quotes.toscrape.com/tag/indifference/page/1\n│   ├── https://quotes.toscrape.com/tag/opposite/page/1\n│   ├── https://quotes.toscrape.com/tag/philosophy/page/1\n│   ├── https://quotes.toscrape.com/tag/death/page/1\n│   ├── https://quotes.toscrape.com/author/George-Eliot\n│   ├── https://quotes.toscrape.com/author/C-S-Lewis\n│   ├── https://quotes.toscrape.com/tag/books/page/1\n│   ├── https://quotes.toscrape.com/tag/reading/page/1\n│   ├── https://quotes.toscrape.com/tag/tea/page/1\n│   ├── https://quotes.toscrape.com/author/Martin-Luther-King-Jr\n│   ├── https://quotes.toscrape.com/tag/hope/page/1\n│   ├── https://quotes.toscrape.com/author/Helen-Keller\n│   └── https://quotes.toscrape.com/tag/inspirational/page/2\n├── https://quotes.toscrape.com/author/Jane-Austen\n├── https://quotes.toscrape.com/tag/aliteracy/page/1\n│   ├── https://quotes.toscrape.com/tag/classic/page/1\n│   └── https://quotes.toscrape.com/tag/humor/page/1\n├── https://quotes.toscrape.com/tag/adulthood/page/1\n│   ├── https://quotes.toscrape.com/tag/success/page/1\n│   └── https://quotes.toscrape.com/tag/value/page/1\n├── https://quotes.toscrape.com/author/Andre-Gide\n├── https://quotes.toscrape.com/author/Eleanor-Roosevelt\n├── https://quotes.toscrape.com/tag/misattributed-eleanor-roosevelt/page/1\n├── https://quotes.toscrape.com/author/Steve-Martin\n├── https://quotes.toscrape.com/tag/obvious/page/1\n│   └── https://quotes.toscrape.com/tag/simile/page/1\n└── https://quotes.toscrape.com/page/2\n    ├── https://quotes.toscrape.com/tag/courage/page/1\n    ├── https://quotes.toscrape.com/tag/simplicity/page/1\n    ├── https://quotes.toscrape.com/tag/understand/page/1\n    ├── https://quotes.toscrape.com/author/Bob-Marley\n    ├── https://quotes.toscrape.com/author/Dr-Seuss\n    ├── https://quotes.toscrape.com/tag/fantasy/page/1\n    ├── https://quotes.toscrape.com/author/Douglas-Adams\n    ├── https://quotes.toscrape.com/tag/navigation/page/1\n    ├── https://quotes.toscrape.com/author/Friedrich-Nietzsche\n    ├── https://quotes.toscrape.com/tag/friendship/page/1\n    ├── https://quotes.toscrape.com/tag/lack-of-friendship/page/1\n    ├── https://quotes.toscrape.com/tag/lack-of-love/page/1\n    ├── https://quotes.toscrape.com/tag/marriage/page/1\n    ├── https://quotes.toscrape.com/tag/unhappy-marriage/page/1\n    ├── https://quotes.toscrape.com/author/Mark-Twain\n    ├── https://quotes.toscrape.com/tag/contentment/page/1\n    ├── https://quotes.toscrape.com/author/Allen-Saunders\n    ├── https://quotes.toscrape.com/tag/fate/page/1\n    ├── https://quotes.toscrape.com/tag/misattributed-john-lennon/page/1\n    ├── https://quotes.toscrape.com/tag/planning/page/1\n    ├── https://quotes.toscrape.com/tag/plans/page/1\n    ├── https://quotes.toscrape.com/page/1\n    └── https://quotes.toscrape.com/page/3",
    )
    assert quotescrape.clear_downloads() == False


@patch("builtins.print")
def test_print_tree_whitelist_website_depth_1(mock_print):
    toscrape.print_tree(1, whitelist=["quotes.toscrape.com"])
    assert mock_print.call_args.args == (
        "https://toscrape.com\n├── http://quotes.toscrape.com\n├── http://quotes.toscrape.com/scroll\n├── http://quotes.toscrape.com/js\n├── http://quotes.toscrape.com/js-delayed\n├── http://quotes.toscrape.com/tableful\n├── http://quotes.toscrape.com/login\n├── http://quotes.toscrape.com/search.aspx\n└── http://quotes.toscrape.com/random",
    )
    assert toscrape.clear_downloads() == False


@patch("builtins.print")
def test_print_tree_multiple_whitelist_website_depth_2(mock_print):
    quotescrape.print_tree(2, whitelist=["quotes.toscrape.com", "goodreads.com"])
    assert mock_print.call_args.args == (
        "https://quotes.toscrape.com\n├── https://quotes.toscrape.com/login\n│   └── https://goodreads.com/quotes\n├── https://quotes.toscrape.com/author/Albert-Einstein\n├── https://quotes.toscrape.com/tag/change/page/1\n│   ├── https://quotes.toscrape.com/tag/deep-thoughts/page/1\n│   ├── https://quotes.toscrape.com/tag/thinking/page/1\n│   ├── https://quotes.toscrape.com/tag/world/page/1\n│   ├── https://quotes.toscrape.com/tag/love\n│   ├── https://quotes.toscrape.com/tag/inspirational\n│   ├── https://quotes.toscrape.com/tag/life\n│   ├── https://quotes.toscrape.com/tag/humor\n│   ├── https://quotes.toscrape.com/tag/books\n│   ├── https://quotes.toscrape.com/tag/reading\n│   ├── https://quotes.toscrape.com/tag/friendship\n│   ├── https://quotes.toscrape.com/tag/friends\n│   ├── https://quotes.toscrape.com/tag/truth\n│   └── https://quotes.toscrape.com/tag/simile\n├── https://quotes.toscrape.com/author/J-K-Rowling\n├── https://quotes.toscrape.com/tag/abilities/page/1\n│   └── https://quotes.toscrape.com/tag/choices/page/1\n├── https://quotes.toscrape.com/tag/inspirational/page/1\n│   ├── https://quotes.toscrape.com/tag/life/page/1\n│   ├── https://quotes.toscrape.com/tag/live/page/1\n│   ├── https://quotes.toscrape.com/tag/miracle/page/1\n│   ├── https://quotes.toscrape.com/tag/miracles/page/1\n│   ├── https://quotes.toscrape.com/author/Marilyn-Monroe\n│   ├── https://quotes.toscrape.com/tag/be-yourself/page/1\n│   ├── https://quotes.toscrape.com/author/Thomas-A-Edison\n│   ├── https://quotes.toscrape.com/tag/edison/page/1\n│   ├── https://quotes.toscrape.com/tag/failure/page/1\n│   ├── https://quotes.toscrape.com/tag/paraphrased/page/1\n│   ├── https://quotes.toscrape.com/tag/friends/page/1\n│   ├── https://quotes.toscrape.com/tag/heartbreak/page/1\n│   ├── https://quotes.toscrape.com/tag/love/page/1\n│   ├── https://quotes.toscrape.com/tag/sisters/page/1\n│   ├── https://quotes.toscrape.com/author/Elie-Wiesel\n│   ├── https://quotes.toscrape.com/tag/activism/page/1\n│   ├── https://quotes.toscrape.com/tag/apathy/page/1\n│   ├── https://quotes.toscrape.com/tag/hate/page/1\n│   ├── https://quotes.toscrape.com/tag/indifference/page/1\n│   ├── https://quotes.toscrape.com/tag/opposite/page/1\n│   ├── https://quotes.toscrape.com/tag/philosophy/page/1\n│   ├── https://quotes.toscrape.com/tag/death/page/1\n│   ├── https://quotes.toscrape.com/author/George-Eliot\n│   ├── https://quotes.toscrape.com/author/C-S-Lewis\n│   ├── https://quotes.toscrape.com/tag/books/page/1\n│   ├── https://quotes.toscrape.com/tag/reading/page/1\n│   ├── https://quotes.toscrape.com/tag/tea/page/1\n│   ├── https://quotes.toscrape.com/author/Martin-Luther-King-Jr\n│   ├── https://quotes.toscrape.com/tag/hope/page/1\n│   ├── https://quotes.toscrape.com/author/Helen-Keller\n│   └── https://quotes.toscrape.com/tag/inspirational/page/2\n├── https://quotes.toscrape.com/author/Jane-Austen\n├── https://quotes.toscrape.com/tag/aliteracy/page/1\n│   ├── https://quotes.toscrape.com/tag/classic/page/1\n│   └── https://quotes.toscrape.com/tag/humor/page/1\n├── https://quotes.toscrape.com/tag/adulthood/page/1\n│   ├── https://quotes.toscrape.com/tag/success/page/1\n│   └── https://quotes.toscrape.com/tag/value/page/1\n├── https://quotes.toscrape.com/author/Andre-Gide\n├── https://quotes.toscrape.com/author/Eleanor-Roosevelt\n├── https://quotes.toscrape.com/tag/misattributed-eleanor-roosevelt/page/1\n├── https://quotes.toscrape.com/author/Steve-Martin\n├── https://quotes.toscrape.com/tag/obvious/page/1\n│   └── https://quotes.toscrape.com/tag/simile/page/1\n└── https://quotes.toscrape.com/page/2\n    ├── https://quotes.toscrape.com/tag/courage/page/1\n    ├── https://quotes.toscrape.com/tag/simplicity/page/1\n    ├── https://quotes.toscrape.com/tag/understand/page/1\n    ├── https://quotes.toscrape.com/author/Bob-Marley\n    ├── https://quotes.toscrape.com/author/Dr-Seuss\n    ├── https://quotes.toscrape.com/tag/fantasy/page/1\n    ├── https://quotes.toscrape.com/author/Douglas-Adams\n    ├── https://quotes.toscrape.com/tag/navigation/page/1\n    ├── https://quotes.toscrape.com/author/Friedrich-Nietzsche\n    ├── https://quotes.toscrape.com/tag/friendship/page/1\n    ├── https://quotes.toscrape.com/tag/lack-of-friendship/page/1\n    ├── https://quotes.toscrape.com/tag/lack-of-love/page/1\n    ├── https://quotes.toscrape.com/tag/marriage/page/1\n    ├── https://quotes.toscrape.com/tag/unhappy-marriage/page/1\n    ├── https://quotes.toscrape.com/author/Mark-Twain\n    ├── https://quotes.toscrape.com/tag/contentment/page/1\n    ├── https://quotes.toscrape.com/author/Allen-Saunders\n    ├── https://quotes.toscrape.com/tag/fate/page/1\n    ├── https://quotes.toscrape.com/tag/misattributed-john-lennon/page/1\n    ├── https://quotes.toscrape.com/tag/planning/page/1\n    ├── https://quotes.toscrape.com/tag/plans/page/1\n    ├── https://quotes.toscrape.com/page/1\n    └── https://quotes.toscrape.com/page/3",
    )
    assert quotescrape.clear_downloads() == False


@patch("builtins.print")
def test_main(mock_print):
    cli_args = ["https://toscrape.com", "1", "easierscrape_downloads"]
    main_out = main(cli_args)
    assert mock_print.call_args.args == (
        "https://toscrape.com\n├── http://books.toscrape.com\n├── http://quotes.toscrape.com\n├── http://quotes.toscrape.com/scroll\n├── http://quotes.toscrape.com/js\n├── http://quotes.toscrape.com/js-delayed\n├── http://quotes.toscrape.com/tableful\n├── http://quotes.toscrape.com/login\n├── http://quotes.toscrape.com/search.aspx\n└── http://quotes.toscrape.com/random",
    )
    assert main_out[0]
    assert main_out[1] == 3
    assert len(listdir(join(toscrape.download_path, "images", url2pathname("https://toscrape.com")[3:]))) == 4
    assert main_out[2] == [0, 0]
    assert main_out[3] == 2
    assert len(listdir(join(toscrape.download_path, "tables", url2pathname("https://toscrape.com")[3:]))) == 2
    assert toscrape.clear_downloads() == True


@patch("builtins.print")
def test_main_dynamic_website(mock_print):
    cli_args = ["http://quotes.toscrape.com/js/", "1", "quotesjs"]
    main_out = main(cli_args)
    assert mock_print.call_args.args == (
        "http://quotes.toscrape.com/js\n├── http://quotes.toscrape.com\n├── http://quotes.toscrape.com/login\n├── http://quotes.toscrape.com/js/page/2\n├── https://goodreads.com/quotes\n└── https://scrapinghub.com",
    )
    assert main_out[0]
    assert len(listdir(join(quotesjs.download_path, "images", url2pathname("http://quotes.toscrape.com/js/")[3:]))) == 1
    assert main_out[1] == 0
    assert main_out[2] == [0, 0]
    assert main_out[3] == 0
    assert quotesjs.clear_downloads() == True
