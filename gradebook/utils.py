import logging
from typing import Any

def configure_logging():
    logger = logging.getLogger()
    if logger.handlers:
        return
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("logs/app.log", encoding="utf-8")
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

def parse_grade(value: Any) -> int:
    """Parse and validate a grade 0..100, returning an int. Raises ValueError on invalid input."""
    try:
        ivalue = int(value)
    except Exception:
        raise ValueError("grade must be an integer.")
    if ivalue < 0 or ivalue > 100:
        raise ValueError("grade must be between 0 and 100.")
    return ivalue
