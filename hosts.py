import platform

BLOCK_LINE_FORMAT = "%s    %s\n"

default_redirect = "localhost"


def detect_path_to_host_file():
    system = platform.system()
    if system == "Windows": return "C:\Windows\System32\drivers\etc\hosts"
    if system == "Darwin": return "/etc/hosts"
    if system == "Linux": return "/etc/hosts"
    raise Exception("Unknown platform: " + system)


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

    def is_blocked(self, url):
        with open(self.path, "r+") as hosts:
            return BLOCK_LINE_FORMAT % (default_redirect, url) in hosts.read()
