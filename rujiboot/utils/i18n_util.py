# path: utils/i18n_util.py
# Description: Utility for loading localized language strings from JSON files (no alias support)

import json
import os
from pathlib import Path
from typing import Dict, Optional

FALLBACK_LANG = "en"

def _candidate_lang_dirs() -> list[Path]:
    """
    Return a list of possible directories where data/lang could live,
    ordered by priority.
    """
    candidates: list[Path] = []

    # 1) Explicit override by env var
    env_dir = os.getenv("RUJIBOOT_LANG_DIR")
    if env_dir:
        candidates.append(Path(env_dir).expanduser().resolve())

    # 2) Repo/dev layout: <project_root>/data/lang
    utils_dir = Path(__file__).resolve().parent
    project_root = utils_dir.parent
    candidates.append(project_root / "data" / "lang")

    # 3) Current working directory
    candidates.append(Path.cwd() / "data" / "lang")

    # 4) Debian installed path
    candidates.append(Path("/opt/rujiboot/data/lang"))

    # Remove duplicates
    seen = set()
    unique_candidates = []
    for c in candidates:
        if c not in seen:
            unique_candidates.append(c)
            seen.add(c)
    return unique_candidates

def _load_json(path: Path) -> Optional[Dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def load_translations(language_code: str) -> Dict[str, str]:
    """
    Loads translation strings from a JSON file based on the selected language.
    No alias resolution. Only plain keys are supported.

    Order of resolution:
      1) RUJIBOOT_LANG_DIR/<lang>.json
      2) <repo_root>/data/lang/<lang>.json
      3) cwd/data/lang/<lang>.json
      4) /opt/rujiboot/data/lang/<lang>.json
      5) fallback to en.json
      6) {} if nothing found
    """
    wanted = f"{language_code}.json"
    fallback = f"{FALLBACK_LANG}.json"
    debug = os.getenv("RUJIBOOT_DEBUG_PATHS") == "1"

    for lang_dir in _candidate_lang_dirs():
        if debug:
            print(f"[DEBUG] Trying lang dir: {lang_dir}")
        if not lang_dir.is_dir():
            continue

        candidate = lang_dir / wanted
        data = _load_json(candidate)
        if data is not None:
            if debug:
                print(f"[DEBUG] Loaded {candidate}")
            return data

        candidate = lang_dir / fallback
        data = _load_json(candidate)
        if data is not None:
            if debug:
                print(f"[DEBUG] Fallback loaded {candidate}")
            return data

    if debug:
        print("[DEBUG] No translation file found. Returning empty dict.")
    return {}
