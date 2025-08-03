# Path: menus/iso_selector_menu.py
# Description: Menu to interactively select and validate an ISO file

import os
import shlex
import readline
from utils.console_util import clear_screen
from utils.iso_selector_util import completer, validate_iso_path, try_auto_detect_iso
from utils.help_util import print_iso_shell_help
from utils.constants_util import EXIT_CODE, BACK_CODE

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

def ask_for_iso_path_interactive(t: dict, require_double: bool = True) -> str | None:
    """
    Interactive shell-style ISO selector with autocompletion and optional double confirmation.

    Args:
        t (dict): Translation dictionary
        require_double (bool): If True, asks 'Type ERASE' to confirm. If False, asks simple y/n.

    Returns:
        str | None: Validated ISO path or None if cancelled
    """
    clear_screen()
    print(t.get("interactive_shell_intro", "[*] Enter ISO path or use shell commands. Type 'help' for help."))
    print(t.get("current_directory", "Current directory:") + f" {os.getcwd()}")
    print()

    auto_iso = try_auto_detect_iso(t)
    if auto_iso:
        return auto_iso

    while True:
        try:
            user_input = input(f"RujiBoot [{os.getcwd()}]> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return None

        if not user_input:
            continue

        args = shlex.split(user_input)
        cmd = args[0]

        if cmd in ["exit", "cancel"]:
            return None
        
        elif cmd == EXIT_CODE:
            print(t.get("menu_exit", "Exiting..."))
            raise SystemExit()

        elif cmd == BACK_CODE:
            print(t.get("menu_return", "Returning to previous menu..."))
            return None


        elif cmd in ["help", "man"]:
            print_iso_shell_help(t)

        elif cmd == "pwd":
            print(t.get("current_directory", "Current directory:") + f" {os.getcwd()}")

        elif cmd == "ls":
            try:
                entries = [f for f in os.listdir() if not f.startswith(".")]
                for entry in sorted(entries):
                    if os.path.isdir(entry):
                        print(f"[DIR] {entry}")
                    elif entry.lower().endswith(".iso"):
                        print(f"[ISO] {entry}")
                print()
            except Exception as e:
                print(t.get("cmd_error", "[!] Command failed") + f": {e}")

        elif cmd == "cd":
            target_dir = os.path.expanduser(args[1]) if len(args) >= 2 else os.path.expanduser("~")
            try:
                os.chdir(target_dir)
                clear_screen()
                print(f"RujiBoot [{os.getcwd()}]>")
                auto_iso = try_auto_detect_iso(t)
                if auto_iso:
                    return auto_iso
            except Exception as e:
                print(t.get("cd_fail", "[!] Could not change directory: ") + str(e))

        elif cmd.lower().endswith(".iso"):
            valid_path = validate_iso_path(cmd, t)
            if not valid_path:
                continue

            print(t.get("confirm_use_this_iso", "[?] Do you want to use this ISO? [Y/n] "), end="")
            first = input().strip().lower()
            if first not in ["", "y", "yes"]:
                continue

            if require_double:
                print(t.get("confirm_double_prompt", "[?] Type 'ERASE' to confirm or exit: "), end="")
                second = input().strip()
                if second != "ERASE":
                    clear_screen()
                    print(t.get("confirm_failed", "[!] Final confirmation failed."))
                    continue

            return valid_path

        else:
            print(t.get("cmd_not_found", "[!] Unrecognized command or invalid path. Type 'help' for help."))
