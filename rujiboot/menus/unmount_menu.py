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
    validator = GenericValidator()

    while True:
        raw = safe_input(t.get("menu_prompt", "Choose an option: ")).strip()
        try:
            choice = validator.validate_input(
                user_input=raw,
                expected_type="str",
                allowed_values=valid_options,
                allow_empty=False
            )
            break
        except ValueError as e:
            print(e)
            safe_input(t.get("press_enter_continue", "Press Enter to try again..."))

    if choice == "0":
        return

    index = int(choice)
    selected = mounted[index - 1]

    print_selected_usb_info(selected, t)

    mountpoint = selected.get("mountpoint")
    if not mountpoint:
        print(t.get("unmount_failed", f"[!] No mountpoint found for {selected['device']}"))
        safe_input(t.get("press_enter_return", "Press Enter to return..."))
        return

    print(t.get("unmounting", f"[*] Unmounting {mountpoint}..."))

    try:
        subprocess.run(["umount", mountpoint], check=True)
        print(t.get("unmount_success", f"Successfully unmounted {mountpoint}"))
    except subprocess.CalledProcessError:
        print(t.get("unmount_failed", f"[!] Failed to unmount {mountpoint}"))

    safe_input(t.get("press_enter_return", "Press Enter to return..."))
