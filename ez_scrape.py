from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from anytree.search import find
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from os import makedirs
from os.path import basename, exists
from re import compile
from requests import get
from urllib.request import urlretrieve










def parse_anchors(url):
	return soup_url(url).find_all('a')

def parse_images(url):
	create_dir('./ez_scrape_downloads/images')
	for img in soup_url(url).findAll('img'):
		try:
			imgUrl = concat_urls(url, img.attrs['src'])
			urlretrieve(imgUrl, './ez_scrape_downloads/images/' + basename(imgUrl))
		except:
			pass

def parse_lists(url):
	# TODO
	pass

def parse_files(url, filetypes = []):
	if len(filetypes) == 0:
		print("No filetype specified")
	for filetype in filetypes:
		create_dir('./ez_scrape_downloads/' + filetype)
		for file in soup_url(url).find_all('a', href = compile(r'(.' + filetype + ')')):
			try:
				fileUrl = concat_urls(url, file.attrs['href'])
				urlretrieve(fileUrl, './ez_scrape_downloads/' + filetype + '/' + basename(fileUrl))
			except:
				pass

def parse_tables(url):
	# TODO
	pass

def parse_text(url):
	# TODO
	pass










def soup_url(url):
	return BeautifulSoup(get(url).text, "html.parser")

def concat_urls(base_url, child_url):
	if child_url.startswith("/"):
		child_url = base_url + child_url
	if child_url.startswith("./"):
		child_url = base_url + child_url[1:]
	if not child_url.startswith('http'):
		child_url = base_url + '/' + child_url
	if child_url.endswith('/'):
		child_url = child_url[:-1]
	return child_url

def create_dir(dir):
	if not exists(dir):
		makedirs(dir)

def tree_gen(url, maxdepth, tree = None, depth = 0):
	if tree is None:
		url = url.replace('www.', '')
		if url.endswith('/'):
			url = url[:-1]
		tree = Node(url, url = url)

	if depth < maxdepth:
		for a in parse_anchors(url):
			child_url = concat_urls(url, a.attrs['href'].replace('www.', ''))
			try:
				if find(tree.root, lambda node: node.url == child_url) is None:
					new_leaf = Node(child_url, url = child_url, parent = tree)
					tree = tree_gen(child_url, maxdepth, new_leaf, depth + 1)
			except:
				pass

	return tree.root

def print_tree(tree):
	for pre, fill, node in RenderTree(tree):
		print("%s%s" % (pre, node.name))










parser = ArgumentParser()
parser.add_argument('url', help = 'the url to scrape')
parser.add_argument('depth', type = int, help = 'the depth of the scrape tree')
args = parser.parse_args()

print_tree(tree_gen(args.url, args.depth))
parse_images(args.url)
parse_files(args.url, ['txt', 'pdf'])










'''
Testing links:
https://www.cs.columbia.edu/~paine/4995/
https://www.cs.columbia.edu/~jae/


Requirements:
pip install -q anytree beautifulsoup4 requests urllib
'''