"""Unit tests for the calculator module."""

from decimal import Decimal

import pytest

from toolkit.calculator import calculate
from toolkit.errors import ConsecutiveOperatorsError
from toolkit.errors import DivisionByZeroError
from toolkit.errors import EmptyExpressionError
from toolkit.errors import InvalidCharacterError
from toolkit.errors import MissingOperandError
from toolkit.errors import UnbalancedParenthesesError


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("2 + 2", Decimal("4")),
        ("10 - 3", Decimal("7")),
        ("4 * 2.5", Decimal("10.0")),
        ("15 / 4", Decimal("3.75")),
        ("14 // 3", Decimal("4")),
        ("14 % 3", Decimal("2")),
        ("2 + 3 * 4", Decimal("14")),
        ("(2 + 3) * 4", Decimal("20")),
        ("10 / (5 - 3)", Decimal("5")),
        ("-5 + 3", Decimal("-2")),
        ("5 + -3", Decimal("2")),
        ("+7 - +2", Decimal("5")),
        ("0.1 + 0.2", Decimal("0.3")),
        ("  10   +   20  *  2 ", Decimal("50")),
    ],
)
def test_calculator_valid_expressions(expression: str, expected: Decimal) -> None:
    """Test valid expressions, operator precedence, and Decimal precision."""
    assert calculate(expression) == expected


def test_division_by_zero() -> None:
    """Test division by zero errors for standard, floor division, and modulo."""
    with pytest.raises(DivisionByZeroError):
        calculate("10 / 0")
    with pytest.raises(DivisionByZeroError):
        calculate("10 // 0")
    with pytest.raises(DivisionByZeroError):
        calculate("10 % (5 - 5)")


def test_empty_expression() -> None:
    """Test rejection of empty expressions or whitespace-only strings."""
    with pytest.raises(EmptyExpressionError):
        calculate("")
    with pytest.raises(EmptyExpressionError):
        calculate("    ")


def test_invalid_characters() -> None:
    """Test rejection of invalid characters."""
    with pytest.raises(InvalidCharacterError):
        calculate("2 + a")
    with pytest.raises(InvalidCharacterError):
        calculate("10 $ 5")


def test_consecutive_operators() -> None:
    """Test rejection of consecutive operators."""
    with pytest.raises(ConsecutiveOperatorsError):
        calculate("2 + * 3")
    with pytest.raises(ConsecutiveOperatorsError):
        calculate("--3")


def test_unbalanced_parentheses() -> None:
    """Test rejection of mismatched or empty parentheses."""
    with pytest.raises(UnbalancedParenthesesError):
        calculate("(2 + 3")
    with pytest.raises(UnbalancedParenthesesError):
        calculate("2 + 3)")
    with pytest.raises(UnbalancedParenthesesError):
        calculate("() + 5")


def test_missing_operands() -> None:
    """Test rejection of missing operands and implicit multiplication."""
    with pytest.raises(MissingOperandError):
        calculate("2 +")
    with pytest.raises(MissingOperandError):
        calculate("* 5")
    with pytest.raises(MissingOperandError):
        calculate("2(3)")
