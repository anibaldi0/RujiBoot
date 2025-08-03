# File: utils/iso_validate_util.py
# Utility functions to validate ISO file paths

import os

def validate_iso_path(path: str, t=None) -> str | None:
    """
    Validates if the given path is a valid .iso file.

    Args:
        path (str): File path to validate
        t (dict or None): Optional translations dictionary

    Returns:
        str | None: Valid absolute path if valid, None otherwise
    """
    abs_path = os.path.abspath(os.path.expanduser(path))

    if not os.path.isfile(abs_path):
        if t:
            print("[!] " + t.get("invalid_iso_path", "Invalid ISO path or file does not exist."))
        else:
            print("[!] File not found.")
        return None

    if not abs_path.lower().endswith(".iso"):
        if t:
            print("[!] " + t.get("invalid_iso_path", "Invalid ISO path or file does not exist."))
        else:
            print("[!] File does not have .iso extension.")
        return None

    if t:
        print("[+] " + t.get("valid_iso_selected", "Valid ISO selected:") + f" {abs_path}")
    else:
        print("[+] ISO file validated.")
    return abs_path
