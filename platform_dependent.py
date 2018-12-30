import platform
import subprocess


def detect_path_to_host_file():
    system = platform.system()
    if system == "Windows":
        return "C:\Windows\System32\drivers\etc\hosts"
    if system == "Darwin":
        return "/etc/hosts"
    if system == "Linux":
        return "/etc/hosts"
    raise Exception("Unknown platform: " + system)


def reset_dns():
    system = platform.system()
    restart_network_command = ""
    if system == "Windows":
        restart_network_command = ["ipconfig", "/flushdns"]
    if system == "Darwin":
        restart_network_command = ["dscacheutil", "-flushcache"]
    if system == "Linux":
        restart_network_command = ["systemctl", "restart", "NetworkManager.service"]
    print("Restarting networking")
    subprocess.check_call(restart_network_command)
