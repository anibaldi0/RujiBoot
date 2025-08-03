# Path: utils/help_util.py
# Description: General help screen for RujiBoot CLI

from utils.header_util import print_program_title_and_help
from utils.console_util import clear_screen

def print_general_help(t):
    clear_screen()
    print_program_title_and_help()
    print()

    print(t.get("help_intro", "RujiBoot allows you to create bootable USB drives with GNU/Linux ISOs."))
    print()

    print(t.get("help_menu_explanation", "Main menu options:"))
    print("  1. " + t.get("menu_option_write_iso", "Write ISO to USB") + " - " + t.get("help_write_iso", "Select a USB, choose an ISO, optionally verify SHA256, and write."))
    print("  2. " + t.get("menu_option_unmount", "Unmount USB") + " - " + t.get("help_unmount", "Safely unmounts a USB device."))
    print("  3. " + t.get("menu_option_verify_checksum", "Check SHA256") + " - " + t.get("help_sha", "Checks ISO integrity against an expected SHA256."))
    print("  4. " + t.get("menu_option_help", "Help") + " - " + t.get("help_help", "Displays this help screen."))
    print("  5. " + t.get("menu_option_exit", "Exit") + " - " + t.get("help_exit", "Closes the program."))
    print()

def print_iso_shell_help(t):
    """
    Shows the help message for ISO shell commands.
    """
    print()
    print(t.get("shell_help", "[*] Available commands:"))
    print("  ls             - " + t.get("cmd_ls_desc", "List files in current directory"))
    print("  pwd            - " + t.get("cmd_pwd_desc", "Show current working directory"))
    print("  cd <dir>       - " + t.get("cmd_cd_desc", "Change directory"))
    print("  help / man     - " + t.get("cmd_help_desc", "Show this help message"))
    print("  exit / cancel  - " + t.get("cmd_exit_desc", "Cancel ISO selection"))
    print("  <path>.iso     - " + t.get("cmd_path_desc", "Enter ISO path manually (use TAB for autocomplete)"))
    print()
