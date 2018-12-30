#!/usr/bin/env python

import time

import schedule

from blocker import Blocker
from config import SitesAvailabilityConfig
from hosts import HostsFileFacade

SCHEDULER_TICK_INTERVAL_IN_SEC = 30

hosts_file_facade = HostsFileFacade()
config = SitesAvailabilityConfig()
blocker = Blocker(hosts_file_facade, config)


def main():
    configure_scheduler()
    do_infinite_schedule_loop()


def configure_scheduler():
    schedule.every(1).minutes.do(update_state)


def do_infinite_schedule_loop():
    while True:
        schedule.run_pending()
        time.sleep(SCHEDULER_TICK_INTERVAL_IN_SEC)


def update_state():
    blocker.update()


if __name__ == '__main__':
    main()
