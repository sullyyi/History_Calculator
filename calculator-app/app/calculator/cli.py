from __future__ import annotations
from app.exceptions import ValidationError
from collections.abc import Callable
from pathlib import Path

from app.calculator.facade import Calculator
from app.calculator_config import load_config
from app.exceptions import ConfigurationError
from app.input_validators import parse_two_numbers


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
        a, b = parse_two_numbers(a_str, b_str)
        result = calc.execute(op_name, a, b)
        return f"Result: {result}"
    except ZeroDivisionError as exc:
        return f"Error: {exc}"
    except ValidationError as exc:
        return f"Error: {exc}"
    except ValueError as exc:
        return f"Error: {exc}"


def run_repl(
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
    history_path: str | Path | None = None,
) -> None:
    # Load dotenv/env configuration (graceful failure)
    try:
        cfg = load_config()
    except ConfigurationError as exc:
        output_func(f"Configuration error: {exc}")
        return

    # CLI arg overrides env config if provided
    path = Path(history_path) if history_path is not None else cfg.history_path

    calc = Calculator.create_default(
        history_path=path,
        auto_save=cfg.auto_save,
        auto_load=False,  # we'll do controlled auto-load below
    )

    output_func("Calculator REPL. Type 'help' for commands.")

    # Auto-load if enabled (Approach A keeps autosave optional)
    if cfg.auto_load:
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