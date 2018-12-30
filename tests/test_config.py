import unittest
import os
from hamcrest import assert_that, equal_to, is_, has_items, is_not
from config import SitesAvailabilityConfig
from datetime import datetime

TEST_CONFIGURATION_JSON = """
{
  "configs": [
    {
      "websites": [
        "www.wp.pl",
        "www.facebook.com"
      ],
      "available": [
        "5:00-6:00",
        "22:00-23:00"
      ]
    }
  ]
}
"""
TEST_CONFIG_NAME = "test_config.json"


class TestConfig(unittest.TestCase):
    def setUp(self):
        with open(TEST_CONFIG_NAME, "w") as config:
            config.write(TEST_CONFIGURATION_JSON)
        self.config = SitesAvailabilityConfig(TEST_CONFIG_NAME)

    def tearDown(self):
        os.remove(TEST_CONFIG_NAME)

    def test_get_all_sites(self):
        assert_that(self.config.get_all_sites(), has_items("www.wp.pl", "www.facebook.com"))

    def test_is_site_blocked_in_time(self):
        assert_that(self.config.is_site_blocked_in_time("www.wp.pl", to_time("4:59")), is_(True))
        assert_that(self.config.is_site_blocked_in_time("www.wp.pl", to_time("5:00")), is_(False))
        assert_that(self.config.is_site_blocked_in_time("www.wp.pl", to_time("5:30")), is_(False))
        assert_that(self.config.is_site_blocked_in_time("www.wp.pl", to_time("5:30")), is_(False))
        assert_that(self.config.is_site_blocked_in_time("www.wp.pl", to_time("6:00")), is_(False))
        assert_that(self.config.is_site_blocked_in_time("www.wp.pl", to_time("6:01")), is_(True))
        assert_that(self.config.is_site_blocked_in_time("www.wp.pl", to_time("21:59")), is_(True))
        assert_that(self.config.is_site_blocked_in_time("www.wp.pl", to_time("22:00")), is_(False))
        assert_that(self.config.is_site_blocked_in_time("www.wp.pl", to_time("23:00")), is_(False))
        assert_that(self.config.is_site_blocked_in_time("www.wp.pl", to_time("23:01")), is_(True))

        assert_that(self.config.is_site_blocked_in_time("www.facebook.com", to_time("23:01")), is_(True))
        assert_that(self.config.is_site_blocked_in_time("www.facebook.com", to_time("23:00")), is_(False))

    def test_should_have_site(self):
        assert_that(self.config.has_site("www.wp.pl"), is_(True))
        assert_that(self.config.has_site("www.onet.pl"), is_(False))


def to_time(time_str):
    start_time = datetime.strptime(time_str, "%H:%M")
    return datetime.combine(datetime.today(), start_time.time())
