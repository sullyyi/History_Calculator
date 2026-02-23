from app.calculation.factory import CalculationFactory
from app.calculation.history import CalculationHistory
from app.calculator.cli import handle_line, run_repl


def test_handle_line_blank():
    factory = CalculationFactory()
    history = CalculationHistory()
    out = handle_line("", factory, history)
    assert "Please enter a command" in out


def test_handle_line_help_contains_supported_ops():
    factory = CalculationFactory()
    history = CalculationHistory()
    out = handle_line("help", factory, history)
    assert "Supported ops" in out
    assert "add" in out
    assert "pow" in out
    assert "root" in out


def test_handle_line_bad_format():
    factory = CalculationFactory()
    history = CalculationHistory()
    out = handle_line("add 1", factory, history)
    assert "Invalid format" in out


def test_handle_line_non_numeric():
    factory = CalculationFactory()
    history = CalculationHistory()
    out = handle_line("add a 2", factory, history)
    assert "Error:" in out
    assert "Inputs must be numbers" in out


def test_handle_line_unknown_operation():
    factory = CalculationFactory()
    history = CalculationHistory()
    out = handle_line("nope 2 3", factory, history)
    assert "Unsupported operation" in out


def test_handle_line_div_by_zero():
    factory = CalculationFactory()
    history = CalculationHistory()
    out = handle_line("div 1 0", factory, history)
    assert "Cannot divide by zero" in out


def test_handle_line_success_adds_history():
    factory = CalculationFactory()
    history = CalculationHistory()
    out = handle_line("add 2 3", factory, history)
    assert out == "Result: 5.0"
    assert len(history.all()) == 1


def test_handle_line_pow_success_adds_history():
    factory = CalculationFactory()
    history = CalculationHistory()
    out = handle_line("pow 2 3", factory, history)
    assert out == "Result: 8.0"
    assert len(history.all()) == 1


def test_handle_line_root_success_adds_history():
    factory = CalculationFactory()
    history = CalculationHistory()
    out = handle_line("root 9 2", factory, history)
    assert out == "Result: 3.0"
    assert len(history.all()) == 1


def test_handle_line_history_after_calc():
    factory = CalculationFactory()
    history = CalculationHistory()
    handle_line("mul 2 4", factory, history)
    out = handle_line("history", factory, history)
    assert "mul" in out
    assert "= 8.0" in out


def test_run_repl_end_to_end():
    inputs = iter(["help", "add 1 2", "history", "exit"])
    outputs: list[str] = []

    def fake_input(prompt: str) -> str:
        return next(inputs)

    def fake_output(msg: str) -> None:
        outputs.append(msg)

    run_repl(input_func=fake_input, output_func=fake_output)

    assert any("Calculator REPL" in s for s in outputs)
    assert any("Supported ops" in s for s in outputs)
    assert any("Result: 3.0" in s for s in outputs)
    assert any("Goodbye." in s for s in outputs)