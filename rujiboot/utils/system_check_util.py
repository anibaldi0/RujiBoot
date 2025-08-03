# path: utils/system_check_util.py
# Description: Validates presence of required system tools before running RujiBoot

import shutil
import sys

# Critical tools for writing, partitioning, formatting and encryption
REQUIRED_TOOLS = [
    "dd",
    "parted",
    "lsblk",
    "mkfs.vfat",
    "mlabel",
    "cryptsetup",
    "udisksctl"
]

# Optional tools that may enhance UX or fallback gracefully
OPTIONAL_TOOLS = [
    "fatlabel",
    "mount",
    "umount"
]

def check_required_tools(t: dict = None) -> bool:
    """
    Checks if all required system tools are available.

    Args:
        t (dict): Optional translation dictionary

    Returns:
        bool: True if all required tools are found, False otherwise
    """
    all_ok = True
    print()
    print("[*] Checking system tools...\n")

    # Check required tools
    for tool in REQUIRED_TOOLS:
        path = shutil.which(tool)
        if path is None:
            msg = t.get("missing_tool", "[!] Required system tool is missing: {tool}") if t else "[!] Missing: {tool}"
            print(msg.replace("{tool}", tool))
            all_ok = False
        else:
            print(f"[+] Found: {tool} -> {path}")

    # Check optional tools
    for tool in OPTIONAL_TOOLS:
        path = shutil.which(tool)
        if path is None:
            msg = t.get("missing_optional_tool", "[!] Optional tool missing: {tool} (some features may be unavailable)") \
                if t else "[!] Optional missing: {tool}"
            print(msg.replace("{tool}", tool))
        else:
            print(f"[+] Optional: {tool} -> {path}")

    # Abort if required tools are missing
    if not all_ok:
        print()
        if t:
            print(t.get("press_enter_exit", "Press Enter to exit."))
        else:
            print("Press Enter to exit.")
        input()
        sys.exit(1)

    print("\n[*] All required tools are available.\n")
    return True
