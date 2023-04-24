from argparse import ArgumentParser
from easierscrape import Scraper


def main(arg_strings=None):
    parser = ArgumentParser()
    parser.add_argument('url', help='the url to scrape')
    parser.add_argument('depth', type=int, help='the depth of the scrape tree')
    args = parser.parse_args(arg_strings)

    scraper = Scraper()
    scraper.print_tree(scraper.tree_gen(args.url, args.depth))
    screenshot_size = scraper.get_screenshot(args.url)
    image_count = scraper.parse_images(args.url)
    file_counts = scraper.parse_files(args.url, ['txt', 'pdf'])
    table_count = scraper.parse_tables(args.url)

    return screenshot_size, image_count, file_counts, table_count


if __name__ == "__main__":
    main()
