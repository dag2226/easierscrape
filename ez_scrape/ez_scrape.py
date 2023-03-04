from anytree import Node, RenderTree
from anytree.search import find
from bs4 import BeautifulSoup
from os import makedirs
from os.path import basename, exists
from pandas import read_html
from re import compile
from requests import get
from urllib.request import urlretrieve, url2pathname
from uuid import uuid4


def parse_anchors(url):
    return soup_url(url).find_all("a")


def parse_files(url, filetypes=[]):
    if len(filetypes) == 0:
        print("No filetype specified")
        return
    file_download_list = []
    for filetype in filetypes:
        files = soup_url(url).find_all("a", href=compile(r"(." + filetype + ")"))
        file_download_count = 0
        if len(files) != 0:
            create_dir("./ez_scrape_downloads/" + filetype + url2pathname(url)[2:])
        for file in files:
            try:
                fileUrl = concat_urls(url, file.attrs["href"])
                urlretrieve(
                    fileUrl, "./ez_scrape_downloads/" + filetype + url2pathname(url)[2:] + "/" + basename(fileUrl)
                )
                file_download_count += 1
            except Exception:
                pass
        file_download_list.append(file_download_count)
    return file_download_list


def parse_images(url):
    images = soup_url(url).findAll("img")
    image_download_count = 0
    if len(images) != 0:
        create_dir("./ez_scrape_downloads/images" + url2pathname(url)[2:])
    for image in images:
        try:
            imageUrl = concat_urls(url, image.attrs["src"])
            urlretrieve(imageUrl, "./ez_scrape_downloads/images/" + url2pathname(url)[2:] + "/" + basename(imageUrl))
            image_download_count += 1
        except Exception:
            pass
    return image_download_count


def parse_lists(url):
    # TODO        The key is "ul"
    return


def parse_tables(url):
    soup_tables = soup_url(url).findAll("table")
    if len(soup_tables) != 0:
        create_dir("./ez_scrape_downloads/tables" + url2pathname(url)[2:])
        tables = read_html(url)
        for i in range(0, len(tables)):
            if soup_tables[i].has_attr("id"):
                table_name = soup_tables["id"]
            else:
                table_name = str(uuid4())
            tables[i].to_csv("./ez_scrape_downloads/tables/" + url2pathname(url)[2:] + "/" + table_name + ".csv")
    return len(soup_tables)


def parse_text(url):
    # TODO
    return


def soup_url(url):
    return BeautifulSoup(get(url).text, "html.parser")


def concat_urls(base_url, child_url):
    if child_url.startswith("/"):
        child_url = base_url + child_url
    if child_url.startswith("./"):
        child_url = base_url + child_url[1:]
    if not child_url.startswith("http"):
        child_url = base_url + "/" + child_url
    if child_url.endswith("/"):
        child_url = child_url[:-1]
    return child_url


def create_dir(dir):
    if not exists(dir):
        makedirs(dir)


def tree_gen(url, maxdepth, tree=None, depth=0):
    if tree is None:
        url = url.replace("www.", "")
        if url.endswith("/"):
            url = url[:-1]
        tree = Node(url, url=url)
    if depth < maxdepth:
        for a in parse_anchors(url):
            child_url = concat_urls(url, a.attrs["href"].replace("www.", ""))
            try:
                if find(tree.root, lambda node: node.url == child_url) is None:
                    new_leaf = Node(child_url, url=child_url, parent=tree)
                    tree = tree_gen(child_url, maxdepth, new_leaf, depth + 1)
            except Exception:
                pass
    return tree.root


def print_tree(tree):
    tree_print = ""
    for pre, fill, node in RenderTree(tree):
        tree_print += "%s%s\n" % (pre, node.name)
    print(tree_print[:-1])
