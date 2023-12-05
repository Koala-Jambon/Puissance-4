from colorama import Style, Fore
import rich


def info_log(message):
    print(Fore.LIGHTMAGENTA_EX + f"@>{message}")

def successful_log(message):
    print(Fore.GREEN + f"#>{message}")

def error_log(message):
    print(Fore.RED + f"!>{message}")