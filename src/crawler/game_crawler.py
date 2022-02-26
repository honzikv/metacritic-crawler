import logging

from src.crawler.crawler import Crawler
from src.crawler.review_list_crawler import ReviewListCrawler

_name = "//div[contains(@class, 'product_title')]//a//h1/text()"
_summary_details_publisher = "//div[contains(@class, 'product_data')]//ul[@class='summary_details']"
_metacritic_rating = "//div[contains(@class, 'score_summary') and contains(@class, 'metascore_summary')]" \
                     "//span[@itemprop='ratingValue']/text()"
_user_rating = "//a[@class='metascore_anchor']//div[contains(@class, 'metascore_w') and contains(@class,'user')]/text()"

_logger = logging.getLogger(__name__)


class GameCrawler(Crawler):
    """
    Used for crawling game info
    """

    def __init__(self, webdriver, timer, url):
        super().__init__(webdriver, timer)
        self._url = url
        self.result = {}

    def crawl(self):
        fetch_success = super()._get_with_retries(self._url)
        if not fetch_success:
            _logger.error(f'Error, unable to GET {self._url}, skipping ...')
            return None

        name = super()._get_element_as_string_by_xpath(_name)
        metacritic_rating = super()._get_element_as_string_by_xpath(_metacritic_rating)
        user_rating = super()._get_element_as_string_by_xpath(_user_rating)

        if name is None:
            _logger.error(f'Unable to get name of game on page: {self._url}, skipping ...')
            return None

        # Map the values to the dictionary
        self.result['name'] = name
        self.result['metacriticRating'] = metacritic_rating
        self.result['userRating'] = user_rating

        # Get all reviews
        critic_review_crawler = ReviewListCrawler()
        critic_reviews = critic_review_crawler.crawl()  # will return list of objects

        if critic_reviews is None:
            _logger.debug(f'No critic reviews found for {self._url}')
        self.result['critic_reviews'] = critic_reviews

        user_review_crawler = ReviewListCrawler()
        user_reviews = user_review_crawler.crawl()  # will return list of objects

        if user_reviews is None:
            _logger.debug(f'No user reviews found for {self._url}')
        self.result['userReviews'] = user_reviews

        return self.result
