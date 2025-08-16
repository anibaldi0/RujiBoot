# path: menus/wipe_usb_menu.py
# Description: USB wipe menu for RujiBoot (fast or full erase with confirmation)

import subprocess
from utils.console_util import clear_screen, safe_input
from utils.session_state_util import selected_usb
from utils.generic_validator_util import GenericValidator
import utils.log_util as log_util

def wipe_usb_menu(t: dict):
    """
    Interactive menu to wipe the selected USB device.
    """
    validator = GenericValidator()

    if selected_usb is None:
        print("[!] No USB device selected.")
        return

    device = selected_usb.get("device")
    model = selected_usb.get("model")
    size = selected_usb.get("size")

    while True:
        clear_screen()
        print("=== Wipe USB ===")
        print()
        print(f"[*] Selected device: {device} - {model} - {size}")
        print()
        print("1. " + t.get("wipe_fast", "Fast wipe (only first 10 MiB)"))
        print("2. " + t.get("wipe_full", "Full wipe (entire USB, slow)"))
        print("0. " + t.get("menu_cancel", "Cancel and return"))
        print()

        choice = safe_input(t.get("menu_prompt", "Choose an option: ")).strip()

        if choice not in ["0", "1", "2"]:
            print(t.get("error_invalid_option", "[!] Invalid option."))
            safe_input(t.get("prompt_continue", "Press Enter to try again..."))
            continue

        if choice == "0":
            return

        confirm1 = safe_input("[?] Type 'WIPE' to confirm: ").strip()
        if confirm1.upper() != "WIPE":
            print("[*] Operation cancelled.")
            return

        confirm2 = safe_input("[?] Type 'ERASE' to proceed: ").strip()
        if confirm2.upper() != "ERASE":
            print("[*] Operation cancelled.")
            return

        try:
            if choice == "1":
                print("[*] Wiping first 10 MiB of the USB...")
                subprocess.run(["sudo", "dd", "if=/dev/zero", f"of={device}", "bs=1M", "count=10", "status=progress"], check=True)
                print("[+] " + t.get("wipe_done", "Fast wipe completed."))
                if not log_util.ANONYMOUS_MODE:
                    log_util.log_event(f"WIPE_FAST - {device}")

            elif choice == "2":
                print("[*] Wiping entire USB (this may take several minutes)...")
                subprocess.run(["sudo", "dd", "if=/dev/zero", f"of={device}", "bs=4M", "status=progress"], check=True)
                print("[+] " + t.get("wipe_done", "Full wipe completed."))
                if not log_util.ANONYMOUS_MODE:
                    log_util.log_event(f"WIPE_FULL - {device}")

        except subprocess.CalledProcessError as e:
            print(f"[!] Wipe failed: {e}")
            if not log_util.ANONYMOUS_MODE:
                log_util.log_event(f"WIPE_FAILED - {device} - {e}")

        return
