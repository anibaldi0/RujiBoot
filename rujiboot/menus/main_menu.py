# path: menus/main_menu.py
# Description: Main CLI menu for RujiBoot (ISO, checksum, logs, persistence, etc.)

from utils.console_util import clear_screen, safe_input
from utils.header_util import print_program_title_and_mode
import utils.log_util as log_util
from utils.generic_validator_util import GenericValidator
from utils.usb_util import print_usb_header
from utils.breadcrumb_util import reset_breadcrumb, add_breadcrumb, get_breadcrumb_str
from utils.session_state_util import selected_usb

def main_menu(t: dict):
    validator = GenericValidator()

    while True:
        clear_screen()
        reset_breadcrumb()
        add_breadcrumb("Main")

        print_program_title_and_mode()
        if selected_usb is not None:
            print_usb_header(selected_usb, t)

        print(">> Path: " + get_breadcrumb_str())
        print()

        print("1. " + t.get("menu_write_iso", "Write ISO to USB"))
        print("2. " + t.get("menu_unmount", "Unmount USB"))
        print("3. " + t.get("menu_verify_sha", "Verify SHA256 of ISO"))
        print("4. " + t.get("menu_help", "Help"))

        if not log_util.ANONYMOUS_MODE:
            print("5. " + t.get("menu_logs", "View logs"))

        print("9. " + t.get("menu_return", "Return to previous menu"))
        print("0. " + t.get("menu_exit", "Exit"))
        print()

        valid_choices = ["0", "1", "2", "3", "4", "9"]
        if not log_util.ANONYMOUS_MODE:
            valid_choices.append("5")

        raw_input = safe_input(t.get("menu_prompt", "Choose an option: "))

        try:
            choice = validator.validate_input(
                raw_input,
                expected_type="str",
                allowed_values=valid_choices,
                allow_empty=False
            )
        except ValueError as ve:
            print(t.get("error_invalid_option", str(ve)))
            safe_input(t.get("prompt_continue", "Press Enter to try again..."))
            continue

        if choice == "0" or choice == "__rujiboot_exit__":
            print(t.get("menu_exit", "Exiting..."))
            break

        elif choice == "1":
            from menus.write_iso_menu import write_iso_menu
            write_iso_menu(t)
            safe_input(t.get("prompt_return", "Press Enter to return..."))

        elif choice == "2":
            from menus.unmount_menu import unmount_menu
            unmount_menu(t)
            safe_input(t.get("prompt_return", "Press Enter to return..."))

        elif choice == "3":
            from menus.verify_sha_menu import verify_sha_menu
            verify_sha_menu(t)
            safe_input(t.get("prompt_return", "Press Enter to return..."))

        elif choice == "4":
            from utils.help_util import print_general_help, print_iso_shell_help
            print_general_help(t)
            print_iso_shell_help(t)
            safe_input(t.get("prompt_return", "Press Enter to return..."))

        elif choice == "5" and not log_util.ANONYMOUS_MODE:
            log_util.show_logs_menu(t)
            safe_input(t.get("prompt_return", "Press Enter to return..."))

        elif choice == "9":
            print(t.get("menu_return_mode", "[*] Returning to mode selection..."))
            from menus.mode_menu import select_mode
            selected = select_mode(t)
            if selected:
                continue  # vuelve a este main_menu con nuevo modo
            else:
                print(t.get("menu_exit", "Exiting..."))
                break

