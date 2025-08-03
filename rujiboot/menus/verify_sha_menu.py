# Path: menus/verify_sha_menu.py
# Description: Menu to verify SHA256 checksums of ISO files

from utils.console_util import clear_screen, safe_input
from utils.checksum_util import calculate_sha256
from menus.iso_selector_menu import ask_for_iso_path_interactive
from utils.generic_validator_util import GenericValidator

def verify_sha_menu(t: dict):
    """
    Menu for SHA256 checksum operations on ISO files.
    Allows calculating and comparing hashes.

    Args:
        t (dict): Translation dictionary
    """
    validator = GenericValidator()

    while True:
        clear_screen()
        print(t.get("verify_sha_title", "[*] SHA256 Verification"))
        print()
        print("1. " + t.get("verify_sha_calc", "Calculate SHA256 of local ISO"))
        print("2. " + t.get("verify_sha_check", "Compare ISO hash with expected value"))
        print("0. " + t.get("verify_sha_back", "Return to main menu"))
        print()

        raw_input = safe_input(t.get("menu_prompt", "Choose an option: "))
        try:
            choice = validator.validate_input(
                raw_input,
                expected_type="str",
                allowed_values=["0", "1", "2"],
                allow_empty=False
            )
        except ValueError as ve:
            print(t.get("invalid_option", str(ve)))
            safe_input(t.get("press_enter_continue", "Press Enter to try again..."))
            continue

        if choice == "1":
            iso_path = ask_for_iso_path_interactive(t)
            if not iso_path:
                continue

            result = calculate_sha256(iso_path, t)
            print()
            if result:
                print(t.get("sha_result", "[+] SHA256: ") + result)
                print(t.get("sha_notice_done", "[*] SHA256 calculation complete."))
            else:
                print(t.get("sha_error", "[!] Failed to calculate SHA256."))
            safe_input(t.get("press_enter_return", "Press Enter to return..."))

        elif choice == "2":
            iso_path = ask_for_iso_path_interactive(t)
            if not iso_path:
                continue

            actual = calculate_sha256(iso_path, t)
            print()
            if not actual:
                print(t.get("sha_error", "[!] Failed to calculate SHA256."))
                safe_input(t.get("press_enter_return", "Press Enter to return..."))
                continue

            expected = safe_input(t.get("ask_paste_sha", "[?] Paste expected SHA256: "), t).strip()
            if not expected:
                print(t.get("invalid_input", "[!] SHA256 value cannot be empty."))
                continue

            if actual.lower() == expected.lower():
                print(t.get("sha_match", "[+] SHA256 match: VALID ISO"))
            else:
                print(t.get("sha_mismatch", "[!] SHA256 mismatch: ISO may be corrupt"))
            safe_input(t.get("press_enter_return", "Press Enter to return..."))

        elif choice == "0":
            return
