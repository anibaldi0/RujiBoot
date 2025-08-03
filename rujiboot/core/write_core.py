# Path: core/write_core.py
# Description: Secure ISO writing to USB using dd with progress and log support

import os
import subprocess
from utils.log_util import log_event
from utils.simulate_util import is_simulation_enabled, simulate_write_process
from core.usb_manager import get_device_size_bytes
from utils import color_strings_util as color
from utils import session_state_util as session
from utils.usb_util import is_suspicious_label

def write_iso_to_device(iso_path: str, device_path: str, t: dict, simulate: bool = False, label: str = None) -> bool:
    """
    Writes an ISO file to a USB device using dd and shows progress.

    Args:
        iso_path (str): Path to the ISO file
        device_path (str): Target USB device path (e.g. /dev/sdX)
        t (dict): Translation dictionary
        simulate (bool): If True, simulate writing (dry run)
        label (str): Optional label to assign to the USB (if supported)

    Returns:
        bool: True if successful, False otherwise
    """
    # --- SUSPICIOUS LABEL WARNING ---
    try:
        label_value = session.selected_usb.get("label", "").strip().upper()
        if label_value and is_suspicious_label(label_value):
            print("[!] " + t.get("warn_usb_label", f"Warning: This USB has a critical system label: {label_value}"))
            print("    " + t.get("confirm_warning", "[!] This action may erase important system partitions."))
            confirm = input(t.get("confirm_question", "Are you sure? [y/N] ") + " ").strip().lower()
            if confirm != "y":
                print(t.get("confirm_cancelled", "[*] Action cancelled."))
                return False
    except Exception:
        pass  # fallback

    if simulate or is_simulation_enabled():
        return simulate_write_process(iso_path, device_path, t)

    print()
    print("[*] " + t.get("writing_start", "Starting ISO writing process..."))
    print("[*] " + t.get("writing_target", "Writing to device:") + f" {device_path}")
    print("[*] " + t.get("writing_source", "Using ISO file:") + f" {iso_path}")
    if label:
        print("[*] " + t.get("writing_label", "Requested label:") + f" {label}")

    log_event(f"WRITE_STARTED - ISO: {iso_path} TO: {device_path}")

    # === Validations ===
    if not os.path.isfile(iso_path):
        print("[!] ISO file not found.")
        log_event(f"WRITE_ABORTED - ISO not found: {iso_path}")
        return False

    if not os.path.exists(device_path):
        print("[!] Device not found.")
        log_event(f"WRITE_ABORTED - Device not found: {device_path}")
        return False

    # Check that ISO fits on USB
    iso_size = os.path.getsize(iso_path)
    usb_size = get_device_size_bytes(device_path)

    if usb_size is not None and iso_size > usb_size:
        print("[!] " + t.get("iso_too_big", "The ISO file is larger than the selected USB device."))
        print("[!] " + t.get("operation_aborted", "Operation aborted for safety."))
        log_event(f"WRITE_ABORTED - ISO too large ({iso_size}B) for USB ({usb_size}B)")
        return False

    print(f"[*] {t.get('writing_progress', 'Writing progress:')}")
    print("[*] This may take several minutes depending on ISO size and USB speed.")
    print()

    try:
        dd_cmd = [
            "sudo", "dd",
            f"if={iso_path}",
            f"of={device_path}",
            "bs=4M",
            "status=progress",
            "conv=fsync"
        ]

        result = subprocess.run(dd_cmd, capture_output=True, text=True)

        if result.stdout:
            print(result.stdout)

        if result.returncode == 0:
            print("\n[+] " + t.get("writing_success", "ISO written successfully to USB."))
            log_event(f"WRITE_SUCCESS - ISO: {iso_path} TO: {device_path}")

            if label:
                apply_label_to_device(device_path, label, t)

            return True
        else:
            print("[!] " + t.get("writing_failed", "Failed to write ISO to USB."))
            log_event(f"WRITE_FAILED - ISO: {iso_path} TO: {device_path}")

            stderr_lines = result.stderr.strip().splitlines()
            if stderr_lines:
                print("    [dd error output]:")
                for line in stderr_lines[-10:]:
                    print("    " + line)
                    if "Read-only file system" in line:
                        print("    [!] " + t.get("write_error_readonly", "The USB device is in read-only mode. Check for physical switch or permissions."))
                        log_event("WRITE_ERROR_DETAIL: USB is read-only (hardware lock?)")
                    elif "Permission denied" in line:
                        print("    [!] " + t.get("write_error_permission", "Permission denied. You may need to run RujiBoot with sudo."))
                        log_event("WRITE_ERROR_DETAIL: Permission denied")
                    elif "No such file or directory" in line:
                        print("    [!] " + t.get("write_error_missing", "Device or file not found. Check the path and USB connection."))
                        log_event("WRITE_ERROR_DETAIL: No such file or directory")
                    elif "Input/output error" in line:
                        print("    [!] " + t.get("write_error_io", "I/O error. The USB may be faulty or disconnected."))
                        log_event("WRITE_ERROR_DETAIL: I/O error")
            else:
                print("    [!] Unknown error. No output from dd.")
                log_event("WRITE_ERROR_DETAIL: dd failed silently")

            return False

    except Exception as e:
        print("[!]", t.get("writing_error", "Error during writing."))
        print("    ", t.get("writing_error_hint", "Possible causes: missing 'sudo', locked USB, write protection, or permission error."))
        print("    ", f"Details: {e}")
        log_event(f"WRITE_ERROR - {str(e)}")
        return False


def apply_label_to_device(device_path: str, label: str, t: dict):
    """
    Tries to apply a new label to the first partition of the device, using FAT32 label tool.

    Args:
        device_path (str): Base device path (e.g., /dev/sdX)
        label (str): Label to apply
        t (dict): Translations for user feedback
    """
    partition = device_path + "1"
    try:
        print("[*] Trying to apply label:", label)
        subprocess.run(["sudo", "fatlabel", partition, label], check=True)
        print(color.GREEN.get("label_success", "[+] Label applied successfully."))
        log_event(f"LABEL_SUCCESS - {partition} set to {label}")
    except Exception as e:
        print(color.YELLOW.get("label_failed", "[!] Could not apply label automatically."))
        log_event(f"LABEL_FAILED - {partition} - {str(e)}")
