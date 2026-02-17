from __future__ import annotations

from collections.abc import Callable

from app.calculation.factory import CalculationFactory
from app.calculation.history import CalculationHistory


def help_text(factory: CalculationFactory) -> str:
    ops = ", ".join(factory.supported)
    return (
        "Commands:\n"
        "  add | sub | mul | div  -> perform arithmetic\n"
        "  history                -> show session history\n"
        "  help                   -> show this help\n"
        "  exit                   -> quit\n\n"
        "Usage:\n"
        "  <op> <a> <b>\n"
        f"Supported ops: {ops}"
    )


def parse_numbers(a_str: str, b_str: str) -> tuple[float, float]:
    # EAFP: attempt conversion, catch failure
    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError as exc:
        raise ValueError("Inputs must be numbers.") from exc
    return a, b


def handle_line(
    line: str,
    factory: CalculationFactory,
    history: CalculationHistory,
) -> str | None:
    line = line.strip()
    if not line:
        return "Please enter a command. Type 'help' for options."

    cmd = line.lower()

    if cmd == "help":
        return help_text(factory)

    if cmd == "history":
        return "\n".join(history.format_lines())

    if cmd == "exit":
        return None

    parts = line.split()
    if len(parts) != 3:
        return "Invalid format. Use: <op> <a> <b> (example: add 2 3)"

    op_name, a_str, b_str = parts
    try:
        a, b = parse_numbers(a_str, b_str)
        calc = factory.create(op_name, a, b)
        result = calc.result()
        history.add(calc)
        return f"Result: {result}"
    except ZeroDivisionError as exc:
        return f"Error: {exc}"
    except ValueError as exc:
        return f"Error: {exc}"


def run_repl(
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> None:
    factory = CalculationFactory()
    history = CalculationHistory()

    output_func("Calculator REPL. Type 'help' for commands.")
    while True:
        line = input_func("> ")
        response = handle_line(line, factory, history)
        if response is None:
            output_func("Goodbye.")
            break
        output_func(response)
