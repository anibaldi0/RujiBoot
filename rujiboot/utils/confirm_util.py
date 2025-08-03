# Path: utils/confirm_util.py
# Description: Utility function to confirm dangerous actions with double-confirmation

import getpass
from utils.log_util import log_event

def confirm_action(t, message_key=None, require_double=False):
    """
    Confirms an action with the user, optionally with double confirmation ('ERASE').

    Args:
        t (dict): Translation dictionary
        message_key (str): Optional key to show specific warning
        require_double (bool): If True, requires 'ERASE' to proceed

    Returns:
        bool: True if confirmed, False if cancelled
    """
    if message_key:
        print(t.get(message_key, "[!] This operation may erase data."))

    print(t.get("confirm_warning", "[!] WARNING: This action may erase data."))

    # Primera confirmación: [y/N] o 'exit'
    while True:
        confirm = input(t.get("confirm_question", "[?] Are you sure? [y/N] ") + " ").strip().lower()
        if confirm == "y":
            break
        elif confirm == "exit":
            print(t.get("confirm_cancelled", "[*] Action cancelled."))
            log_event("ACTION_CANCELLED_AT_FIRST_CONFIRM")
            return False
        else:
            print(t.get("ask_valid_y_n", "[!] Please enter 'y' or 'n'."))

    # Segunda confirmación: 'ERASE' (case-sensitive) o 'exit'
    if require_double:
        while True:
            double = input(t.get("confirm_double_prompt", "[?] Type 'ERASE' to confirm: ") + " ").strip()
            if double == "ERASE":
                log_event("ACTION_CONFIRMED_FULLY")
                return True
            elif double.lower() == "exit":
                print(t.get("confirm_cancelled", "[*] Action cancelled."))
                log_event("ACTION_CANCELLED_AT_SECOND_CONFIRM")
                return False
            else:
                print(t.get("invalid_final_confirm", "[!] Invalid confirmation. Please type 'ERASE' or 'exit'."))

    # Confirmación simple aceptada
    log_event("ACTION_CONFIRMED_BASIC")
    return True


def prompt_password_optional(t: dict) -> str | None:
    """
    Prompts for a password to use for encrypted persistence.

    Returns:
        str or None
    """
    password = getpass.getpass(t.get("ask_password", "[?] Enter a password (or leave blank to skip): ")).strip()
    if password:
        return password
    print(t.get("password_skipped_warning", "[*] Password skipped. Persistence will not be encrypted."))
    return None
