# Path: utils/checksum_util.py
# Description: Utility functions for calculating and verifying SHA256 checksums

import hashlib
import os
from utils.log_util import log_event

def calculate_sha256(file_path: str, t: dict) -> str | None:
    """
    Calculates SHA256 checksum of a given file.

    Args:
        file_path (str): Path to the file
        t (dict): Translation dictionary

    Returns:
        str | None: SHA256 hash, or None if error
    """
    if not os.path.isfile(file_path):
        print(t.get("file_not_found", "[!] File does not exist."))
        return None

    try:
        print(t.get("calculating_sha256", "[*] Calculating SHA256 hash (please wait)..."))
        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)

        hash_result = sha256_hash.hexdigest()
        print(t.get("calculated_sha256", "[+] SHA256:") + f" {hash_result}")
        log_event(f"SHA256_CALCULATED - {file_path} = {hash_result}")
        return hash_result

    except Exception as e:
        print(t.get("error_sha256", "[!] Error while calculating SHA256:"))
        print("    Details:", str(e))
        log_event(f"SHA256_ERROR - {file_path} - {e}")
        return None


def prompt_and_compare_sha256(file_path: str, t: dict) -> bool | None:
    """
    Prompts user to verify the file SHA256 hash.

    Args:
        file_path (str): Path to the ISO file
        t (dict): Translation dictionary

    Returns:
        bool | None:
            - True if SHA256 matched
            - False if mismatch or cancelled
            - None if verification skipped but user chose to continue
    """
    actual_hash = calculate_sha256(file_path, t)
    if not actual_hash:
        log_event(f"SHA256_ABORTED - {file_path} (could not calculate)")
        return False

    while True:
        verify = input(t.get("ask_verify_sha", "[?] Verify this SHA256 with the expected value? [y/n] ")).strip().lower()
        if verify in ["y", "n"]:
            break
        print(t.get("ask_valid_y_n", "[!] Please enter 'y' or 'n'."))

    if verify == "y":
        expected = input(t.get("ask_paste_sha", "[?] Paste expected SHA256: ")).strip()
        if actual_hash.lower() == expected.lower():
            print(t.get("sha_match", "[+] SHA256 match: VALID ISO"))
            log_event(f"SHA256_MATCH - {file_path}")
            return True
        else:
            print(t.get("sha_mismatch", "[!] SHA256 mismatch: ISO may be corrupt"))
            log_event(f"SHA256_MISMATCH - {file_path} - expected: {expected}")
            while True:
                proceed = input(t.get("ask_continue_anyway", "[?] Continue anyway? [y/n] ")).strip().lower()
                if proceed in ["y", "n"]:
                    break
                print(t.get("ask_valid_y_n", "[!] Please enter 'y' or 'n'."))
            if proceed == "y":
                print(t.get("warning_proceed_risk", "[!] Proceeding at your own risk."))
                log_event(f"SHA256_CONTINUE_FORCED - {file_path}")
                return None
            else:
                print(t.get("cancelled_by_user", "[*] Operation cancelled by user."))
                log_event(f"SHA256_VERIFICATION_CANCELLED - {file_path}")
                return False

    else:
        print(t.get("warn_no_verification", "[!] SHA256 verification skipped."))
        while True:
            proceed = input(t.get("ask_continue_anyway", "[?] Continue anyway? [y/n] ")).strip().lower()
            if proceed in ["y", "n"]:
                break
            print(t.get("ask_valid_y_n", "[!] Please enter 'y' or 'n'."))
        if proceed == "y":
            print(t.get("warning_proceed_risk", "[!] Proceeding at your own risk."))
            log_event(f"SHA256_SKIPPED_AND_CONTINUED - {file_path}")
            return None
        else:
            print(t.get("cancelled_by_user", "[*] Operation cancelled by user."))
            log_event(f"SHA256_SKIPPED_AND_CANCELLED - {file_path}")
            return False
