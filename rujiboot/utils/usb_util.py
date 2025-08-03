# path: utils/usb_util.py
# Description: Utilities for USB validation and info display

# === Validations ===

SUSPICIOUS_LABELS = {"EFI", "SYSTEM", "RECOVERY", "WINDOWS", "BOOT", "RESCUE"}

def is_usb_large_enough(usb_device: dict, min_size_bytes: int = 2 * 1024 * 1024 * 1024) -> bool:
    """
    Checks if the USB device meets the minimum size requirement.

    Args:
        usb_device (dict): USB device dictionary.
        min_size_bytes (int): Minimum required size in bytes.

    Returns:
        bool: True if size is equal or greater, False otherwise.
    """
    size_str = usb_device.get("size_bytes")
    try:
        size_int = int(size_str)
        return size_int >= min_size_bytes
    except (ValueError, TypeError):
        return False

def is_suspicious_label(label: str) -> bool:
    """
    Checks if a USB label is considered critical or system-reserved.

    Args:
        label (str): USB label.

    Returns:
        bool: True if label is suspicious.
    """
    if not label:
        return False
    return label.strip().upper() in SUSPICIOUS_LABELS

# === Printer ===

def print_selected_usb_info(selected_usb: dict, t: dict):
    """
    Prints formatted information about a selected USB device.

    Args:
        selected_usb (dict): Dictionary with USB device details.
        t (dict): Translation dictionary
    """
    if not selected_usb:
        return

    print(t.get("usb_info_label", "[*] Selected USB device:"))

    label = selected_usb.get("label") or "-"
    size = selected_usb.get("size") or "?"
    model = selected_usb.get("model") or "?"
    device = selected_usb.get("device") or "?"

    print(f"  {device} - {size} - {model} - Label: {label}")
    print()

def print_usb_header(usb: dict, t: dict):
    """
    Prints a persistent header with the selected USB device.
    Should be placed just below the program title.
    """
    if not usb:
        return
    label = usb.get("label") or t.get("no_label", "no label")
    model = usb.get("model", "")
    size = usb.get("size", "")
    dev_path = usb.get("device", "?")

    device_str = f"{dev_path} - {size} - {model}"
    print(t.get("selected_usb_header", "[USB Selected] ") + f"{device_str} - Label: {label}")
