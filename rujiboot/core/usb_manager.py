# File: core/usb_manager.py
# USB management functions: detection, writing, validation and unmount

import subprocess
import json
import re
import time
from utils.simulate_util import is_simulation_enabled
from utils.log_util import log_event
from utils.generic_validator_util import GenericValidator
from utils.usb_util import is_suspicious_label, is_usb_large_enough  # NUEVOS IMPORTS

validator = GenericValidator()

def detect_usb_devices():
    """
    Detects connected USB devices using lsblk and sysfs.

    Returns:
        List of dictionaries with device info.
    """
    devices = []

    try:
        output = subprocess.check_output(
            ["lsblk", "-J", "-o", "NAME,MODEL,SIZE,MOUNTPOINT,RM,TRAN,LABEL"],
            text=True
        )
        lsblk_data = json.loads(output)

        for device in lsblk_data.get("blockdevices", []):
            if device.get("rm") != 1:
                continue
            if device.get("tran") != "usb":
                continue

            mountpoint = device.get("mountpoint", "")
            label = device.get("label", "")

            if "children" in device:
                for part in device["children"]:
                    if not mountpoint and part.get("mountpoint"):
                        mountpoint = part["mountpoint"]
                    if not label and part.get("label"):
                        label = part["label"]

            device_info = {
                "device": "/dev/" + device["name"],
                "model": device.get("model", "").strip(),
                "size": device.get("size", ""),
                "label": label if label else None,
                "mountpoint": mountpoint if mountpoint else None,
                "removable": True
            }

            devices.append(device_info)

    except Exception as e:
        print(f"[!] Error while detecting USB devices: {e}")

    return devices


def unmount_usb_device(device_path):
    """
    Unmounts all partitions of the given device.

    Args:
        device_path (str): Full path to device (e.g., /dev/sdb)

    Returns:
        bool: True if all partitions were unmounted, False otherwise
    """
    success = True

    try:
        output = subprocess.check_output(
            ["lsblk", "-J", "-o", "NAME,MOUNTPOINT"],
            text=True
        )
        data = json.loads(output)
        device_name = device_path.replace("/dev/", "")
        partitions = []

        for d in data["blockdevices"]:
            if d["name"] == device_name and "children" in d:
                for child in d["children"]:
                    part_path = "/dev/" + child["name"]
                    if child.get("mountpoint"):
                        partitions.append(part_path)

        for part in partitions:
            try:
                print(f"[*] Unmounting {part} ...")
                subprocess.run(["udisksctl", "unmount", "-b", part], check=True)
            except Exception:
                try:
                    subprocess.run(["umount", part], check=True)
                except Exception as e:
                    print(f"[!] Failed to unmount {part}: {e}")
                    success = False

    except Exception as e:
        print(f"[!] Error while unmounting device: {e}")
        return False

    return success


def format_usb_device(device_path):
    """
    Formats the USB device with FAT32 filesystem using mkfs.vfat.
    If simulation mode is enabled, performs a dry-run with fake progress.

    Args:
        device_path (str): Full path to device (e.g., /dev/sdb)

    Returns:
        bool: True if formatting was successful (or simulated), False otherwise
    """
    if is_simulation_enabled():
        print(f"[*] Simulating format of {device_path} to FAT32...")
        log_event(f"FORMAT_SIMULATION_STARTED - {device_path}")
        for i in range(1, 11):
            bar = "[" + "#" * i + " " * (10 - i) + "]"
            print(f"\r{bar} {i*10}%", end="", flush=True)
            time.sleep(0.1)
        print("\n[+] Format simulation completed.")
        log_event(f"FORMAT_SIMULATION_DONE - {device_path}")
        return True

    try:
        print(f"[*] Unmounting {device_path} before formatting...")
        if not unmount_usb_device(device_path):
            print(f"[!] Could not unmount all partitions of {device_path}.")
            return False

        print(f"[*] Formatting {device_path} to FAT32...")
        subprocess.run(["sudo", "mkfs.vfat", "-F", "32", device_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Format failed: {e}")
        return False


def change_usb_label(device_path, new_label):
    """
    Changes the volume label of the USB device (only if FAT32/vfat).
    Automatically selects first partition and validates filesystem.

    Args:
        device_path (str): Base device path (e.g., /dev/sdb)
        new_label (str): New volume label

    Returns:
        bool: True if label was changed successfully, False otherwise
    """
    part = get_first_partition(device_path)
    if not part:
        print("[!] No partition found to change label.")
        return False

    fs_type = get_partition_filesystem(part)
    if fs_type not in ["vfat", "fat32", "FAT32"]:
        print(f"[!] Filesystem of {part} is not FAT32/vfat (detected: {fs_type}).")
        return False

    try:
        validated_label = validator.expect_non_empty(new_label, prompt="[?] Label must not be empty. Re-enter: ")
        print(f"[*] Changing label of {part} to '{validated_label}'...")
        subprocess.run(["sudo", "mlabel", "-i", part, "::" + validated_label], check=True)
        return True
    except Exception as e:
        print(f"[!] Failed to change label: {e}")
        return False


def get_first_partition(device_path):
    try:
        output = subprocess.check_output(["lsblk", "-J", "-o", "NAME,TYPE"], text=True)
        data = json.loads(output)
        base = device_path.replace("/dev/", "")

        for d in data["blockdevices"]:
            if d["name"] == base and "children" in d:
                for child in d["children"]:
                    if child.get("type") == "part":
                        return "/dev/" + child["name"]
        return None
    except Exception as e:
        print(f"[!] Error getting partition: {e}")
        return None


def get_partition_filesystem(partition_path):
    try:
        output = subprocess.check_output(["lsblk", "-no", "FSTYPE", partition_path], text=True)
        fs_type = output.strip()
        return fs_type if fs_type else None
    except Exception as e:
        print(f"[!] Error detecting filesystem: {e}")
        return None


def get_device_size_bytes(device_path: str) -> int | None:
    try:
        output = subprocess.check_output(["lsblk", "-b", "-J", "-o", "NAME,SIZE"], text=True)
        data = json.loads(output)
        base = device_path.replace("/dev/", "")

        for d in data["blockdevices"]:
            if d["name"] == base:
                return int(d["size"])
    except Exception as e:
        print(f"[!] Error getting device size: {e}")
        return None
