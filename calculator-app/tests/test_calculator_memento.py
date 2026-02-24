from app.calculator_memento import MementoCaretaker
from app.calculation.history import CalculationHistory
from app.calculation.factory import CalculationFactory


def test_memento_caretaker_methods():
    caretaker = MementoCaretaker()

    assert caretaker.can_undo() is False
    assert caretaker.can_redo() is False

    # Create a real snapshot to put in the stacks
    history = CalculationHistory()
    factory = CalculationFactory()
    history.add(factory.create("add", 1, 2))
    snap = history.snapshot()

    caretaker.undo_stack.append(snap)
    assert caretaker.can_undo() is True

    caretaker.redo_stack.append(snap)
    assert caretaker.can_redo() is True

    caretaker.clear_redo()
    assert caretaker.can_redo() is False