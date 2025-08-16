# path: utils/color_strings_util.py
# Description: ANSI color wrapper with string lookup for translations

import json
from pathlib import Path
from utils import constants_util as c

class ColorStrings:
    def __init__(self, color_code: str, strings_file: str = "data/lang/es.json"):
        """
        Load strings from JSON file and store ANSI color code.
        """
        strings_path = Path(strings_file)
        if not strings_path.is_file():
            raise FileNotFoundError(f"Translation file not found: {strings_file}")
        with open(strings_path, "r", encoding="utf-8") as f:
            self.strings = json.load(f)
        self.color = color_code
        self.reset = c.RESET

    def get(self, key: str, fallback: str = None) -> str:
        """
        Return the colored string from key.
        If not found, return fallback in white if provided.
        """
        value = self.strings.get(key, None)
        if value is None:
            if fallback:
                return f"{FG_WHITE}{fallback}{c.RESET}"
            else:
                return f"{self.color}[?? {key}]{self.reset}"
        return f"{self.color}{value}{self.reset}"

    def __getitem__(self, key: str) -> str:
        return self.get(key)

# === Predefined color instances ===
BLACK   = ColorStrings(c.FG_BLACK)
RED     = ColorStrings(c.FG_RED)
GREEN   = ColorStrings(c.FG_GREEN)
YELLOW  = ColorStrings(c.FG_YELLOW)
BLUE    = ColorStrings(c.FG_BLUE)
MAGENTA = ColorStrings(c.FG_MAGENTA)
CYAN    = ColorStrings(c.FG_CYAN)
WHITE   = ColorStrings(c.FG_WHITE)

# Fallback for get() inside class
FG_WHITE = c.FG_WHITE
