from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from app.calculator.facade import Calculator


def parse_numbers(a_str: str, b_str: str) -> tuple[float, float]:
    # EAFP: attempt conversion, catch failure
    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError as exc:
        raise ValueError("Inputs must be numbers.") from exc
    return a, b


def handle_line(line: str, calc: Calculator) -> str | None:
    line = line.strip()
    if not line:
        return "Please enter a command. Type 'help' for options."

    cmd = line.lower()

    if cmd == "help":
        return calc.help_text()

    if cmd == "history":
        return "\n".join(calc.history_lines())

    if cmd == "clear":
        calc.clear()
        return "History cleared."

    if cmd == "undo":
        if calc.undo():
            return "Undo successful."
        return "Nothing to undo."

    if cmd == "redo":
        if calc.redo():
            return "Redo successful."
        return "Nothing to redo."

    if cmd == "save":
        calc.save()
        return f"History saved to: {calc.history_path}"

    if cmd == "load":
        try:
            calc.load()
            return f"History loaded from: {calc.history_path}"
        except FileNotFoundError as exc:
            return f"Error: {exc}"

    if cmd == "exit":
        return None

    parts = line.split()
    if len(parts) != 3:
        return "Invalid format. Use: <op> <a> <b> (example: add 2 3)"

    op_name, a_str, b_str = parts
    try:
        a, b = parse_numbers(a_str, b_str)
        result = calc.execute(op_name, a, b)
        return f"Result: {result}"
    except ZeroDivisionError as exc:
        return f"Error: {exc}"
    except ValueError as exc:
        return f"Error: {exc}"


def run_repl(
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
    history_path: str | Path = "history.csv",
) -> None:
    calc = Calculator.create_default(history_path=history_path)

    output_func("Calculator REPL. Type 'help' for commands.")

    # Optional auto-load; keep it small and predictable
    try:
        if calc.auto_load_if_exists():
            output_func(f"Loaded history from: {calc.history_path}")
    except Exception as exc:
        output_func(f"Warning: Failed to load history: {exc}")

    while True:
        line = input_func("> ")
        response = handle_line(line, calc)
        if response is None:
            output_func("Goodbye.")
            break
        output_func(response)