# Base crawling module
import logging

from selenium import webdriver

from src.crawler.crawler_config import CrawlerConfig
from src.utils.metacritic_uri_builder import create_games_url
from src.utils.request_utils import get_default_instance

from src.crawler.crawler import Crawler
from src.crawler.year_crawler import YearCrawler

_logger = logging.getLogger(__name__)


class MetacriticCrawler(Crawler):
    """
    Base crawler class that crawls entire metacritic.com for all games released between years passed in the constructor
    """

    def __init__(self, chrome_driver_path, crawler_config: CrawlerConfig):
        super().__init__(webdriver.Chrome(executable_path=chrome_driver_path), get_default_instance())
        self.crawler_config = crawler_config

    def __del__(self):
        self._webdriver.quit()

    def crawl(self):
        store = {}

        for year in self.crawler_config.years_crawled:
            _logger.info(f'Crawling games released in {year}')
            store[year] = self._crawl_year(year)

        return store

    def _crawl_year(self, year):
        current_url = create_games_url(year)

        # Wait out the politeness timer if necessary
        if not super()._get_with_retries(current_url):
            _logger.warning(f'Failed to crawl: {current_url}. Skipping ...')
            return []

        year_crawler = YearCrawler(self._webdriver, self._timer, self.crawler_config)
        return year_crawler.crawl()
