from __future__ import annotations

from app.exceptions import ValidationError


def parse_two_numbers(a_str: str, b_str: str) -> tuple[float, float]:
    # EAFP: attempt conversion, catch failure
    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError as exc:
        raise ValidationError("Inputs must be numbers.") from exc
    return a, b


def split_command(line: str) -> list[str]:
    return line.strip().split()