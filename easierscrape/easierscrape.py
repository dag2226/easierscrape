from anytree import Node, RenderTree
from anytree.search import find
from bs4 import BeautifulSoup
from os import getcwd, makedirs
from os.path import basename, exists, join
from pandas import read_html, ExcelWriter
from re import compile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from urllib.request import urlopen, url2pathname
from uuid import uuid4


class Scraper:
    """Class for a scraper that targets `url`. A `Scraper` object acts as a "one-stop-shop" for
    all scraping functions.
    """

    def __init__(self, url):
        """
        Args:
            url (str): The url to scrape from.

        """
        self.url = url

        # hide GUI
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)

        self.soup_url = BeautifulSoup(self.driver.page_source, "html.parser")

    def __del__(self):
        self.driver.quit()

    def _concat_urls(self, base_url, child_url):
        parsed = urlparse(base_url)
        if child_url.startswith("/"):
            child_url = parsed.scheme + "://" + parsed.netloc + child_url
        if child_url.startswith("./"):
            child_url = base_url + child_url[1:]
        if not child_url.startswith("http"):
            child_url = base_url + "/" + child_url
        if child_url.endswith("/"):
            child_url = child_url[:-1]
        return child_url

    def _get_download_dir(self, type):
        dir = join(getcwd(), "easierscrape_downloads", type, url2pathname(self.url)[3:])
        if not exists(dir):
            makedirs(dir)
        return dir

    def _tree_gen_rec(self, url, maxdepth, tree, depth):
        if tree is None:
            url = url.replace("www.", "")
            if url.endswith("/"):
                url = url[:-1]
            tree = Node(url, url=url)
        if depth < maxdepth:
            parent_node = tree
            self.driver.get(url)
            for a in BeautifulSoup(self.driver.page_source, "html.parser").find_all("a"):
                try:
                    child_url = self._concat_urls(url, a.attrs["href"].replace("www.", ""))
                    if find(tree.root, lambda node: node.url == child_url) is None:
                        new_leaf = Node(child_url, url=child_url, parent=parent_node)
                        tree = self._tree_gen_rec(child_url, maxdepth, new_leaf, depth + 1)
                except Exception:
                    pass
        return tree.root

    def get_screenshot(self):
        """Downloads screenshot from the Scraper url to an "easierscrape_downloads" folder in the
        current working directory.

        Returns:
            bool: True

        """
        download_file = join(self._get_download_dir("images"), "easierscrape_screenshot.png")

        self.driver.find_element(By.TAG_NAME, "body").screenshot(download_file)

        return True

    def parse_anchors(self):
        """Parses a list of anchor tags from the Scraper url.

        Returns:
            List[str]: List of anchor tags in the url.

        """
        return self.soup_url.find_all("a")

    def parse_files(self, filetypes=[]):
        """Downloads provided filetypes from the Scraper url to an "easierscrape_downloads" folder
        in the current working directory.

        Args:
            filetypes (List[str]): List of filetypes ("pdf", "txt", etc.) to scrape.

        Returns:
            List[int]: List of number of files downloaded per filetype from url (so if
            filetypes=["pdf", "txt"] and the return value is [1, 30] this means that 1
            pdf file and 30 txt files were downloaded).

        """
        if len(filetypes) == 0:
            print("No filetype specified")
            return
        file_download_list = []
        for filetype in filetypes:
            file_download_count = 0
            for file in self.soup_url.find_all("a", href=compile(r"(." + filetype + ")")):
                try:
                    fileUrl = self._concat_urls(self.url, file.attrs["href"])
                    response = urlopen(fileUrl)
                    with open(join(self._get_download_dir(filetype), basename(fileUrl)), "wb") as file:
                        file.write(response.read())
                    file.close()
                    file_download_count += 1
                except Exception:
                    pass
            file_download_list.append(file_download_count)
        return file_download_list

    def parse_images(self):
        """Downloads all images from the Scraper url to an "easierscrape_downloads" folder in the
        current working directory.

        Returns:
            int: Number of images downloaded from url.

        """
        image_download_count = 0
        for image in self.soup_url.findAll("img"):
            try:
                imageUrl = self._concat_urls(self.url, image.attrs["src"])
                response = urlopen(imageUrl)
                with open(join(self._get_download_dir("images"), basename(imageUrl)), "wb") as file:
                    file.write(response.read())
                    file.close()
                image_download_count += 1
            except Exception:
                pass
        return image_download_count

    def parse_lists(self):
        """Parses a list of lists from the Scraper url.

        Returns:
            List[List[str]]: List of lists (each stored as a List) in the url.

        """
        # This covers unordered and ordered, but not description lists (dl)
        out = []
        for list in self.soup_url.findAll(["ul", "ol"]):
            out.append([item for item in list.stripped_strings])
            if out[-1] == []:
                out.pop()
        return out

    def parse_tables(self, output_type="csv"):
        """Downloads all tables from the Scraper url to an "easierscrape_downloads" folder in the
        current working directory.

        Supported output types are csv and xlsx (defaults to csv).

        - If downloaded as a csv file, each table will be stored in a separate csv.
        - If downloaded as an xlsx file, all tables will be stored as separate sheets in a
          "tables.xlsx" file.

        Args:
            output_type (str): The filetype to output to (defaults to csv).

        Returns:
            int: Number of tables downloaded from url.

        """
        soup_tables = self.soup_url.findAll("table")
        if len(soup_tables) != 0:
            tables = read_html(self.url)
            # soup_tables is only used to get the ids of tables (for naming purposes)
            # and find the number of tables. pandas read_html does all the work
            for i in range(0, len(tables)):
                if soup_tables[i].has_attr("id"):
                    table_name = soup_tables[i]["id"]
                else:
                    table_name = uuid4().hex[0:31]
                if output_type == "csv":
                    tables[i].to_csv(join(self._get_download_dir("tables"), table_name + ".csv"))
                elif output_type == "xlsx":
                    excel_file = join(self._get_download_dir("tables"), "tables.xlsx")
                    if exists(excel_file):
                        with ExcelWriter(excel_file, mode="a") as writer:
                            tables[i].to_excel(writer, sheet_name=table_name)
                    else:
                        with ExcelWriter(excel_file, mode="w") as writer:
                            tables[i].to_excel(writer, sheet_name=table_name)
                else:
                    print(
                        "output_type = "
                        + output_type
                        + " not implemented.\nCurrently supported filetypes are csv and xlsx."
                    )
        return len(soup_tables)

    def parse_text(self):
        """Parses a list of text fragments from the Scraper url.

        Returns:
            List[str]: List of text fragments in the url.

        """
        return [text for text in self.soup_url.stripped_strings]

    def tree_gen(self, maxdepth):
        """Generates a tree of depth=maxdepth starting at the Scraper url.

        Args:
            maxdepth (int): The depth you want to generate the tree to.

        Returns:
            Node: Head node of an anytree hyperlink tree.

        """
        return self._tree_gen_rec(self.url, maxdepth, None, 0)

    def print_tree(self, maxdepth):
        """Prints a tree of depth=maxdepth starting at the Scraper url.

        Args:
            maxdepth (int): The depth you want to print the tree to.

        """
        tree_print = ""
        for pre, fill, node in RenderTree(self.tree_gen(maxdepth)):
            tree_print += "%s%s\n" % (pre, node.name)
        print(tree_print[:-1])
