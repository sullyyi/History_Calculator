class CalculatorError(Exception):
    """Base exception for calculator app."""


class ConfigurationError(CalculatorError):
    """Raised when configuration is missing or invalid."""


class ValidationError(CalculatorError):
    """Raised when user input is invalid."""


class UnknownOperationError(CalculatorError):
    """Raised when a requested operation is unsupported."""