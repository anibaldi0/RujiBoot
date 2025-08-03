# path: utils/color_strings_util.py
# ANSI color wrapper without alias resolution (direct string lookup only)

import json
from pathlib import Path

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
        self.reset = "\033[0m"

    def get(self, key: str, fallback: str = None) -> str:
        """
        Return the colored string from key.
        If not found, return fallback in white if provided.
        """
        value = self.strings.get(key, None)
        if value is None:
            if fallback:
                return f"{WHITE.color}{fallback}{WHITE.reset}"
            else:
                return f"{self.color}[?? {key}]{self.reset}"
        return f"{self.color}{value}{self.reset}"

    def __getitem__(self, key: str) -> str:
        return self.get(key)

# === ANSI color instances ===
BLACK   = ColorStrings("\033[30m")  # usually avoided
RED     = ColorStrings("\033[31m")  # errors
GREEN   = ColorStrings("\033[32m")  # success
YELLOW  = ColorStrings("\033[33m")  # warnings
BLUE    = ColorStrings("\033[34m")  # headings
MAGENTA = ColorStrings("\033[35m")  # custom use
CYAN    = ColorStrings("\033[36m")  # custom use
WHITE   = ColorStrings("\033[37m")  # neutral/default
