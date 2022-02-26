# Base crawling module
import logging
from typing import List

from selenium import webdriver

from src.utils.metacritic_uri_builder import create_games_url
from src.utils.request_utils import get_default_instance

from src.crawler.crawler import Crawler
from src.crawler.year_crawler import YearCrawler

_logger = logging.getLogger(__name__)

_webdriver_exe_path = '../../chromedriver.exe'
_chrome_driver = webdriver.Chrome(_webdriver_exe_path)


class MetacriticCrawler(Crawler):
    """
    Base crawler class that crawls entire metacritic.com for all games released between years passed in the constructor
    """

    def __init__(self, crawl_years: List[int]):
        super().__init__(_chrome_driver, get_default_instance())
        self.crawl_years = crawl_years

    def crawl(self):
        store = {}

        for year in self.crawl_years:
            _logger.info(f'Crawling games released in {year}')
            store[year] = self._crawl_year(year)

        return store

    def _crawl_year(self, year):
        current_url = create_games_url(year)

        # Wait out the politeness timer if necessary
        if not super()._get_with_retries(current_url):
            _logger.warning(f'Failed to crawl: {current_url}')
            return []

        year_crawler = YearCrawler(self._webdriver, self._timer)
        return year_crawler.crawl()
