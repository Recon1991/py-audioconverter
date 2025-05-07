from colorama import Fore, Style, init
import datetime

init(autoreset=True)

def log_info(message):
    print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + message)

def log_success(message):
    print(Fore.GREEN + "[SUCCESS] " + Style.RESET_ALL + message)

def log_warning(message):
    print(Fore.YELLOW + "[WARNING] " + Style.RESET_ALL + message)

def log_error(message):
    print(Fore.RED + "[ERROR] " + Style.RESET_ALL + message)

def log_to_file(log_file, message):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")
