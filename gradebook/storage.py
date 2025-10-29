from __future__ import annotations

import json
import os
from typing import Dict, Any, Tuple
from json import JSONDecodeError
import logging

DEFAULT_PATH = os.path.join("data", "gradebook.json")


def empty_db() -> Dict[str, Any]:
    """Return an empty gradebook structure."""
    return {"students": [], "courses": [], "enrollments": [], "meta": {"next_student_id": 1}}


def _normalize_db(data: Any) -> Dict[str, Any]:
    """
    Make sure the loaded object is a dict with required top-level keys.
    If shape is wrong, fall back to empty.
    """
    if not isinstance(data, dict):
        return empty_db()
    data.setdefault("students", [])
    data.setdefault("courses", [])
    data.setdefault("enrollments", [])
    data.setdefault("meta", {"next_student_id": 1})
    if not isinstance(data["meta"], dict):
        data["meta"] = {"next_student_id": 1}
    data["meta"].setdefault("next_student_id", 1)
    return data


def load_data(path: str = DEFAULT_PATH) -> Tuple[Dict[str, Any], str]:
    """
    Load gradebook data from JSON.
    - If file does not exist, return empty db.
    - If JSON is corrupted, print a helpful message and return empty db.
    - Any other unexpected error, print message and return empty db.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        data = _normalize_db(raw)
        logging.info("Loaded data from %s", path)
        return data, path

    except FileNotFoundError:
        logging.info("No existing data file at %s; starting with empty DB.", path)
        return empty_db(), path

    except JSONDecodeError as e:
        logging.error("Corrupted JSON at %s: %s", path, e)
        print(f"The data file '{path}' is corrupted or not valid JSON. Starting with an empty database.")
        return empty_db(), path

    except Exception as e:
        logging.error("Unexpected error loading %s: %s", path, e)
        print(f"Unexpected error loading data: {e}. Starting with an empty database.")
        return empty_db(), path


def save_data(db: Dict[str, Any], path: str = DEFAULT_PATH) -> None:
    """
    Save gradebook data to JSON, creating the parent directory if needed.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
        logging.info("Saved data to %s", path)
    except Exception as e:
        logging.error("Unexpected error saving %s: %s", path, e)
        print(f"Failed to save data to '{path}': {e}")