import abc
import logging
from abc import abstractmethod

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

_logger = logging.getLogger(__name__)


class Crawler(abc.ABC):
    """
    Base crawler class
    """

    def __init__(self, webdriver: WebDriver, timer):
        self._webdriver = webdriver
        self._timer = timer

    @abstractmethod
    def crawl(self):
        pass

    def _get_with_retries(self, url: str, retries=3):
        while retries > 0:
            try:
                self._timer.wait_until_timer_expired()
                self._webdriver.get(url)
                return True
            except TimeoutException:
                _logger.warning(f'URL: {url} timed out, will retry... ({retries - 1})')
                retries -= 1

        return False

    def _get_elements_by_xpath(self, xpath):
        try:
            return self._webdriver.find_elements(By.XPATH, xpath)
        except NoSuchElementException:
            return []

    def _get_element_by_xpath(self, xpath):
        try:
            return self._webdriver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return None

    def _get_string_by_xpath(self, xpath):
        el = self._get_element_by_xpath(xpath)
        return el.text if el is not None else None

    def _get_string_from_element_by_xpath(self, element: WebElement, xpath: str):
        try:
            return element.find_element_by_xpath(xpath).text
        except NoSuchElementException:
            return None

    def _get_last_page_no(self, default_page_no, xpath):
        # We have not processed the first page yet
        max_page = self._get_element_by_xpath(xpath)
        if max_page is None:
            return default_page_no

        if max_page.text.isdigit():
            return int(max_page.text)

        return default_page_no
