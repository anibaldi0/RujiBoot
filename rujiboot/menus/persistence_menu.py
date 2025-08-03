# Path: menus/persistence_menu.py
# Description: Menu to select persistence mode (plain, encrypted, or none) for USB writing

from utils.console_util import clear_screen, safe_input
from utils.confirm_util import prompt_password_optional
from utils.generic_validator_util import GenericValidator
from core.prepare_persistence_core import prepare_persistent_usb

def persistence_menu(t: dict, device_path: str, iso_path: str) -> None:
    """
    Displays a menu to select the persistence type for ISO writing.

    Args:
        t (dict): Translation dictionary
        device_path (str): Path to the USB device (e.g., /dev/sdb)
        iso_path (str): Path to the ISO image
    """
    validator = GenericValidator()

    while True:
        clear_screen()
        print(t.get("menu_option_live_persistence", "[*] Create USB Live with optional persistence"))
        print()
        print("1. " + t.get("persistence_mode_1", "Yes, without encryption"))
        print("2. " + t.get("persistence_mode_2", "Yes, with encryption"))
        print("3. " + t.get("persistence_mode_3", "No, live mode only"))
        print("0. " + t.get("persistence_mode_0", "Cancel"))
        print()

        raw_choice = safe_input(t.get("menu_prompt", "Choose an option: "), t)

        try:
            choice = validator.validate_input(
                raw_choice,
                expected_type="str",
                allowed_values=["0", "1", "2", "3"],
                allow_empty=False
            )
        except ValueError as ve:
            print(t.get("invalid_option", str(ve)))
            safe_input(t.get("press_enter_continue", "Press Enter to try again..."), t)
            continue

        if choice == "0":
            return

        elif choice == "1":
            success = prepare_persistent_usb(device_path, iso_path, t, password=None)
            if success:
                print(t.get("persistence_done", "Persistence created successfully."))
            else:
                print(t.get("persistence_error", "Failed to create persistence."))
            safe_input(t.get("press_enter_return", "Press Enter to return..."), t)
            return

        elif choice == "2":
            password = prompt_password_optional(t)
            if password is None:
                return  # User skipped encryption
            success = prepare_persistent_usb(device_path, iso_path, t, password=password)
            if success:
                print(t.get("persistence_done", "Encrypted persistence created successfully."))
            else:
                print(t.get("persistence_error", "Failed to create encrypted persistence."))
            safe_input(t.get("press_enter_return", "Press Enter to return..."), t)
            return

        elif choice == "3":
            print(t.get("warn_no_persistence", "[*] No persistence will be created."))
            safe_input(t.get("press_enter_return", "Press Enter to return..."), t)
            return
