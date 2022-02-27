import json
import logging
import os

from src.crawler.metacritic_crawler import MetacriticCrawler, CrawlerConfig

logging.basicConfig(level=logging.DEBUG)

_logger = logging.getLogger(__name__)

_chrome_driver_path = os.path.abspath('../chromedriver.exe')


def main():
    _logger.info('Starting the crawler ...')

    config = CrawlerConfig([2020, 2021, 2022], 2, 2, 2)

    metacritic_crawler = MetacriticCrawler(_chrome_driver_path, config)
    items = metacritic_crawler.crawl()

    os.makedirs('../out', exist_ok=True)
    with open('../out/output.json', 'w') as file:
        json.dump(items, file)


if __name__ == '__main__':
    main()
