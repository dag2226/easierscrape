from anytree import Node, RenderTree
from anytree.search import find
from bs4 import BeautifulSoup
from os import makedirs
from os.path import basename, exists, join
from pandas import read_html
from re import compile
from requests import get
from urllib.request import urlcleanup, urlretrieve, url2pathname
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
        for file in files:
            try:
                fileUrl = concat_urls(url, file.attrs["href"])
                urlretrieve(fileUrl, join(get_download_dir(filetype, url), basename(fileUrl)))
                urlcleanup()
                file_download_count += 1
            except Exception:
                pass
        file_download_list.append(file_download_count)
    return file_download_list


def parse_images(url):
    images = soup_url(url).findAll("img")
    image_download_count = 0
    for image in images:
        try:
            imageUrl = concat_urls(url, image.attrs["src"])
            urlretrieve(imageUrl, join(get_download_dir("images", url), basename(imageUrl)))
            urlcleanup()
            image_download_count += 1
        except Exception:
            pass
    return image_download_count


def parse_lists(url):
    # This covers unordered and ordered, but not description lists (dl)
    # It's kinda buggy, needs work. Might need some formatting for list items
    # The unit test could also be better
    lists = soup_url(url).findAll(["ul", "ol"])
    if len(lists) != 0:
        for list in lists:
            if list.has_attr("id"):
                list_name = list["id"]
            else:
                list_name = str(uuid4())
            with open(join(get_download_dir("lists", url), list_name + ".txt"), "w") as f:
                items = list.findAll("li")
                for item in items:
                    f.write("- " + item.text + "\n")
            f.close()

    return len(lists)


def parse_tables(url):
    soup_tables = soup_url(url).findAll("table")
    if len(soup_tables) != 0:
        tables = read_html(url)
        # soup_tables is only used to get the ids of tables (for naming purposes)
        # and find the number of tables. pandas read_html does all the work
        for i in range(0, len(tables)):
            if soup_tables[i].has_attr("id"):
                table_name = soup_tables[i]["id"]
            else:
                table_name = str(uuid4())
            tables[i].to_csv(join(get_download_dir("tables", url), table_name + ".csv"))
    return len(soup_tables)


def parse_text(url):
    return [text for text in soup_url(url).stripped_strings]


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


def get_download_dir(type, url):
    dir = join(".", "easierscrape_downloads", type, url2pathname(url)[3:])
    if not exists(dir):
        makedirs(dir)
    return dir


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
