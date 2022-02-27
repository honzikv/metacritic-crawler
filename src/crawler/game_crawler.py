import logging

from src.crawler.crawler import Crawler
from src.crawler.crawler_config import CrawlerConfig
from src.crawler.review_list_crawler import ReviewListCrawler
from src.utils.metacritic_uri_builder import create_critic_reviews_url, create_user_reviews_url

_name = "//div[contains(@class, 'product_title')]//a//h1"
_summary_details_publisher = "//div[contains(@class, 'product_data')]//ul[@class='summary_details']"
_metacritic_rating = "//div[contains(@class, 'score_summary') and contains(@class, 'metascore_summary')]" \
                     "//span[@itemprop='ratingValue']"
_user_rating = "//a[@class='metascore_anchor']//div[contains(@class, 'metascore_w') and contains(@class,'user')]"

_logger = logging.getLogger(__name__)

_critic_reviews_xpaths = {
    'review_list': "//ol[contains(@class, 'reviews') and contains(@class, 'critic_reviews')]//li""//div["
                   "@class='review_content']",
    'reviewer_name': ".//div[@class='review_critic']//div[@class='source']/a",
    'date_reviewed': ".//div[@class='review_critic']//div[@class='date']",
    'score': ".//div[@class='review_grade']/div",
    'review_text': ".//div[@class='review_body']"
}

_user_reviews_xpaths = {
    'review_list': "//ol[contains(@class, 'reviews') and contains(@class, 'user_reviews')]//li//div["
                   "@class='review_content']",
    'review_text': ".//div[@class='review_body']//span[contains(@class, 'blurb') and contains(@class, "
                   "'blurb_expanded')]",
    'review_text_alt': ".//div[@class='review_body']//span",
    'reviewer_name': ".//div[@class='review_critic']//div[@class='name']//a",
    'date_reviewed': ".//div[@class='review_critic']//div[@class='date']",
    'score': ".//div[@class='review_grade']//div"
}


class GameCrawler(Crawler):
    """
    Used for crawling game info
    """

    def __init__(self, webdriver, timer, url, crawler_config: CrawlerConfig):
        super().__init__(webdriver, timer)
        self._url = url
        self.result = {}
        self.crawler_config = crawler_config

    def crawl(self):
        fetch_success = super()._get_with_retries(self._url)
        if not fetch_success:
            _logger.error(f'Error, unable to GET {self._url}, skipping ...')
            return None

        name = super()._get_string_by_xpath(_name)
        metacritic_rating = super()._get_string_by_xpath(_metacritic_rating)
        user_rating = super()._get_string_by_xpath(_user_rating)

        if name is None:
            _logger.error(f'Unable to get name of game on page: {self._url}, skipping ...')
            return None

        # Map the values to the dictionary
        self.result['name'] = name
        self.result['metacriticRating'] = metacritic_rating
        self.result['userRating'] = user_rating

        # Get all reviews
        critic_reviews_url = create_critic_reviews_url(self._url)
        critic_review_crawler = ReviewListCrawler(self._webdriver, self._timer, critic_reviews_url,
                                                  _critic_reviews_xpaths,
                                                  self.crawler_config.max_critic_reviews_per_game)
        critic_reviews = critic_review_crawler.crawl()  # will return list of objects

        if critic_reviews is None:
            _logger.debug(f'No critic reviews found for {self._url}')
        self.result['critic_reviews'] = critic_reviews

        user_reviews_url = create_user_reviews_url(self._url)
        user_review_crawler = ReviewListCrawler(self._webdriver, self._timer, user_reviews_url, _user_reviews_xpaths,
                                                self.crawler_config.max_user_reviews_per_game)
        user_reviews = user_review_crawler.crawl()  # will return list of objects

        if user_reviews is None:
            _logger.debug(f'No user reviews found for {self._url}')
        self.result['userReviews'] = user_reviews

        return self.result
