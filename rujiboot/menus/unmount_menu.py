# path: menus/unmount_menu.py
# Description: Menu to unmount USB partitions safely

import subprocess
from utils.console_util import clear_screen, safe_input
from core.usb_manager import detect_usb_devices
from utils.generic_validator_util import GenericValidator
from utils.usb_util import print_selected_usb_info  # ← NUEVO

def unmount_menu(t: dict):
    """
    Allows the user to safely unmount a mounted USB partition.
    """
    clear_screen()
    print(t.get("menu_option_unmount", "[*] Unmount USB device"))
    print()

    devices = detect_usb_devices()
    mounted = []

    # Collect mounted partitions from detected USBs
    for dev in devices:
        if dev.get("mountpoint"):
            mounted.append(dev)

    if not mounted:
        print(t.get("no_mounts_found", "No mounted USB partitions found."))
        safe_input(t.get("press_enter_return", "Press Enter to return..."))
        return

    print(t.get("usb_selection_title", "Select a USB device to unmount:"))
    for i, d in enumerate(mounted, 1):
        print(f"  {i}. {d['device']} - {d['model']} - {d['mountpoint']}")
    print("  0. " + t.get("cancel_selection", "Cancel and return"))
    print()

    valid_options = [str(i) for i in range(len(mounted) + 1)]
    validator = GenericValidator(
        valid_choices=valid_options,
        error_message=t.get("invalid_option", "[!] Invalid input."),
        retry_message=t.get("press_enter_continue", "Press Enter to try again...")
    )

    choice = validator.get_validated_input(t.get("menu_prompt", "Choose an option: "), allow_empty=False).strip()
    if choice == "0":
        return

    index = int(choice)
    selected = mounted[index - 1]

    print_selected_usb_info(selected, t)

    print(t.get("unmounting", f"[*] Unmounting {selected['device']}..."))

    try:
        subprocess.run(["umount", selected["device"]], check=True)
        print(t.get("unmount_success", f"Successfully unmounted {selected['device']}"))
    except subprocess.CalledProcessError:
        print(t.get("unmount_failed", f"[!] Failed to unmount {selected['device']}"))

    safe_input(t.get("press_enter_return", "Press Enter to return..."))
