# File: utils/log_util.py
# Logging utility for RujiBoot with optional anonymous mode and audit viewer

import os
from datetime import datetime

ANONYMOUS_MODE = False  # This flag is set in cli_main.py before menu logic

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "rujiboot.log")

def log_event(message: str):
    """
    Appends a timestamped event to the RujiBoot log file,
    unless anonymous mode is active.
    """
    if ANONYMOUS_MODE:
        return

    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def show_logs_menu(t: dict):
    """
    Displays a menu of logs in /logs for audit view mode.
    Allows user to select and view log content.
    """
    if ANONYMOUS_MODE:
        print("[!] " + t.get("anonymous_no_logs", "Logging is disabled in anonymous mode."))
        return

    if not os.path.isdir(LOG_DIR):
        print("[*] " + t.get("no_logs_found", "No audit logs available."))
        input(t.get("press_enter_return", "Press Enter to return to menu..."))
        return

    log_files = sorted(
        [f for f in os.listdir(LOG_DIR) if f.endswith(".log") and not f.startswith(".")],
        reverse=True
    )

    if not log_files:
        print("[*] " + t.get("no_logs_found", "No audit logs available."))
        input(t.get("press_enter_return", "Press Enter to return to menu..."))
        return

    print()
    print("=== " + t.get("logs_title", "RujiBoot - Audit Logs") + " ===\n")

    for idx, file in enumerate(log_files, 1):
        print(f"  {idx}. {file}")
    print("  0. " + t.get("cancel_return", "Cancel and return to menu"))
    print()

    choice = input("[?] " + t.get("choose_log_number", "Select log file to view: ")).strip()
    if choice == "0":
        return

    try:
        index = int(choice)
        if 1 <= index <= len(log_files):
            path = os.path.join(LOG_DIR, log_files[index - 1])
            print()
            print("=== " + log_files[index - 1] + " ===\n")
            with open(path, "r", encoding="utf-8") as f:
                print(f.read())
            print()
            input("[*] " + t.get("press_enter_return", "Press Enter to return to menu..."))
    except (ValueError, IndexError):
        print("[!] " + t.get("invalid_choice", "Invalid selection. Try again."))
        input(t.get("press_enter_return", "Press Enter to return to menu..."))
