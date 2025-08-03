# File: utils/iso_selector_util.py
# Description: Utilities for ISO detection, selection and confirmation

import os
import readline
from utils.console_util import clear_screen
from utils.iso_validate_path_util import validate_iso_path

# === Autocompletion ===
def completer(text, state):
    options = []
    try:
        entries = os.listdir()
        for entry in entries:
            if entry.startswith(text):
                if os.path.isdir(entry) or entry.lower().endswith(".iso"):
                    options.append(entry + ("/" if os.path.isdir(entry) else ""))
        return options[state]
    except IndexError:
        return None

# Setup readline once on import
readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

# === Simple confirmation for selected ISO ===
def simple_confirm_selection(iso_path, t) -> bool:
    """
    Asks user for a simple yes/no confirmation to use the selected ISO.

    Args:
        iso_path (str): Absolute path to ISO
        t (dict): Translations dictionary

    Returns:
        bool: True if confirmed, False otherwise
    """
    print("[?] " + t.get("confirm_use_this_iso", "Use this ISO? [Y/n] "), end="")
    answer = input().strip().lower()
    return answer in ["", "y", "yes"]

# === Auto-detect and allow choosing one ISO ===
def try_auto_detect_iso(t) -> str | None:
    """
    Detects ISO files in the current directory and allows user to select one.

    Args:
        t (dict): Translations dictionary

    Returns:
        str | None: Validated ISO path, or None if cancelled
    """
    while True:
        clear_screen()
        iso_files = [f for f in os.listdir() if f.lower().endswith(".iso")]
        if not iso_files:
            return None

        print(f"RujiBoot [{os.getcwd()}]>")
        print("[*] " + t.get("multiple_isos_found", "ISOs detected in current directory:"))
        for idx, iso in enumerate(iso_files, start=1):
            print(f"  {idx}. {iso}")
        print("  0. " + t.get("cancel_selection", "Cancel and return to prompt"))
        print()

        selection = input("[?] " + t.get("choose_iso_number", "Select ISO number: ")).strip()
        if selection == "0":
            clear_screen()
            return None

        try:
            index = int(selection)
            if 1 <= index <= len(iso_files):
                selected_iso = os.path.abspath(iso_files[index - 1])
                clear_screen()
                print("[+] " + t.get("valid_iso_selected", "Valid ISO selected:") + f" {selected_iso}")
                if simple_confirm_selection(selected_iso, t):
                    if validate_iso_path(selected_iso, t):
                        return selected_iso
                else:
                    print("[*] " + t.get("press_enter_return", "Press Enter to return to ISO menu..."))
                    input()
                    clear_screen()
            else:
                print("[!] " + t.get("invalid_choice", "Invalid selection. Try again."))
        except ValueError:
            print("[!] " + t.get("invalid_choice", "Invalid selection. Try again."))
