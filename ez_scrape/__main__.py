from ez_scrape import parse_files, parse_images, parse_tables, print_tree, tree_gen
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('url', help='the url to scrape')
    parser.add_argument('depth', type=int, help='the depth of the scrape tree')
    args = parser.parse_args()

    print_tree(tree_gen(args.url, args.depth))
    parse_images(args.url)
    parse_files(args.url, ['txt', 'pdf'])
    parse_tables(args.url)
