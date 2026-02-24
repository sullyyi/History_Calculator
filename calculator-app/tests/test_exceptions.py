import pytest

from app.exceptions import (
    CalculatorError,
    ConfigurationError,
    UnknownOperationError,
    ValidationError,
)


def test_exceptions_are_raised_and_catchable():
    with pytest.raises(CalculatorError):
        raise CalculatorError("base")

    with pytest.raises(CalculatorError):
        raise ConfigurationError("config")

    with pytest.raises(CalculatorError):
        raise ValidationError("validation")

    with pytest.raises(CalculatorError):
        raise UnknownOperationError("unknown op")