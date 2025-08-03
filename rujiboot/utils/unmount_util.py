# Path: utils/unmount_util.py
# Description: Utility to unmount all mounted partitions of a given USB device

import os
import subprocess
from utils.log_util import log_event

def unmount_all_partitions(device_path: str, t: dict) -> bool:
    """
    Unmounts all mounted partitions of a given USB device (e.g., /dev/sdb).

    Args:
        device_path (str): Base device path like /dev/sdb
        t (dict): Translation dictionary

    Returns:
        bool: True if all partitions were unmounted or none were mounted, False if any failed
    """
    if not device_path.startswith("/dev/sd"):
        print(t.get("invalid_device_path", "[!] Invalid device path."))
        return False

    print(t.get("unmounting_partitions", "[*] Checking and unmounting USB partitions..."))

    try:
        # List mounted partitions
        result = subprocess.run(["lsblk", "-ln", "-o", "NAME,MOUNTPOINT", device_path], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().splitlines()
        unmounted_all = True

        for line in lines[1:]:  # Skip the base device line
            parts = line.split()
            if len(parts) == 2:
                part_name, mount_point = parts
                full_part_path = "/dev/" + part_name

                print(t.get("unmounting", f"[!] Unmounting {full_part_path} from {mount_point}"))
                try:
                    subprocess.run(["sudo", "umount", full_part_path], check=True)
                    log_event(f"UNMOUNTED - {full_part_path}")
                except subprocess.CalledProcessError:
                    print(t.get("unmount_failed", f"[!] Failed to unmount {full_part_path}"))
                    log_event(f"UNMOUNT_FAILED - {full_part_path}")
                    unmounted_all = False

        if unmounted_all:
            print(t.get("unmounted_all", "[+] All USB partitions unmounted successfully."))
        else:
            print(t.get("unmounted_partial", "[!] Some partitions could not be unmounted."))
        return unmounted_all

    except subprocess.CalledProcessError as e:
        print(t.get("unmount_error", f"[!] Error checking USB partitions: {e}"))
        log_event(f"UNMOUNT_ERROR - {device_path} - {e}")
        return False
