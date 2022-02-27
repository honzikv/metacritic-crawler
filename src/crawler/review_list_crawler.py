import logging
import math

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.crawler.crawler import Crawler
from src.utils.metacritic_uri_builder import add_page_no_query

_logger = logging.getLogger(__name__)

_max_page_xpath = "//ul[@class='pages']//li[contains(@class, 'page') and contains(@class, 'last_page')]//a"


class ReviewListCrawler(Crawler):

    def __init__(self, webdriver, timer, url, xpaths, max_reviews, has_expand_button=False):
        super().__init__(webdriver, timer)
        self._url = url
        self.xpaths = xpaths
        self.max_reviews = max_reviews
        self.click_expand_button = has_expand_button

    def _find_and_click_expand_button(self, element: WebElement, xpath: str):
        try:
            element.find_element(By.XPATH, xpath).click()
        except (NoSuchElementException, WebDriverException):
            return

    def crawl(self):
        fetch_success = super()._get_with_retries(self._url)
        if not fetch_success:
            _logger.error(f'Error could not GET page with url: {self._url}, skipping...')
            return []

        max_page = math.inf
        current_page = 0

        items = []
        while not current_page > max_page and len(items) < self.max_reviews:
            if max_page is math.inf:
                max_page = super()._get_last_page_no(current_page, _max_page_xpath)
            else:
                current_url = add_page_no_query(self._url, current_page)
                fetch_success = super()._get_with_retries(current_url)
                if not fetch_success:
                    _logger.warning(f'Error while fetching {current_url}, skipping...')
                    return items

            reviews = super()._get_elements_by_xpath(self.xpaths['review_list'])

            for review_el in reviews:
                review = {
                    'reviewerName': super()._get_string_from_element_by_xpath(review_el, self.xpaths['reviewer_name']),
                    'dateReviewed': super()._get_string_from_element_by_xpath(review_el, self.xpaths['date_reviewed']),
                    'score': super()._get_string_from_element_by_xpath(review_el, self.xpaths['score'])
                }

                if self.click_expand_button:
                    try:
                        self._find_and_click_expand_button(review_el, self.xpaths['expand_button'])
                    except Exception as e:
                        _logger.error(f'An error has occurred: {str(e)}')

                # the review text itself may be in two different tags in some cases so get one which is not None if any
                review_text = super()._get_string_from_element_by_xpath(review_el, self.xpaths['review_text'])
                review_text_alt = super()._get_string_from_element_by_xpath(
                    review_el, self.xpaths['review_text_alt']) if 'review_text_alt' in self.xpaths else None

                if review_text is not None and len(review_text) > 0:
                    review['text'] = review_text
                elif review_text_alt is not None and len(review_text_alt) > 0:
                    review['text'] = review_text_alt
                else:
                    continue

                items.append(review)
                if len(items) >= self.max_reviews:
                    break

            current_page += 1

        return items
