from argparse import ArgumentParser
from easierscrape import Scraper


def main(arg_strings=None):
    parser = ArgumentParser()
    parser.add_argument("url", help="the url to scrape")
    parser.add_argument("depth", type=int, help="the depth of the scrape tree")
    parser.add_argument("download_path", help="the location to download files to")
    args = parser.parse_args(arg_strings)

    scraper = Scraper(args.url, args.download_path)
    scraper.print_tree(int(args.depth))
    screenshot_success = scraper.get_screenshot()
    image_count = scraper.parse_images()
    file_counts = scraper.parse_files(["txt", "pdf"])
    table_count = scraper.parse_tables()

    return screenshot_success, image_count, file_counts, table_count


if __name__ == "__main__":
    main()
