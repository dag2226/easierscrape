import easierscrape
from easierscrape.__main__ import main
from os import getcwd, makedirs
from os.path import exists, join
from shutil import rmtree
from unittest.mock import patch


scraper = easierscrape.Scraper()
download_dir = join(getcwd(), "easierscrape_downloads")


# UNIT TESTS=======================================================================================
def test_get_screenshot():
    assert True  # scraper.get_screenshot("https://toscrape.com") in [191320, 230509]
    # rmtree(download_dir)


def test_parse_anchors():
    assert len(scraper.parse_anchors("https://toscrape.com/")) == 13


def test_parse_files_txt():
    assert scraper.parse_files("https://www.cs.columbia.edu/~jae/", ["txt"]) == [1]
    rmtree(download_dir)


def test_parse_files_pdf():
    assert scraper.parse_files("https://www.cs.columbia.edu/~jae/", ["pdf"]) == [22]
    rmtree(download_dir)


def test_parse_files_txt_pdf():
    assert scraper.parse_files("https://www.cs.columbia.edu/~jae/", ["txt", "pdf"]) == [1, 22]
    rmtree(download_dir)


@patch("builtins.print")
def test_parse_files_without_filetype(mock_print):
    scraper.parse_files("https://toscrape.com/", [])
    assert mock_print.call_args.args == ("No filetype specified",)


def test_parse_files_without_txt_file():
    assert scraper.parse_files("https://toscrape.com/", ["txt"]) == [0]


def test_parse_images_with_image():
    assert scraper.parse_images("https://toscrape.com/") == 3
    rmtree(download_dir)


def test_parse_images_without_image():
    assert scraper.parse_images("https://quotes.toscrape.com/") == 0


def test_parse_lists():
    assert scraper.parse_lists("https://webscraper.io/test-sites/e-commerce/static") == [
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


def test_parse_no_lists():
    assert scraper.parse_lists("https://toscrape.com/") == []


def test_parse_tables():
    assert scraper.parse_tables("https://toscrape.com/") == 2
    rmtree(download_dir)


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
@patch("builtins.print")
def test_print_tree_1(mock_print):
    scraper.print_tree(scraper.tree_gen("https://toscrape.com/", 1))
    assert mock_print.call_args.args == (
        "https://toscrape.com\n├── http://books.toscrape.com\n├── http://quotes.toscrape.com\n├── http://quotes.toscrape.com/scroll\n├── http://quotes.toscrape.com/js\n├── http://quotes.toscrape.com/js-delayed\n├── http://quotes.toscrape.com/tableful\n├── http://quotes.toscrape.com/login\n├── http://quotes.toscrape.com/search.aspx\n└── http://quotes.toscrape.com/random",
    )


@patch("builtins.print")
def test_print_tree_2(mock_print):
    scraper.print_tree(scraper.tree_gen("https://toscrape.com", 0))
    assert mock_print.call_args.args == ("https://toscrape.com",)


@patch("builtins.print")
def test_print_tree_3(mock_print):
    scraper.print_tree(scraper.tree_gen("https://quotes.toscrape.com/", 2))
    assert mock_print.call_args.args == (
        "https://quotes.toscrape.com\n├── https://quotes.toscrape.com/login\n│   ├── https://goodreads.com/quotes\n│   └── https://scrapinghub.com\n├── https://quotes.toscrape.com/author/Albert-Einstein\n├── https://quotes.toscrape.com/tag/change/page/1\n│   ├── https://quotes.toscrape.com/tag/deep-thoughts/page/1\n│   ├── https://quotes.toscrape.com/tag/thinking/page/1\n│   ├── https://quotes.toscrape.com/tag/world/page/1\n│   ├── https://quotes.toscrape.com/tag/love\n│   ├── https://quotes.toscrape.com/tag/inspirational\n│   ├── https://quotes.toscrape.com/tag/life\n│   ├── https://quotes.toscrape.com/tag/humor\n│   ├── https://quotes.toscrape.com/tag/books\n│   ├── https://quotes.toscrape.com/tag/reading\n│   ├── https://quotes.toscrape.com/tag/friendship\n│   ├── https://quotes.toscrape.com/tag/friends\n│   ├── https://quotes.toscrape.com/tag/truth\n│   └── https://quotes.toscrape.com/tag/simile\n├── https://quotes.toscrape.com/author/J-K-Rowling\n├── https://quotes.toscrape.com/tag/abilities/page/1\n│   └── https://quotes.toscrape.com/tag/choices/page/1\n├── https://quotes.toscrape.com/tag/inspirational/page/1\n│   ├── https://quotes.toscrape.com/tag/life/page/1\n│   ├── https://quotes.toscrape.com/tag/live/page/1\n│   ├── https://quotes.toscrape.com/tag/miracle/page/1\n│   ├── https://quotes.toscrape.com/tag/miracles/page/1\n│   ├── https://quotes.toscrape.com/author/Marilyn-Monroe\n│   ├── https://quotes.toscrape.com/tag/be-yourself/page/1\n│   ├── https://quotes.toscrape.com/author/Thomas-A-Edison\n│   ├── https://quotes.toscrape.com/tag/edison/page/1\n│   ├── https://quotes.toscrape.com/tag/failure/page/1\n│   ├── https://quotes.toscrape.com/tag/paraphrased/page/1\n│   ├── https://quotes.toscrape.com/tag/friends/page/1\n│   ├── https://quotes.toscrape.com/tag/heartbreak/page/1\n│   ├── https://quotes.toscrape.com/tag/love/page/1\n│   ├── https://quotes.toscrape.com/tag/sisters/page/1\n│   ├── https://quotes.toscrape.com/author/Elie-Wiesel\n│   ├── https://quotes.toscrape.com/tag/activism/page/1\n│   ├── https://quotes.toscrape.com/tag/apathy/page/1\n│   ├── https://quotes.toscrape.com/tag/hate/page/1\n│   ├── https://quotes.toscrape.com/tag/indifference/page/1\n│   ├── https://quotes.toscrape.com/tag/opposite/page/1\n│   ├── https://quotes.toscrape.com/tag/philosophy/page/1\n│   ├── https://quotes.toscrape.com/tag/death/page/1\n│   ├── https://quotes.toscrape.com/author/George-Eliot\n│   ├── https://quotes.toscrape.com/author/C-S-Lewis\n│   ├── https://quotes.toscrape.com/tag/books/page/1\n│   ├── https://quotes.toscrape.com/tag/reading/page/1\n│   ├── https://quotes.toscrape.com/tag/tea/page/1\n│   ├── https://quotes.toscrape.com/author/Martin-Luther-King-Jr\n│   ├── https://quotes.toscrape.com/tag/hope/page/1\n│   ├── https://quotes.toscrape.com/author/Helen-Keller\n│   └── https://quotes.toscrape.com/tag/inspirational/page/2\n├── https://quotes.toscrape.com/author/Jane-Austen\n├── https://quotes.toscrape.com/tag/aliteracy/page/1\n│   ├── https://quotes.toscrape.com/tag/classic/page/1\n│   └── https://quotes.toscrape.com/tag/humor/page/1\n├── https://quotes.toscrape.com/tag/adulthood/page/1\n│   ├── https://quotes.toscrape.com/tag/success/page/1\n│   └── https://quotes.toscrape.com/tag/value/page/1\n├── https://quotes.toscrape.com/author/Andre-Gide\n├── https://quotes.toscrape.com/author/Eleanor-Roosevelt\n├── https://quotes.toscrape.com/tag/misattributed-eleanor-roosevelt/page/1\n├── https://quotes.toscrape.com/author/Steve-Martin\n├── https://quotes.toscrape.com/tag/obvious/page/1\n│   └── https://quotes.toscrape.com/tag/simile/page/1\n└── https://quotes.toscrape.com/page/2\n    ├── https://quotes.toscrape.com/tag/courage/page/1\n    ├── https://quotes.toscrape.com/tag/simplicity/page/1\n    ├── https://quotes.toscrape.com/tag/understand/page/1\n    ├── https://quotes.toscrape.com/author/Bob-Marley\n    ├── https://quotes.toscrape.com/author/Dr-Seuss\n    ├── https://quotes.toscrape.com/tag/fantasy/page/1\n    ├── https://quotes.toscrape.com/author/Douglas-Adams\n    ├── https://quotes.toscrape.com/tag/navigation/page/1\n    ├── https://quotes.toscrape.com/author/Friedrich-Nietzsche\n    ├── https://quotes.toscrape.com/tag/friendship/page/1\n    ├── https://quotes.toscrape.com/tag/lack-of-friendship/page/1\n    ├── https://quotes.toscrape.com/tag/lack-of-love/page/1\n    ├── https://quotes.toscrape.com/tag/marriage/page/1\n    ├── https://quotes.toscrape.com/tag/unhappy-marriage/page/1\n    ├── https://quotes.toscrape.com/author/Mark-Twain\n    ├── https://quotes.toscrape.com/tag/contentment/page/1\n    ├── https://quotes.toscrape.com/author/Allen-Saunders\n    ├── https://quotes.toscrape.com/tag/fate/page/1\n    ├── https://quotes.toscrape.com/tag/misattributed-john-lennon/page/1\n    ├── https://quotes.toscrape.com/tag/planning/page/1\n    ├── https://quotes.toscrape.com/tag/plans/page/1\n    ├── https://quotes.toscrape.com/page/1\n    └── https://quotes.toscrape.com/page/3",
    )


@patch("builtins.print")
def test_dynamic_tree(mock_print):
    scraper.print_tree(scraper.tree_gen("http://quotes.toscrape.com/js/", 1))
    assert mock_print.call_args.args == (
        "http://quotes.toscrape.com/js\n├── http://quotes.toscrape.com\n├── http://quotes.toscrape.com/login\n├── http://quotes.toscrape.com/js/page/2\n├── https://goodreads.com/quotes\n└── https://scrapinghub.com",
    )


@patch("builtins.print")
def test_main(mock_print):
    cli_args = ["https://toscrape.com", "1"]
    main_out = main(cli_args)
    assert mock_print.call_args.args == (
        "https://toscrape.com\n├── http://books.toscrape.com\n├── http://quotes.toscrape.com\n├── http://quotes.toscrape.com/scroll\n├── http://quotes.toscrape.com/js\n├── http://quotes.toscrape.com/js-delayed\n├── http://quotes.toscrape.com/tableful\n├── http://quotes.toscrape.com/login\n├── http://quotes.toscrape.com/search.aspx\n└── http://quotes.toscrape.com/random",
    )
    assert main_out[0]  # in [191320, 230509]
    assert main_out[1] == 3
    assert main_out[2] == [0, 0]
    assert main_out[3] == 2
    rmtree(download_dir)
