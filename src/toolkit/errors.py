class ToolkitError(Exception):
    """Base class for all toolkit errors."""

    pass


class InvalidValueError(ToolkitError):
    """Raised when an invalid value is provided."""

    def __init__(self, value: float, message: str = "Invalid value provided."):
        self.value = value
        super().__init__(f"{message} Value: {value}")


class CalculatorError(ToolkitError):
    """Raised when an error occurs in the calculator module."""

    pass


class ConverterError(ToolkitError):
    """Raised when an error occurs in the converter module."""

    pass


class EmptyExpressionError(CalculatorError):
    """Raised when an empty expression is provided to the calculator."""

    def __init__(self, message: str = "You cannot pass an empty value."):
        super().__init__(message)


class InvalidCharacterError(CalculatorError):
    """Raised when an invalid character is found in the expression."""

    def __init__(self, character: str, message: str = "Invalid character in expression."):
        self.character = character
        super().__init__(f"{message} Character: {character}")


class ConsecutiveOperatorsError(CalculatorError):
    """Raised when consecutive operators are found in the expression."""

    def __init__(
        self,
        operator1: str | float,
        operator2: str | float,
        message: str = "Consecutive operators were detected in the expression.",
    ):
        self.operator1 = operator1
        self.operator2 = operator2
        super().__init__(f"{message} {operator1}{operator2}")

    pass


class MissingOperandError(CalculatorError):
    """Raised when an operand is missing in the expression."""

    def __init__(self, operator: str | float, message: str = "The expression is missing an operand."):
        self.operator = operator
        super().__init__(f"{message} {operator}")


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero is attempted in the calculator."""

    pass


class UnbalancedParenthesesError(CalculatorError):
    """Raised when parentheses are unbalanced or mismatched."""

    def __init__(self, message: str = "Unbalanced parentheses in expression."):
        super().__init__(message)


class UnknownUnitError(ConverterError):
    """Raised when an unknown unit is provided to the converter."""

    def __init__(self, unit: str, message: str = "Unknown unit provided."):
        self.unit = unit
        super().__init__(f"{message} Unit: {unit}")


class IncompatibleUnitsError(ConverterError):
    """Raised when incompatible units are provided to the converter. kg and m are incompatible, for example."""

    def __init__(self, unit1: str, unit2: str, message: str = "Incompatible units provided."):
        self.unit1 = unit1
        self.unit2 = unit2
        super().__init__(f"{message} {unit1} and {unit2} are incompatible.")


class BelowAbsoluteZeroError(ConverterError):
    """Raised when a temperature below absolute zero is provided to the converter."""

    def __init__(self, message: str = "Temperature cannot be below absolute zero."):
        super().__init__(message)
