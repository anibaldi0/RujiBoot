# File: core/persistence_with_encryption_core.py
# Description: Creates encrypted persistence partition with SWAP for Live USB

import os
import subprocess
import time
from utils.log_util import log_event

def prepare_persistence_encrypted(device_path: str, iso_path: str, t: dict, password: str) -> bool:
    """
    Prepares a USB with encrypted persistence and a swap partition.

    Args:
        device_path (str): e.g., /dev/sdb
        iso_path (str): Path to ISO
        t (dict): Translations
        password (str): Encryption password

    Returns:
        bool: True if success, False otherwise
    """
    print("[*] " + t.get("partitioning_start", "Starting USB partitioning..."))
    log_event(f"PERSISTENCE_INIT (ENCRYPTED) - Device: {device_path}")

    try:
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

        print("[*] " + t.get("persistence_encrypted", "Creating encrypted persistence..."))
        subprocess.run(["sudo", "cryptsetup", "luksFormat", part_persist], input=f"{password}\n".encode(), check=True)

        # Close if already opened from previous failed run
        try:
            subprocess.run(["sudo", "cryptsetup", "status", "persistence_encrypted"],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("[*] Mapper 'persistence_encrypted' already active. Closing it...")
            subprocess.run(["sudo", "cryptsetup", "close", "persistence_encrypted"], check=True)
        except subprocess.CalledProcessError:
            pass

        subprocess.run(["sudo", "cryptsetup", "open", part_persist, "persistence_encrypted"],
                       input=f"{password}\n".encode(), check=True)

        subprocess.run(["sudo", "mkfs.ext4", "-L", "persistence", "/dev/mapper/persistence_encrypted"], check=True)

        os.makedirs("/mnt/persistence", exist_ok=True)
        subprocess.run(["sudo", "mount", "/dev/mapper/persistence_encrypted", "/mnt/persistence"], check=True)

        with open("/mnt/persistence/persistence.conf", "w") as f:
            f.write("/ union\n")

        subprocess.run(["sudo", "umount", "/mnt/persistence"])
        subprocess.run(["sudo", "cryptsetup", "close", "persistence_encrypted"])

        print("[+] " + t.get("persistence_done", "Encrypted persistence partition ready."))
        log_event(f"PERSISTENCE_SUCCESS (ENCRYPTED) - {device_path}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"[!] {t.get('persistence_error', 'Error during encrypted persistence setup')}: {e}")
        log_event(f"PERSISTENCE_FAILED (ENCRYPTED) - {e}")
        return False
