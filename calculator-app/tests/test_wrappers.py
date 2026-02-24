def test_wrappers_import():
    import app.calculation  # noqa: F401
    import app.history  # noqa: F401
    import app.operations  # noqa: F401
    import app.calculator_repl  # noqa: F401
    import app.calculator_memento  # noqa: F401