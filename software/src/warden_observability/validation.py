"""Strict scalar validation shared by the supported JSON formats."""

from __future__ import annotations

import math
from typing import Any


def object_value(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be an object")
    return value


def integer(value: dict[str, Any], field: str) -> int:
    result = value[field]
    if not isinstance(result, int) or isinstance(result, bool):
        raise TypeError(f"{field} must be an integer")
    return result


def number(value: dict[str, Any], field: str) -> float:
    result = value[field]
    if not isinstance(result, (int, float)) or isinstance(result, bool):
        raise TypeError(f"{field} must be numeric")
    try:
        converted = float(result)
    except OverflowError as exc:
        raise ValueError(f"{field} must be finite") from exc
    if not math.isfinite(converted):
        raise ValueError(f"{field} must be finite")
    return converted


def boolean(value: dict[str, Any], field: str) -> bool:
    result = value[field]
    if not isinstance(result, bool):
        raise TypeError(f"{field} must be boolean")
    return result


def text(value: dict[str, Any], field: str) -> str:
    result = value[field]
    if not isinstance(result, str) or not result.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return result


def records(value: dict[str, Any], field: str) -> list[dict[str, Any]]:
    result = value[field]
    if not isinstance(result, list):
        raise TypeError(f"{field} must be an array")
    return [object_value(item, field) for item in result]
