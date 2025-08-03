# path: menus/write_iso_menu.py
# Description: Menu for writing ISO to USB with optional SHA256 verification and persistence support

import os
from utils.console_util import clear_screen, safe_input
from utils.usb_util import print_usb_header
from menus.iso_selector_menu import ask_for_iso_path_interactive
from utils.checksum_util import prompt_and_compare_sha256
from utils.confirm_util import confirm_action, prompt_password_optional
from utils.generic_validator_util import GenericValidator
from core.write_core import write_iso_to_device
from core.usb_manager import detect_usb_devices
from core.prepare_persistence_core import prepare_persistent_usb
from utils.breadcrumb_util import reset_breadcrumb, add_breadcrumb, get_breadcrumb_str
from utils.header_util import print_program_title_and_mode
import utils.session_state_util as session

def guess_default_label_from_iso(iso_path: str) -> str:
    return os.path.splitext(os.path.basename(iso_path))[0][:11].upper()

def write_iso_menu(t: dict):
    clear_screen()
    reset_breadcrumb()
    add_breadcrumb("Main")
    add_breadcrumb("Write ISO")

    print_program_title_and_mode()

    devices = detect_usb_devices()
    if not devices:
        print()
        print(t.get("no_usb_detected", "No USB devices detected."))
        safe_input(t.get("press_enter_return", "Press Enter to return..."))
        return

    print()
    print(t.get("usb_selection_title", "Select a USB device:"))
    for idx, dev in enumerate(devices, 1):
        label = dev.get("label") or "-"
        print(f"  {idx}. {dev['device']} - {dev['size']} - {dev['model']} - Label: {label}")
    print("  0. " + t.get("cancel_selection", "Cancel and return"))
    print()

    valid_choices = [str(i) for i in range(len(devices) + 1)]
    validator = GenericValidator()

    while True:
        raw_input = safe_input(t.get("choose_iso_number", "Select a device number: "), t)
        choice = validator.validate_input(
            raw_input,
            expected_type="str",
            allowed_values=valid_choices,
            allow_empty=False
        )

        if choice == "0":
            return
        selected_usb = devices[int(choice) - 1]
        session.selected_usb = selected_usb
        break

    iso_path = ask_for_iso_path_interactive(t)
    if not iso_path:
        safe_input(t.get("press_enter_return", "Press Enter to return..."))
        return

    clear_screen()
    print_program_title_and_mode()
    print_usb_header(session.selected_usb, t)
    print(">> Path: " + get_breadcrumb_str())
    print()

    while True:
        print(t.get("write_iso_flow_title", "[*] Select ISO write mode:"))
        print("1. " + t.get("write_iso_simple", "Write ISO only (direct mode)"))
        print("2. " + t.get("write_iso_with_persistence", "Write ISO with persistence"))
        print("3. " + t.get("write_iso_verify_first", "Verify SHA256 before writing"))
        print("0. " + t.get("write_iso_cancel", "Return to main menu"))
        print()

        raw_input = safe_input(t.get("menu_prompt", "Choose an option: "), t)
        try:
            choice = validator.validate_input(
                raw_input,
                expected_type="str",
                allowed_values=["1", "2", "3", "0"],
                allow_empty=False
            )
        except ValueError as e:
            print(t.get("invalid_option", str(e)))
            safe_input(t.get("press_enter_continue", "Press Enter to try again..."))
            continue

        if choice == "0":
            return

        if choice == "1":
            add_breadcrumb("Direct Mode")
            clear_screen()
            print_program_title_and_mode()
            print_usb_header(session.selected_usb, t)
            print(">> Path: " + get_breadcrumb_str())
            print()

            default_label = guess_default_label_from_iso(iso_path)
            label_prompt = t.get("ask_optional_label", "[?] Enter label (default: {default}): ").replace("{default}", default_label)
            label = safe_input(label_prompt, t).strip()
            if not label:
                label = default_label

            if confirm_action(t, "confirm_write_iso", require_double=True):
                success = write_iso_to_device(iso_path, session.selected_usb["device"], t, label=label)
                if success:
                    print(t.get("writing_success", "ISO written successfully."))
                else:
                    print(t.get("writing_failed", "Failed to write ISO."))
                safe_input(t.get("press_enter_return", "Press Enter to return..."))
            return

        elif choice == "2":
            add_breadcrumb("Persistence")

            while True:
                clear_screen()
                print_program_title_and_mode()
                print_usb_header(session.selected_usb, t)
                print(">> Path: " + get_breadcrumb_str())
                print()

                print(t.get("persistence_mode_title", "Do you want to enable persistence?"))
                print("1. " + t.get("persistence_mode_1", "Yes, without encryption"))
                print("2. " + t.get("persistence_mode_2", "Yes, with encryption"))
                print("3. " + t.get("persistence_mode_3", "No, just write live ISO"))
                print("0. " + t.get("persistence_mode_0", "Cancel"))
                print()

                mode_input = safe_input(t.get("menu_prompt", "Choose an option: "), t).strip()
                if mode_input not in ["0", "1", "2", "3"]:
                    print(t.get("invalid_option", "[!] Invalid option."))
                    safe_input(t.get("press_enter_continue", "Press Enter to try again..."))
                    continue

                if mode_input == "0":
                    return

                if mode_input == "3":
                    print(t.get("warn_no_verification", "[!] Persistence was skipped."))
                    safe_input(t.get("press_enter_return", "Press Enter to return..."))
                    return

                if not confirm_action(t, "confirm_write_iso", require_double=True):
                    safe_input(t.get("press_enter_return", "Press Enter to return..."))
                    return

                password = None
                if mode_input == "2":
                    add_breadcrumb("Encrypted")
                    password = prompt_password_optional(t)
                else:
                    add_breadcrumb("No Encryption")

                clear_screen()
                print_program_title_and_mode()
                print_usb_header(session.selected_usb, t)
                print(">> Path: " + get_breadcrumb_str())
                print()

                success = prepare_persistent_usb(
                    device_path=session.selected_usb["device"],
                    iso_path=iso_path,
                    t=t,
                    password=password
                )

                if success:
                    print(t.get("persistence_done", "USB with persistence is ready."))
                else:
                    print(t.get("persistence_error", "Error preparing persistent USB."))
                safe_input(t.get("press_enter_return", "Press Enter to return..."))
                return

        elif choice == "3":
            add_breadcrumb("Verify ISO")
            clear_screen()
            print_program_title_and_mode()
            print_usb_header(session.selected_usb, t)
            print(">> Path: " + get_breadcrumb_str())
            print()

            verified = prompt_and_compare_sha256(iso_path, t)

            if verified is True:
                print(t.get("sha_match", "SHA256 verification successful."))
                safe_input(t.get("press_enter_continue", "Press Enter to continue..."))
            elif verified is False:
                print(t.get("sha_mismatch", "SHA256 verification failed or was cancelled."))
                safe_input(t.get("press_enter_return", "Press Enter to return..."))
                return
            elif verified is None:
                print(t.get("sha_skipped", "SHA256 verification was skipped."))
                print(t.get("warning_proceed_risk", "Proceeding at your own risk."))
                safe_input(t.get("press_enter_continue", "Press Enter to continue..."))

            clear_screen()
            print_program_title_and_mode()
            print_usb_header(session.selected_usb, t)
            print(">> Path: " + get_breadcrumb_str())
            print()

            default_label = guess_default_label_from_iso(iso_path)
            label_prompt = t.get("ask_optional_label", "[?] Enter label (default: {default}): ").replace("{default}", default_label)
            label = safe_input(label_prompt, t).strip()
            if not label:
                label = default_label

            if confirm_action(t, "confirm_write_iso", require_double=True):
                success = write_iso_to_device(iso_path, session.selected_usb["device"], t, label=label)
                if success:
                    print(t.get("writing_success", "ISO written successfully."))
                else:
                    print(t.get("writing_failed", "Failed to write ISO."))
                safe_input(t.get("press_enter_return", "Press Enter to return..."))
            return
