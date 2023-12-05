import time

from colorama import Style, Fore
import rich
from yaspin import yaspin
from yaspin.spinners import Spinners


def info_log(message):
    message = Fore.BLUE + message
    with yaspin(Spinners.earth, text=message) as sp:
        time.sleep(2)




def successful_log(message):
    print(Fore.GREEN + f"#>{message}")

def error_log(message):
    print(Fore.RED + f"!>{message}")