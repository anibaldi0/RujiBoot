# path: menus/usb_menu.py
# usb_menu.py - USB-related menu logic for RujiBoot CLI

from utils.header_util import print_program_title_and_mode
from utils.console_util import clear_screen, safe_input
from core.usb_manager import detect_usb_devices
from utils.generic_validator_util import GenericValidator
from utils.usb_util import print_selected_usb_info

def show_usb_menu(t):
    """
    Displays the USB device selection menu and returns the selected USB dict.
    """
    clear_screen()
    print_program_title_and_mode()
    print("\n" + t.get("usb_selection_title", "Select a USB device:") + "\n")

    devices = detect_usb_devices()
    if not devices:
        print(t.get("no_usb_detected", "No USB devices detected."))
        safe_input(t.get("press_enter_return", "Press Enter to return to menu..."), t)
        return None

    for idx, dev in enumerate(devices, 1):
        label = dev.get("label") or "—"
        print(f"  {idx}. {dev['device']} - {dev['size']} - {dev['model']} - Label: {label}")
    print("  0. " + t.get("cancel_selection", "Cancel and return"))
    print()

    valid_choices = [str(i) for i in range(len(devices) + 1)]
    validator = GenericValidator(
        valid_choices=valid_choices,
        error_message=t.get("invalid_choice", "Invalid choice. Try again."),
        retry_message=t.get("press_enter_continue", "Press Enter to continue...")
    )

    while True:
        raw_input = safe_input(t.get("choose_iso_number", "Select a device number: "), t)
        try:
            choice = validator.validate_input(
                raw_input,
                expected_type="str",
                allowed_values=valid_choices,
                allow_empty=False
            )
        except ValueError as ve:
            print(t.get("invalid_choice", str(ve)))
            safe_input(t.get("press_enter_continue", "Press Enter to try again..."), t)
            continue

        if choice == "0":
            return None

        selected = devices[int(choice) - 1]
        clear_screen()
        print_program_title_and_mode()
        print_selected_usb_info(selected, t)
        return selected
