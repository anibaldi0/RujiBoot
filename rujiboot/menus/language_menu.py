# path: menus/language_menu.py
# Description: Language selector menu for RujiBoot CLI

from utils.console_util import clear_screen, safe_input
from utils.header_util import show_program_title
from utils.generic_validator_util import GenericValidator

# Custom exception to indicate exit from the language menu
class LanguageMenuExit(Exception):
    """Raised when the user chooses to exit from the language selection."""
    pass

def select_language() -> str:
    """
    Displays the language selection menu.

    Returns:
        str: Language code ("es", "pt", "en")

    Raises:
        LanguageMenuExit: If the user selects option 0 to exit
    """
    validator = GenericValidator()

    while True:
        clear_screen()
        print(show_program_title())
        print()
        print("Select language:")
        print("1. " + "Spanish")
        print("2. " + "Portuguese")
        print("3. " + "English")
        print("0. " + "Exit")

        choice = safe_input("Choose an option: ").strip()

        try:
            validated = validator.validate_input(
                user_input=choice,
                expected_type="str",
                allowed_values=["1", "2", "3", "0"]
            )
        except ValueError as ve:
            print(str(ve))
            safe_input("Press Enter to try again...")
            continue

        if validated == "0" or validated == "__rujiboot_exit__":
            print("Exiting...")
            raise LanguageMenuExit()

        return {"1": "es", "2": "pt", "3": "en"}[validated]
