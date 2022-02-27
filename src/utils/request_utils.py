import logging
import time
from datetime import datetime

_logger = logging.getLogger(__name__)

class RequestsTimer:
    """
    Util class for waiting between requests
    """

    def __init__(self, politeness_interval_ms=1250):
        self._politeness_interval_ms = politeness_interval_ms
        self._last_request_time = None

    def wait_until_timer_expired(self):
        if self._last_request_time is None:
            self._last_request_time = datetime.now()
            return

        diff_ms = (datetime.now() - self._last_request_time).total_seconds() * 1000
        if diff_ms < self._politeness_interval_ms:
            # sleep for the remaining duration (approx)
            sleep_time = self._politeness_interval_ms - diff_ms
            _logger.debug(f'Sleeping for: {diff_ms} ms...')
            time.sleep(sleep_time / 1000)

        self._last_request_time = datetime.now()


# Default instance
_instance = RequestsTimer()


def get_default_instance(): return _instance
