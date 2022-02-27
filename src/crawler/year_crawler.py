import logging
import math

from src.crawler.crawler import Crawler
from src.crawler.game_crawler import GameCrawler
from src.utils.metacritic_uri_builder import create_absolute_game_url, add_page_no_query

_max_page_xpath = "//li[contains(@class, 'page last_page')]//a[contains(@class, 'page_num')]"
# //div[contains(@class, 'browse_list_wrapper')]//td[contains(@class, 'clamp-summary-wrap')]//a[contains(@class, 'title')]/@href
_items_xpath = "//div[contains(@class, 'browse_list_wrapper')]//td[contains(@class, 'clamp-summary-wrap')]//a[contains(@class, 'title')]"

_logger = logging.getLogger(__name__)


class YearCrawler(Crawler):
    """
    Used for crawling individual year of releases
    """

    def __init__(self, webdriver, timer):
        super().__init__(webdriver, timer)
        self._base_url = webdriver.current_url

    def crawl(self):
        """
        Crawls the entire year
        :return:
        """

        max_page = math.inf
        current_page = 0

        items = []
        while not current_page > max_page:
            _logger.debug(f'Attempting to crawl items from url: {self._webdriver.current_url}')
            if max_page is math.inf:
                max_page = super()._get_last_page_no(current_page, _max_page_xpath)
            else:
                current_url = add_page_no_query(self._base_url, current_page)
                fetch_success = super()._get_with_retries(current_url)
                if not fetch_success:
                    _logger.warning(f'Error while fetching {current_url}, skipping...')
                    return items

            # Get all item urls in the page
            item_url_els = self._get_elements_by_xpath(_items_xpath)
            if len(item_url_els) == 0:
                return

            item_urls = []
            for item_url_el in item_url_els:
                link = item_url_el.get_attribute('href')
                if link is None:
                    continue

                item_urls.append(link)

            _logger.debug(f'Found {len(item_urls)} item urls, attempting to scrape ...')

            for item_url in item_urls:
                game_crawler = GameCrawler(self._webdriver, self._timer, item_url)
                item = game_crawler.crawl()

                if item is not None:
                    items.append(item)

            current_page += 1

        return items
