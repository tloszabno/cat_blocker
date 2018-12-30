import json
from datetime import datetime

DEFAULT_CONFIG_PATH = "config.json"

AVAILABLE_ELEMENT = "available"
WEBSITES_ELEMENT = "websites"
ROOT_ELEMENT_NAME = "configs"


class SitesAvailabilityConfig(object):
    def __init__(self, config_file_path=DEFAULT_CONFIG_PATH):
        self.raw_configs = None
        self.all_sites_with_availability = None
        self.update_config(config_file_path)

    def print(self):
        print(self.all_sites_with_availability)

    def get_all_sites(self):
        return self.all_sites_with_availability.keys()

    def is_site_blocked_in_time(self, url, time):
        availability = self.all_sites_with_availability[url]
        if not availability:
            raise Exception("Site with url %s not found in configuration" % url)
        for time_range in availability:
            start_availability = time_range[0]
            end_availability = time_range[1]
            if (start_availability <= time) and (end_availability >= time):
                return False
        return True

    def has_site(self, url):
        return url in self.all_sites_with_availability.keys()

    def update_config(self, config_file_path=DEFAULT_CONFIG_PATH):
        with open(config_file_path, "r") as config:
            self.raw_configs = json.load(config)
            self.all_sites_with_availability = __get_all_sites_with_availability__(self.raw_configs)


def __get_all_sites_with_availability__(raw_configs):
    all_sites = dict()
    for config in __get_all_config__(raw_configs):
        all_sites.update(__get_sites_from_config__(config))
    return all_sites


def __get_sites_from_config__(raw_config):
    availability = {}
    for site in __get_all_websites__(raw_config):
        availability[site] = __get_availability_parsed__(raw_config)
    return availability


def __get_availability_parsed__(raw_config):
    return [__parse_interval__(interval) for interval in __get_availability__(raw_config)]


def __parse_interval__(interval_str):
    split = interval_str.split("-")
    from_str = split[0]
    to_str = split[1]
    return __to_today_time__(from_str), __to_today_time__(to_str)


def __to_today_time__(time_str):
    start_time = datetime.strptime(time_str, "%H:%M")
    return datetime.combine(datetime.today(), start_time.time())


def __get_availability__(raw_config):
    return raw_config[AVAILABLE_ELEMENT]


def __get_all_websites__(raw_config):
    return raw_config[WEBSITES_ELEMENT]


def __get_all_config__(raw_configs):
    return raw_configs[ROOT_ELEMENT_NAME]
