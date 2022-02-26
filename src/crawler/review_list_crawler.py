import logging

from src.crawler.crawler import Crawler

_logger = logging.getLogger(__name__)

_last_page = "//ul[@class='pages']//li[contains(@class, 'page') and contains(@class, 'last_page')]//a/text()"

class ReviewListCrawler(Crawler):

    def __init__(self, webdriver, timer, url, xpaths):
        super().__init__(webdriver, timer)
        self._url = url
        self.xpaths = xpaths

    def crawl(self):
        fetch_success = super()._get_with_retries(self._url)
        if not fetch_success:
            _logger.error(f'Error could not GET page with url: {self._url}, skipping...')
            return []

        # Get max page number
        max_page =
