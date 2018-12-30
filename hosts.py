from platform_dependent import detect_path_to_host_file, reset_dns

BLOCK_LINE_FORMAT = "%s    %s #cat_blocker\n"

default_redirect = "localhost"


class HostsFileFacade(object):
    def __init__(self, hosts_file_path_resolver=detect_path_to_host_file):
        self.path = hosts_file_path_resolver()

    def block_sites(self, urls):
        urls = set(urls)
        with open(self.path, "r+") as hosts:
            hosts_content = hosts.read()
            if not hosts_content.endswith("\n"):
                hosts.write("\n")
            for url in urls:
                if url not in hosts_content:
                    hosts.write(BLOCK_LINE_FORMAT % (default_redirect, url))

    def unblock_sites(self, urls):
        urls = set(urls)
        with open(self.path, "r+") as hosts:
            hosts_content = hosts.readlines()
            hosts.seek(0)
            for line in hosts_content:
                if len(list(filter(lambda x: x in line, urls))) == 0:
                    hosts.write(line)
            hosts.truncate()

    def get_currently_blocked_sites(self):
        blocked = set()
        with open(self.path, "r+") as hosts:
            for line in hosts.readlines():
                if "#cat_blocker" in line:
                    blocked.add(line.split("    ")[1].split(" ")[0])
        return blocked

    def restart_networking(self):
        reset_dns()

    def is_blocked(self, url):
        with open(self.path, "r+") as hosts:
            return BLOCK_LINE_FORMAT % (default_redirect, url) in hosts.read()
