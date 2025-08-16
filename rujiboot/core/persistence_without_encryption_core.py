# path: core/persistence_without_encryption_core.py
# Description: Creates non-encrypted persistence partition with SWAP for Live USB

import os
import subprocess
import time
from utils.log_util import log_event
from core.usb_manager import unmount_usb_device  # ← agregado

def prepare_persistence_plain(device_path: str, iso_path: str, t: dict) -> bool:
    """
    Prepares a USB with non-encrypted persistence and a swap partition.
    """
    print("[*] " + t.get("partitioning_start", "Starting USB partitioning..."))
    log_event(f"PERSISTENCE_INIT (PLAIN) - Device: {device_path}")

    try:
        print("[*] Unmounting all partitions...")
        unmount_usb_device(device_path)

        print("[*] Wiping first sectors of the USB...")
        subprocess.run(["sudo", "dd", "if=/dev/zero", f"of={device_path}", "bs=1M", "count=10"], check=True)

        subprocess.run(["sudo", "parted", device_path, "--script", "mklabel", "msdos"], check=True)
        subprocess.run(["sudo", "parted", device_path, "--script", "mkpart", "primary", "fat32", "1MiB", "4096MiB"], check=True)
        subprocess.run(["sudo", "parted", device_path, "--script", "mkpart", "primary", "linux-swap", "4096MiB", "5120MiB"], check=True)
        subprocess.run(["sudo", "parted", device_path, "--script", "mkpart", "primary", "ext4", "5120MiB", "100%"], check=True)

        print("[+] " + t.get("partitioning_done", "Partitioning completed."))
        time.sleep(2)

        part_boot = device_path + "1"
        part_swap = device_path + "2"
        part_persist = device_path + "3"

        print("[*] " + t.get("writing_start", "Writing ISO to device..."))
        subprocess.run(["sudo", "dd", f"if={iso_path}", f"of={device_path}", "bs=4M", "status=progress", "conv=fsync"], check=True)
        log_event(f"PERSISTENCE_ISO_WRITTEN - ISO written to {device_path}")

        print("[*] " + t.get("swap_creating", "Creating swap partition..."))
        subprocess.run(["sudo", "mkswap", part_swap], check=True)
        log_event(f"SWAP_CREATED - {part_swap}")

        print("[*] " + t.get("persistence_plain", "Creating plain persistence..."))
        subprocess.run(["sudo", "mkfs.ext4", "-L", "persistence", part_persist], check=True)

        os.makedirs("/mnt/persistence", exist_ok=True)
        subprocess.run(["sudo", "mount", part_persist, "/mnt/persistence"], check=True)

        with open("/mnt/persistence/persistence.conf", "w") as f:
            f.write("/ union\n")

        subprocess.run(["sudo", "umount", "/mnt/persistence"])

        print("[+] " + t.get("persistence_done", "Plain persistence partition ready."))
        log_event(f"PERSISTENCE_SUCCESS (PLAIN) - {device_path}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"[!] {t.get('persistence_error', 'Error during plain persistence setup')}: {e}")
        log_event(f"PERSISTENCE_FAILED (PLAIN) - {e}")
        return False
