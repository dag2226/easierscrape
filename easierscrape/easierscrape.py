from anytree import Node, RenderTree
from anytree.search import find
from bs4 import BeautifulSoup
from os import getcwd, makedirs
from os.path import basename, exists, join
from pandas import read_html
from re import compile
from requests import get
from urllib.request import urlcleanup, urlretrieve, url2pathname
from uuid import uuid4


def _soup_url(url):
    return BeautifulSoup(get(url).text, "html.parser")


def _concat_urls(base_url, child_url):
    if child_url.startswith("/"):
        child_url = base_url + child_url
    if child_url.startswith("./"):
        child_url = base_url + child_url[1:]
    if not child_url.startswith("http"):
        child_url = base_url + "/" + child_url
    if child_url.endswith("/"):
        child_url = child_url[:-1]
    return child_url


def _get_download_dir(type, url):
    dir = join(getcwd(), "easierscrape_downloads", type, url2pathname(url)[3:])
    if not exists(dir):
        makedirs(dir)
    return dir


def _tree_gen_rec(url, maxdepth, tree, depth):
    if tree is None:
        url = url.replace("www.", "")
        if url.endswith("/"):
            url = url[:-1]
        tree = Node(url, url=url)
    if depth < maxdepth:
        for a in parse_anchors(url):
            child_url = _concat_urls(url, a.attrs["href"].replace("www.", ""))
            try:
                if find(tree.root, lambda node: node.url == child_url) is None:
                    new_leaf = Node(child_url, url=child_url, parent=tree)
                    tree = tree_gen(child_url, maxdepth, new_leaf, depth + 1)
            except Exception:
                pass
    return tree.root


def parse_anchors(url):
    """Parses a list of anchor tags from provided url.

    Args:
        url (str): The url to scrape from

    Returns:
        List[str]: List of anchor tags in the url

    """
    return _soup_url(url).find_all("a")


def parse_files(url, filetypes=[]):
    """Downloads provided filetypes from provided url to an "easierscrape_downloads"
    folder in the current working directory

    Args:
        url (str): The url to scrape from
        filetypes (List[str]): List of filetypes ("pdf", "txt", etc.) to scrape

    Returns:
        List[int]: List of number of files downloaded per filetype from url (so if
        filetypes=["pdf", "txt"] and the return value is [1, 30] this means that 1
        pdf file and 30 txt files were downloaded)

    """
    if len(filetypes) == 0:
        print("No filetype specified")
        return
    file_download_list = []
    for filetype in filetypes:
        file_download_count = 0
        for file in _soup_url(url).find_all("a", href=compile(r"(." + filetype + ")")):
            try:
                fileUrl = _concat_urls(url, file.attrs["href"])
                urlretrieve(fileUrl, join(_get_download_dir(filetype, url), basename(fileUrl)))
                urlcleanup()
                file_download_count += 1
            except Exception:
                pass
        file_download_list.append(file_download_count)
    return file_download_list


def parse_images(url):
    """Downloads all images from provided url to an "easierscrape_downloads"
    folder in the current working directory

    Args:
        url (str): The url to scrape from

    Returns:
        int: Number of images downloaded from url

    """
    image_download_count = 0
    for image in _soup_url(url).findAll("img"):
        try:
            imageUrl = _concat_urls(url, image.attrs["src"])
            urlretrieve(imageUrl, join(_get_download_dir("images", url), basename(imageUrl)))
            urlcleanup()
            image_download_count += 1
        except Exception:
            pass
    return image_download_count


def parse_lists(url):
    """Parses a list of lists from provided url.

    Args:
        url (str): The url to scrape from

    Returns:
        List[List[str]]: List of lists (each stored as a List) in the url

    """
    # This covers unordered and ordered, but not description lists (dl)
    # TODO: The unit test for this could be improved
    out = []
    for list in _soup_url(url).findAll(["ul", "ol"]):
        out.append([item for item in list.stripped_strings])
        if out[-1] == []:
            out.pop()
    return out


def parse_tables(url):
    """Downloads all tables from provided url to an "easierscrape_downloads"
    folder in the current working directory

    Args:
        url (str): The url to scrape from

    Returns:
        int: Number of tables downloaded from url

    """
    soup_tables = _soup_url(url).findAll("table")
    if len(soup_tables) != 0:
        tables = read_html(url)
        # soup_tables is only used to get the ids of tables (for naming purposes)
        # and find the number of tables. pandas read_html does all the work
        for i in range(0, len(tables)):
            if soup_tables[i].has_attr("id"):
                table_name = soup_tables[i]["id"]
            else:
                table_name = str(uuid4())
            tables[i].to_csv(join(_get_download_dir("tables", url), table_name + ".csv"))
    return len(soup_tables)


def parse_text(url):
    """Parses a list of text fragments from provided url.

    Args:
        url (str): The url to scrape from

    Returns:
        List[str]: List of text fragments in the url

    """
    return [text for text in _soup_url(url).stripped_strings]


def tree_gen(url, maxdepth):
    """Generates a tree of depth=maxdepth starting at url

    Args:
        url (str): The head url to generate the tree from
        maxdepth (int): The depth you want to generate the tree to

    Returns:
        Node: Head node of an anytree hyperlink tree

    """
    return _tree_gen_rec(url, maxdepth, None, 0)


def print_tree(tree):
    """Prints out the tree of the provided anytree Node structure

    Args:
        tree (Node): The head anytree Node of the tree to print

    """
    tree_print = ""
    for pre, fill, node in RenderTree(tree):
        tree_print += "%s%s\n" % (pre, node.name)
    print(tree_print[:-1])
