# Path: core/prepare_persistence_core.py
# Description: High-level logic for preparing persistent USB, modular and robust

import os
from utils.log_util import log_event
from core.usb_manager import get_device_size_bytes
from core.persistence_with_encryption_core import prepare_persistence_encrypted
from core.persistence_without_encryption_core import prepare_persistence_plain

# Space constants in MB
ISO_BUFFER_MB = 1024            # 1 GiB de margen por seguridad
SWAP_MB = 1024                  # Tamaño fijo de swap: 1 GiB
PERSISTENCE_MIN_MB = 2048      # Tamaño mínimo recomendado para persistencia: 2 GiB

def prepare_persistent_usb(device_path: str, iso_path: str, t: dict, password: str | None = None) -> bool:
    """
    Prepares a USB with encrypted or plain persistence depending on the password.

    Args:
        device_path (str): e.g. /dev/sdb
        iso_path (str): Path to ISO file
        t (dict): Translation dictionary
        password (str | None): If present, encrypted persistence is used

    Returns:
        bool: True if success, False otherwise
    """
    if not device_path.startswith("/dev/sd") or len(device_path) < 8:
        print(f"[!] {t.get('invalid_device', 'Invalid or dangerous device path')}: {device_path}")
        return False

    if not os.path.isfile(iso_path):
        print(f"[!] {t.get('invalid_iso_path', 'Invalid ISO path or file does not exist')}: {iso_path}")
        return False

    usb_size = get_device_size_bytes(device_path)
    if not usb_size:
        print(f"[!] {t.get('device_size_error', 'Could not determine device size')}")
        return False

    iso_size = os.path.getsize(iso_path)

    # Build required space dynamically
    required_bytes = iso_size + (ISO_BUFFER_MB * 1024**2)

    # Add SWAP and persistence if persistence is enabled
    wants_persistence = True
    wants_swap = True  # siempre usamos swap

    if wants_swap:
        required_bytes += SWAP_MB * 1024**2
    if wants_persistence:
        required_bytes += PERSISTENCE_MIN_MB * 1024**2

    if usb_size < required_bytes:
        print("[!] " + t.get("usb_too_small", "USB is too small for selected options."))
        print(f"[*] ISO size: {iso_size / (1024**2):.1f} MiB")
        print(f"[*] Required space: {required_bytes / (1024**2):.1f} MiB")
        print(f"[*] USB size: {usb_size / (1024**2):.1f} MiB")
        return False

    log_event(f"PERSISTENCE_REQUEST - Device: {device_path} | Encrypted: {bool(password)}")

    if password:
        return prepare_persistence_encrypted(device_path, iso_path, t, password)
    else:
        return prepare_persistence_plain(device_path, iso_path, t)
