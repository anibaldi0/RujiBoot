# path: utils/header_util.py
# Description: Title utilities for CLI menus (color only here, no translation)

from utils import log_util
from utils.simulate_util import is_simulation_enabled
from utils.constants_util import FG_CYAN, RESET, FG_YELLOW

def show_program_title() -> str:
    """
    Returns only the base program title with cyan color.
    """
    return f"{FG_CYAN}=== RujiBoot ==={RESET}"

def print_program_title_and_help():
    """
    Prints the program title with a help label (yellow).
    """
    print(f"{show_program_title()} [{FG_YELLOW}Help{RESET}]")

def print_program_title_and_mode():
    """
    Prints the program title along with the current mode (logs / anonymous),
    and shows SIMULATION_MODE warning if active.
    """
    print()
    mode_text = "Anonymous mode (no logs)" if log_util.ANONYMOUS_MODE else "Auditoria mode (persistent logs)"
    print(f"{show_program_title()} [{FG_YELLOW}{mode_text}{RESET}]")

    if is_simulation_enabled():
        print(f"{FG_YELLOW}[SIMULATION MODE ACTIVE - NO DISK WRITING]{RESET}")
        if not log_util.ANONYMOUS_MODE:
            log_util.log_event("SIMULATION_MODE_ACTIVE")
    print()
