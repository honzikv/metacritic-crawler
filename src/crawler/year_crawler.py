import logging
import math

from src.crawler.crawler import Crawler
from src.crawler.game_crawler import GameCrawler
from src.utils.metacritic_uri_builder import create_absolute_game_url

_max_page_xpath = "//li[contains(@class, 'page last_page')]//a[contains(@class, 'page_num')]/text()"
_items_xpath = "//div[contains(@class, 'browse_list_wrapper')]//td[contains(@class, 'clamp-summary-wrap')]" \
               "//a[contains(@class, 'title')]/@href"

_logger = logging.getLogger(__name__)


class YearCrawler(Crawler):
    """
    Used for crawling individual year of releases
    """

    def __init__(self, webdriver, timer):
        super().__init__(webdriver, timer)

    def crawl(self):
        """
        Crawls the entire year
        :return:
        """

        max_page = math.inf
        current_page = 0

        items = []
        while not current_page > max_page:
            if max_page is math.inf:
                max_page = self._get_last_page_no(current_page)

            # Get all item urls in the page
            item_urls = super()._get_elements_by_xpath(_items_xpath)
            _logger.debug(f'Found {len(item_urls)} item urls, attempting to scrape ...')

            for relative_item_url in item_urls:
                game_url = create_absolute_game_url(relative_item_url)
                game_crawler = GameCrawler(self._webdriver, self._timer, game_url)
                item = game_crawler.crawl()

                if item is not None:
                    items.append(item)

        return items