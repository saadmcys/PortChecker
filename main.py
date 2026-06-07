import os
from scan import scan

# ANSI COLORS
RESET = "\033[0m"

WHITE = "\033[97m"
YELLOW = "\033[93m"
RED = "\033[91m"

BWHITE = "\033[1;97m"
BYELLOW = "\033[1;93m"
BRED = "\033[1;91m"


def start_scan():
    scan()


def clear():
    os.system("cls" if os.name == "nt" else "clear")


while True:

    clear()

    BANNER = f"""
{RED}+=============================================================================+{RESET}
{RED}|{RESET}{YELLOW}     ____            _      ____ _               _               _   ___     {RESET}{RED}|{RESET}
{RED}|{RESET}{YELLOW}    |  _ \\ ___  _ __| |_   / ___| |__   ___  ___| | _____ _ __  / | / _ \\    {RESET}{RED}|{RESET}
{RED}|{RESET}{YELLOW}    | |_) / _ \\| '__| __| | |   | '_ \\ / _ \\/ __| |/ / _ \\ '__| | || | | |   {RESET}{RED}|{RESET}
{RED}|{RESET}{YELLOW}    |  __/ (_) | |  | |_  | |___| | | |  __/ (__|   <  __/ |    | || |_| |   {RESET}{RED}|{RESET}
{RED}|{RESET}{YELLOW}    |_|   \\___/|_|   \\__|  \\____|_| |_|\\___|\\___|_|\\_\\___|_|    |_(_)___/    {RESET}{RED}|{RESET}
{RED}+=============================================================================+{RESET}
{RED}|                                                                             |{RESET}
{RED}|   {YELLOW}github : saadm.cys {RED}* {YELLOW}this tool by zliss team {RED}* {YELLOW}instagram : saadm.cys   {RESET}{RED}|{RESET}
{RED}|                                                                             |{RESET}
{RED}+=============================================================================+{RESET}
"""

    print(BANNER)

    choice = input(
        f"\n{YELLOW}Start scanning? (Y/N): {RESET}"
    ).strip().lower()

    if choice in ["y", "yes"]:

        try:

            while True:

                start_scan()

                scan_again = input(
                    f"\n{YELLOW}Do you want to scan again? (Y/N): {RESET}"
                ).strip().lower()

                if scan_again not in ["y", "yes"]:

                    exit_choice = input(
                        f"\n{RED}Do you want to exit? (Y/N): {RESET}"
                    ).strip().lower()

                    if exit_choice in ["y", "yes"]:

                        print(f"\n{RED}[INFO] Program terminated.{RESET}")
                        break

                    else:
                        break

        except KeyboardInterrupt:

            exit_choice = input(
                f"\n\n{RED}Do you want to exit? (Y/N): {RESET}"
            ).strip().lower()

            if exit_choice in ["y", "yes"]:

                print(f"\n{RED}[INFO] Program terminated.{RESET}")
                break

    elif choice in ["n", "no"]:
        break