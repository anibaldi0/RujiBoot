# path: menus/mode_menu.py
# Description: Execution mode selection for RujiBoot (audit or anonymous)

from utils.console_util import clear_screen, safe_input
from utils.header_util import show_program_title
import utils.log_util as log_util
from utils.generic_validator_util import GenericValidator

def select_mode(t: dict) -> bool:
    """
    Displays the mode selection menu.
    Sets the logging mode (audit or anonymous) in log_util.

    Args:
        t (dict): Translations dictionary

    Returns:
        bool: True if mode was selected, False if user chose to go back
    """
    validator = GenericValidator()

    while True:
        clear_screen()
        print(show_program_title())
        print()
        print(t.get("mode_title", "Select execution mode:"))
        print("1. " + t.get("mode_logs", "Audit mode"))
        print("2. " + t.get("mode_anonymous", "Anonymous mode"))
        print("3. " + t.get("mode_help", "Help: What is each mode?"))
        print("9. " + t.get("menu_option_return_to_mode", "Return to previous menu"))
        print()

        raw_input = safe_input(t.get("menu_prompt", "Choose an option: "))

        try:
            choice = validator.validate_input(
                raw_input,
                expected_type="str",
                allowed_values=["9", "1", "2", "3"],
                allow_empty=False
            )
        except ValueError as ve:
            print(t.get("invalid_option", str(ve)))
            safe_input(t.get("press_enter_continue", "Press Enter to try again..."))
            continue

        if choice == "9" or choice == "__rujiboot_back__":
            return False

        elif choice == "1":
            log_util.ANONYMOUS_MODE = False
            return True

        elif choice == "2":
            log_util.ANONYMOUS_MODE = True
            return True

        elif choice == "3":
            print()
            print(t.get(
                "mode_help_text",
                "In audit mode, RujiBoot stores events like SHA256 match, write success/failure, etc. In anonymous mode, no logs are stored."
            ))
            print()
            safe_input(t.get("press_enter_continue", "Press Enter to continue..."))
