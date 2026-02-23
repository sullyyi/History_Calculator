from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from app.calculation.factory import CalculationFactory
from app.calculation.history import CalculationHistory, HistorySnapshot


@dataclass
class ReplSession:
    factory: CalculationFactory
    history: CalculationHistory
    history_path: Path
    undo_stack: list[HistorySnapshot]
    redo_stack: list[HistorySnapshot]


def help_text(factory: CalculationFactory) -> str:
    ops = ", ".join(factory.supported)
    return (
        "Commands:\n"
        "  add | sub | mul | div | pow | root  -> perform arithmetic\n"
        "  history                            -> show history\n"
        "  clear                              -> clear history\n"
        "  undo                               -> undo last change\n"
        "  redo                               -> redo last undone change\n"
        "  save                               -> save history to CSV\n"
        "  load                               -> load history from CSV\n"
        "  help                               -> show this help\n"
        "  exit                               -> quit\n\n"
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


def _record_undo_before_change(session: ReplSession) -> None:
    session.undo_stack.append(session.history.snapshot())
    session.redo_stack.clear()


def _do_undo(session: ReplSession) -> bool:
    if not session.undo_stack:
        return False
    session.redo_stack.append(session.history.snapshot())
    snap = session.undo_stack.pop()
    session.history.restore(snap)
    return True


def _do_redo(session: ReplSession) -> bool:
    if not session.redo_stack:
        return False
    session.undo_stack.append(session.history.snapshot())
    snap = session.redo_stack.pop()
    session.history.restore(snap)
    return True


def handle_line(line: str, session: ReplSession) -> str | None:
    line = line.strip()
    if not line:
        return "Please enter a command. Type 'help' for options."

    cmd = line.lower()

    if cmd == "help":
        return help_text(session.factory)

    if cmd == "history":
        return "\n".join(session.history.format_lines())

    if cmd == "clear":
        _record_undo_before_change(session)
        session.history.clear()
        return "History cleared."

    if cmd == "undo":
        if _do_undo(session):
            return "Undo successful."
        return "Nothing to undo."

    if cmd == "redo":
        if _do_redo(session):
            return "Redo successful."
        return "Nothing to redo."

    if cmd == "save":
        session.history.save(session.history_path)
        return f"History saved to: {session.history_path}"

    if cmd == "load":
        # LBYL: check file exists before attempting load (history.load is also LBYL)
        if not session.history_path.exists():
            return f"Error: History file not found: {session.history_path}"
        _record_undo_before_change(session)
        session.history.load(session.history_path)
        return f"History loaded from: {session.history_path}"

    if cmd == "exit":
        return None

    parts = line.split()
    if len(parts) != 3:
        return "Invalid format. Use: <op> <a> <b> (example: add 2 3)"

    op_name, a_str, b_str = parts
    try:
        a, b = parse_numbers(a_str, b_str)
        calc = session.factory.create(op_name, a, b)

        _record_undo_before_change(session)
        result = calc.result()
        session.history.add(calc)

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
    session = ReplSession(
        factory=CalculationFactory(),
        history=CalculationHistory(),
        history_path=Path(history_path),
        undo_stack=[],
        redo_stack=[],
    )

    output_func("Calculator REPL. Type 'help' for commands.")

    # auto-load on start if file exists (LBYL)
    if session.history_path.exists():
        try:
            session.history.load(session.history_path)
            output_func(f"Loaded history from: {session.history_path}")
        except Exception as exc:
            output_func(f"Warning: Failed to load history: {exc}")

    while True:
        line = input_func("> ")
        response = handle_line(line, session)
        if response is None:
            output_func("Goodbye.")
            break
        output_func(response)