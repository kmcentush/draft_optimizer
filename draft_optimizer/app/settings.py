import json
import os
from typing import Any, Dict, List

# Specify settings directory
SETTINGS_DIR = os.path.abspath(os.path.join(__file__, "..", "..", "..", "settings"))


def list_settings() -> List[str]:
    files = os.listdir(SETTINGS_DIR)
    files = [f for f in files if f.endswith(".json")]
    return files


def load_settings(settings_file: str) -> Dict[str, Any]:
    settings_file = os.path.join(SETTINGS_DIR, settings_file)
    with open(settings_file, "r", encoding="utf-8") as f:
        out = json.load(f)

    return out


def save_settings(settings_file, settings: Dict[str, Any]):
    settings_file = os.path.join(SETTINGS_DIR, settings_file)
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)
