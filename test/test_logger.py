import logging
from unittest import TestCase

logging.basicConfig(level=logging.INFO)

log = logging.getLogger("hello")


class TestUtensil(TestCase):
    def test_logger(self):
        print("456")
        log.info("123")
