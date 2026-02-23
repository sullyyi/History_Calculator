from pathlib import Path

from app.calculation.factory import CalculationFactory
from app.calculation.history import CalculationHistory
from app.calculator.cli import ReplSession, handle_line, run_repl


def make_session(tmp_path: Path) -> ReplSession:
    return ReplSession(
        factory=CalculationFactory(),
        history=CalculationHistory(),
        history_path=tmp_path / "history.csv",
        undo_stack=[],
        redo_stack=[],
    )


def test_handle_line_blank(tmp_path: Path):
    session = make_session(tmp_path)
    out = handle_line("", session)
    assert "Please enter a command" in out


def test_handle_line_help_contains_supported_ops(tmp_path: Path):
    session = make_session(tmp_path)
    out = handle_line("help", session)
    assert "Supported ops" in out
    assert "add" in out
    assert "pow" in out
    assert "root" in out


def test_handle_line_bad_format(tmp_path: Path):
    session = make_session(tmp_path)
    out = handle_line("add 1", session)
    assert "Invalid format" in out


def test_handle_line_non_numeric(tmp_path: Path):
    session = make_session(tmp_path)
    out = handle_line("add a 2", session)
    assert "Error:" in out
    assert "Inputs must be numbers" in out


def test_handle_line_unknown_operation(tmp_path: Path):
    session = make_session(tmp_path)
    out = handle_line("nope 2 3", session)
    assert "Unsupported operation" in out


def test_handle_line_div_by_zero(tmp_path: Path):
    session = make_session(tmp_path)
    out = handle_line("div 1 0", session)
    assert "Cannot divide by zero" in out


def test_handle_line_success_adds_history(tmp_path: Path):
    session = make_session(tmp_path)
    out = handle_line("add 2 3", session)
    assert out == "Result: 5.0"
    assert len(session.history.all()) == 1


def test_handle_line_history_after_calc(tmp_path: Path):
    session = make_session(tmp_path)
    handle_line("mul 2 4", session)
    out = handle_line("history", session)
    assert "mul" in out
    assert "= 8.0" in out


def test_handle_line_clear_undo_redo(tmp_path: Path):
    session = make_session(tmp_path)

    handle_line("add 2 3", session)
    handle_line("mul 2 4", session)
    assert len(session.history.all()) == 2

    out = handle_line("clear", session)
    assert "History cleared" in out
    assert len(session.history.all()) == 0

    out = handle_line("undo", session)
    assert "Undo successful" in out
    assert len(session.history.all()) == 2

    out = handle_line("redo", session)
    assert "Redo successful" in out
    assert len(session.history.all()) == 0


def test_handle_line_undo_redo_nothing(tmp_path: Path):
    session = make_session(tmp_path)

    out = handle_line("undo", session)
    assert "Nothing to undo" in out

    out = handle_line("redo", session)
    assert "Nothing to redo" in out


def test_handle_line_save_and_load(tmp_path: Path):
    session = make_session(tmp_path)

    handle_line("add 2 3", session)
    handle_line("pow 2 3", session)
    assert len(session.history.all()) == 2

    out = handle_line("save", session)
    assert "History saved to:" in out
    assert session.history_path.exists()

    out = handle_line("clear", session)
    assert "History cleared" in out
    assert len(session.history.all()) == 0

    out = handle_line("load", session)
    assert "History loaded from:" in out
    assert len(session.history.all()) == 2

    text = "\n".join(session.history.format_lines())
    assert "add" in text
    assert "pow" in text


def test_handle_line_load_missing_file(tmp_path: Path):
    session = make_session(tmp_path)

    out = handle_line("load", session)
    assert "Error: History file not found" in out


def test_run_repl_end_to_end(tmp_path: Path):
    inputs = iter(["help", "add 1 2", "history", "exit"])
    outputs: list[str] = []

    def fake_input(prompt: str) -> str:
        return next(inputs)

    def fake_output(msg: str) -> None:
        outputs.append(msg)

    run_repl(
        input_func=fake_input,
        output_func=fake_output,
        history_path=tmp_path / "history.csv",
    )

    assert any("Calculator REPL" in s for s in outputs)
    assert any("Supported ops" in s for s in outputs)
    assert any("Result: 3.0" in s for s in outputs)
    assert any("Goodbye." in s for s in outputs)