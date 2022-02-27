import json
import logging
import os

from src.crawler.metacritic_crawler import MetacriticCrawler

logging.basicConfig(level=logging.DEBUG)

_logger = logging.getLogger(__name__)
_years = [2021]

_chrome_driver_path = os.path.abspath('../chromedriver.exe')


def main():
    _logger.info('Starting the crawler ...')
    metacritic_crawler = MetacriticCrawler(_chrome_driver_path, _years)
    items = metacritic_crawler.crawl()

    with open('../out/output.json', 'w') as file:
        json.dump(items, file)


if __name__ == '__main__':
    main()
