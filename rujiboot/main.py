# File: main.py
# Main entry point for RujiBoot
# Handles startup logic: language selection, dependency check, GUI or CLI dispatch

import sys
import os

# Ensure program always runs from its own directory (fixes icon launcher issues)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from utils.system_check_util import check_required_tools
from utils.i18n_util import load_translations
from cli.cli_main import run_cli

if __name__ == "__main__":
    # --- Detect language flag ---
    lang = "en"
    for arg in sys.argv:
        if arg.startswith("--lang=es"):
            lang = "es"
        elif arg.startswith("--lang=pt"):
            lang = "pt"

    t = load_translations(lang)

    # --- Check required system tools ---
    check_required_tools(t)

    # --- Dispatch GUI or CLI ---
    if "--gui" in sys.argv:
        try:
            from gui.gui_main import run_gui
            run_gui()
        except ImportError:
            print(t.get("error_gui_missing", "Error: GUI dependencies are not available on this system."))
            print(t.get("error_gui_env", "Make sure you run GUI mode only on graphical environments."))
    else:
        run_cli()
