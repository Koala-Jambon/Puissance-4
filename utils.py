from colorama import Style, Fore
import rich
from yaspin import yaspin


def info_log(message):
    with yaspin():
    print(Fore.LIGHTMAGENTA_EX + f"@>{message}")

def successful_log(message):
    print(Fore.GREEN + f"#>{message}")

def error_log(message):
    print(Fore.RED + f"!>{message}")