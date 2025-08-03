# Path: utils/simulate_util.py
# Description: Simulated write mode logic for RujiBoot CLI (used for dev/testing)

import time
import os
from utils.log_util import log_event

# Correct env variable for simulation
SIMULATION_MODE = os.getenv("RUJIBOOT_SIMULATE", "0") == "1"

def is_simulation_enabled() -> bool:
    """
    Returns True if simulate mode is active via RUJIBOOT_SIMULATE=1
    """
    return SIMULATION_MODE

def simulate_write_process(iso_path: str, device_path: str, t: dict) -> bool:
    """
    Simulates writing an ISO to a device.
    Shows a fake progress bar and logs the action.

    Args:
        iso_path (str): Path to ISO file
        device_path (str): Target USB device
        t (dict): Translations dictionary

    Returns:
        bool: Always returns True (simulated success)
    """
    print()
    print(t.get("simulated_write_title", "[SIMULATION MODE]"))
    print("[*] " + t.get("writing_start", "Starting ISO writing process..."))
    print("[*] " + t.get("writing_target", "Writing to device:") + f" {device_path}")
    print("[*] " + t.get("writing_source", "Using ISO file:") + f" {iso_path}")
    print("[*] " + t.get("writing_progress", "Writing progress:"))

    log_event(f"WRITE_SIMULATION_STARTED - ISO: {iso_path} TO: {device_path}")

    bar_len = 20
    for i in range(1, bar_len + 1):
        bar = "[" + "#" * i + " " * (bar_len - i) + "]"
        percent = i * 5
        print(f"\r{bar} {percent}%", end="", flush=True)
        time.sleep(0.2)

    print("\n[+] " + t.get("writing_done_simulated", "Dry-run complete. No data was written."))
    log_event(f"WRITE_SIMULATION_DONE - ISO: {iso_path} TO: {device_path}")

    return True

def warn_if_wrong_env_var(t: dict):
    """
    Shows a warning if SIMULATION_MODE=1 was set instead of RUJIBOOT_SIMULATE=1.
    Should be called from main CLI only if needed.
    """
    if os.getenv("SIMULATION_MODE") == "1" and not SIMULATION_MODE:
        print(t.get("warn_wrong_env_var", "[!] Warning: SIMULATION_MODE=1 has no effect."))
        print(t.get("warn_use_correct_env", "[*] Use RUJIBOOT_SIMULATE=1 to activate simulation mode."))
