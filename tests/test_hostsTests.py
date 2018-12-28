import unittest
import os
from hamcrest import assert_that, equal_to, is_, has_item, is_not
from hosts import HostsFileFacade

TEST_HOSTS = "test_hosts.txt"


class TestHostsFacade(unittest.TestCase):
    def setUp(self):
        with open(TEST_HOSTS, "w") as test_hosts:
            test_hosts.write("127.0.0.1    localhost")
        hosts_file_path_resolver = lambda: TEST_HOSTS
        self.facade = HostsFileFacade(hosts_file_path_resolver)

    def tearDown(self):
        os.remove(TEST_HOSTS)

    def test_should_add_url_to_hosts_with_localhost_mapping(self):
        #when
        self.facade.block_url(["wp.pl"])

        #then
        assert_that(content_of_hosts(), has_item("localhost    wp.pl\n"))

    def test_should_add_url_to_hosts_with_localhost_mapping_only_once(self):
        #when
        self.facade.block_url(["wp.pl"])
        self.facade.block_url(["wp.pl"])

        #then
        assert_that(content_of_hosts().count("localhost    wp.pl\n"), equal_to(1))

    def test_should_delete_url_from_hosts(self):
        #given
        self.facade.block_url(["wp.pl", "onet.pl"])

        #when
        self.facade.unblock_url(["wp.pl"])

        #then
        assert_that(content_of_hosts(), is_not(has_item("localhost    wp.pl\n")))
        assert_that(content_of_hosts(), has_item("localhost    onet.pl\n"))

    def test_should_contain_blocked_url(self):
        #given
        self.facade.block_url(["wp.pl", "onet.pl"])

        #when
        blocked_wp = self.facade.is_blocked("wp.pl")
        blocked_facebook = self.facade.is_blocked("facebook.pl")

        #then
        assert_that(blocked_wp, is_(True))
        assert_that(blocked_facebook, is_(False))

def content_of_hosts():
    with open(TEST_HOSTS, "r") as f:
        return f.readlines()