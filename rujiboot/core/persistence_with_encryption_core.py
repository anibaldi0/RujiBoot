# path: core/persistence_with_encryption_core.py
# Description: Creates encrypted persistence partition with SWAP for Live USB

import os
import subprocess
import time
from utils.log_util import log_event
from core.usb_manager import get_device_size_bytes, unmount_usb_device  # ← agregado

def prepare_persistence_encrypted(device_path: str, iso_path: str, t: dict, password: str) -> bool:
    """
    Prepares a USB with encrypted persistence and a swap partition.
    """
    print("[*] " + t.get("partitioning_start", "Starting USB partitioning..."))
    log_event(f"PERSISTENCE_INIT (ENCRYPTED) - Device: {device_path}")

    try:
        print("[*] Unmounting all partitions...")
        unmount_usb_device(device_path)

        print("[*] Wiping first sectors of the USB...")
        subprocess.run(["sudo", "dd", "if=/dev/zero", f"of={device_path}", "bs=1M", "count=10"], check=True)

        usb_size_bytes = get_device_size_bytes(device_path)
        if not usb_size_bytes:
            print("[!] " + t.get("device_size_error", "Could not determine device size."))
            return False

        usb_size_mib = usb_size_bytes // (1024 * 1024)
        if usb_size_mib < 6144:
            print("[!] USB too small. Minimum required size is 6 GiB.")
            return False

        part1_end = 4096
        part2_end = 5120
        part3_end = usb_size_mib - 4

        subprocess.run(["sudo", "parted", device_path, "--script", "mklabel", "msdos"], check=True)
        subprocess.run(["sudo", "parted", device_path, "--script", "mkpart", "primary", "fat32", "1MiB", f"{part1_end}MiB"], check=True)
        subprocess.run(["sudo", "parted", device_path, "--script", "mkpart", "primary", "linux-swap", f"{part1_end}MiB", f"{part2_end}MiB"], check=True)
        subprocess.run(["sudo", "parted", device_path, "--script", "mkpart", "primary", "ext4", f"{part2_end}MiB", f"{part3_end}MiB"], check=True)

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
