"""Unit tests for the unit converter module."""

import pytest

from toolkit.converter import convert
from toolkit.errors import BelowAbsoluteZeroError
from toolkit.errors import IncompatibleUnitsError
from toolkit.errors import InvalidValueError
from toolkit.errors import UnknownUnitError


@pytest.mark.parametrize(
    "value, from_u, to_u, expected",
    [
        (1000.0, "mm", "m", 1.0),
        (5.0, "km", "m", 5000.0),
        (2.5, "kg", "g", 2500.0),
        (500.0, "G", "kg", 0.5),
        (0.0, "C", "K", 273.15),
        (32.0, "f", "c", 0.0),
        (300.0, "k", "k", 300.0),
    ],
)
def test_converter_valid_conversions(value: float, from_u: str, to_u: str, expected: float) -> None:
    """Test valid unit conversions with case-insensitivity."""
    assert convert(value, from_u, to_u) == pytest.approx(expected, rel=1e-4)


def test_incompatible_units() -> None:
    """Test conversion between different unit categories."""
    with pytest.raises(IncompatibleUnitsError):
        convert(100.0, "kg", "m")
    with pytest.raises(IncompatibleUnitsError):
        convert(25.0, "c", "km")


def test_unknown_unit() -> None:
    """Test rejection of unsupported units."""
    with pytest.raises(UnknownUnitError):
        convert(10.0, "lightyear", "m")
    with pytest.raises(UnknownUnitError):
        convert(10.0, "kg", "pound")


def test_below_absolute_zero() -> None:
    """Test rejection of temperatures below absolute zero."""
    with pytest.raises(BelowAbsoluteZeroError):
        convert(-300.0, "c", "k")
    with pytest.raises(BelowAbsoluteZeroError):
        convert(-500.0, "f", "c")
    with pytest.raises(BelowAbsoluteZeroError):
        convert(-1.0, "k", "c")


def test_invalid_value() -> None:
    """Test rejection of non-numeric values."""
    with pytest.raises(InvalidValueError):
        convert("invalid_num", "m", "km")  # type: ignore[arg-type]
