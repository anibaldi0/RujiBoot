# File: utils/console_util.py
# Utility to clear the console screen and handle safe input

import os
import signal

def clear_screen():
    os.system("clear")


def safe_input(prompt: str = "", t: dict = None) -> str:
    try:
        value = input(prompt).strip()
        if value.lower() in ["salir", "exit", "cancel"]:
            print()
            msg = "[*] Operation cancelled by user."
            if t:
                msg = t.get("cancelled_by_user", msg)
            print(msg)
            return "__rujiboot_exit__"
        return value
    except (EOFError, KeyboardInterrupt):
        print()
        msg = "[!] Exit blocked. Use option 0 to exit."
        if t:
            msg = t.get("blocked_exit_message", msg)
        print(msg)
        return ""
