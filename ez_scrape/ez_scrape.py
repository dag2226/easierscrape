from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from anytree.search import find
from bs4 import BeautifulSoup
from os import makedirs
from os.path import basename, exists
from pandas import DataFrame
from re import compile
from requests import get
from urllib.request import urlretrieve, url2pathname
from uuid import uuid4

def parse_anchors(url):
	return soup_url(url).find_all('a')

def parse_images(url):
	images = soup_url(url).findAll('img')
	if len(images) == 0:
		print('No images found at ' + url)
	else:
		create_dir('./ez_scrape_downloads/images' + url2pathname(url)[2:])
		for image in images:
			try:
				imageUrl = concat_urls(url, image.attrs['src'])
				urlretrieve(imageUrl, './ez_scrape_downloads/images/' + url2pathname(url)[2:] +'/' + basename(imageUrl))
			except:
				pass

def parse_lists(url):
	# TODO		The key is "ul"
	pass

def parse_files(url, filetypes = []):
	if len(filetypes) == 0:
		print("No filetype specified")
	for filetype in filetypes:
		files = soup_url(url).find_all('a', href = compile(r'(.' + filetype + ')'))
		if len(files) == 0:
			print('No ' + filetype + ' files found at ' + url)
		else:
			create_dir('./ez_scrape_downloads/' + filetype + url2pathname(url)[2:])
			for file in files:
				try:
					fileUrl = concat_urls(url, file.attrs['href'])
					urlretrieve(fileUrl, './ez_scrape_downloads/' + filetype + url2pathname(url)[2:] + '/' + basename(fileUrl))
				except:
					pass

def parse_tables(url):
	tables = soup_url(url).findAll('table')
	if len(tables) == 0:
		print('No tables found at ' + url)
	else:
		create_dir('./ez_scrape_downloads/tables' + url2pathname(url)[2:])
		for table in soup_url(url).findAll('table'):
			content = []

			for tr in table.find_all('tr')[1:]:
				row = []
				for td in tr.find_all('td'):
					row.append(td.text)
				content.append(row)

			df = DataFrame(content)
			df.columns = [th.text for th in table.find_all('th')]

			if table.has_attr('id'):
				table_name = table['id']
			else:
				table_name = str(uuid4())

			df.to_csv('./ez_scrape_downloads/tables/' + url2pathname(url)[2:] + '/' + table_name + '.csv')  

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