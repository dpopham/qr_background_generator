"""Environment-driven application settings."""

from __future__ import annotations

import os


def _bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int, minimum: int) -> int:
    try:
        value = int(os.getenv(name, str(default)))
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return value


HOST = os.getenv("QR_HOST", "127.0.0.1")
PORT = _int("QR_PORT", 5555, 1)
DEBUG = _bool("QR_DEBUG", False)

BACKGROUND_WIDTH = _int("QR_BACKGROUND_WIDTH", 1280, 1)
BACKGROUND_HEIGHT = _int("QR_BACKGROUND_HEIGHT", 720, 1)
BACKGROUND_COLOR = os.getenv("QR_BACKGROUND_COLOR", "white")
QR_SIZE = _int("QR_SIZE", 300, 1)
QR_LEFT = _int("QR_LEFT", 0, 0)
QR_TOP = _int("QR_TOP", 0, 0)
QR_BOX_SIZE = _int("QR_BOX_SIZE", 10, 1)
QR_BORDER = _int("QR_BORDER", 4, 4)
MAX_MESSAGE_LENGTH = _int("QR_MAX_MESSAGE_LENGTH", 2048, 1)
MAX_REQUEST_BYTES = _int("QR_MAX_REQUEST_BYTES", 16384, 1024)
