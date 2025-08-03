# path: cli/cli_main.py
# Description: CLI entry point for RujiBoot (language, mode, and main menu navigation)

import signal
import sys
from utils import color_strings_util as color
from utils.console_util import clear_screen
from menus.language_menu import select_language, LanguageMenuExit
from menus.mode_menu import select_mode
from menus.main_menu import main_menu
from utils.i18n_util import load_translations

# Block Ctrl+C globally
signal.signal(signal.SIGINT, lambda s, f: print(color.RED.get("ctrl_c_blocked", "\n[!] Ctrl+C blocked. Use option 0 to exit.")))

def run_cli():
    """
    Starts the CLI interaction for RujiBoot: language selection, mode selection, main menu.
    """
    try:
        while True:
            # Language selection
            lang_code = select_language()
            t = load_translations(lang_code)

            # Mode selection (logs / anonymous)
            mode_selected = select_mode(t)
            if not mode_selected:
                print(t.get("returning_language", "[*] Returning to language selection..."))
                continue  # Back to language menu

            # Main menu
            main_menu(t)
            break  # Exit after main menu finishes

    except LanguageMenuExit:
        print("\n[*] RujiBoot was closed by the user from the language selector.")
        sys.exit(0)
