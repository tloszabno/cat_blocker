from datetime import datetime


class Blocker(object):
    def __init__(self, hosts_file_facade, config):
        self.hosts_file_facade = hosts_file_facade
        self.config = config

    def update(self):
        self.config.update_config()
        to_block, to_unblock = self.get_sites_to_block_and_unblock(datetime.now())

        is_there_any_changes = len(to_block) > 0 or len(to_unblock) > 0
        if is_there_any_changes:
            print("Applying changes: sites_to_block=%s, sites_to_unblock=%s" % (str(to_block), str(to_unblock)))
            self.hosts_file_facade.unblock_sites(to_unblock)
            self.hosts_file_facade.block_sites(to_block)
            self.hosts_file_facade.restart_networking()

    def get_sites_to_block_and_unblock(self, now):
        sites_which_now_should_be_blocked = self.config.get_all_blocked_sites_for(now)
        sites_which_are_blocked = self.hosts_file_facade.get_currently_blocked_sites()
        to_block = sites_which_now_should_be_blocked - sites_which_are_blocked
        to_unblock = sites_which_are_blocked - sites_which_now_should_be_blocked
        return to_block, to_unblock
