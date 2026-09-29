from toolkit.errors import BelowAbsoluteZeroError
from toolkit.errors import IncompatibleUnitsError
from toolkit.errors import InvalidValueError
from toolkit.errors import UnknownUnitError

units_of_measurement: dict[str, dict[str, float]] = {
    "length": {"mm": 1.0, "cm": 10.0, "m": 1000.0, "km": 1_000_000.0},
    "mass": {"g": 1.0, "kg": 1_000.0},
}


def _get_category(unit: str) -> str:
    if unit in units_of_measurement["length"]:
        return "length"
    elif unit in units_of_measurement["mass"]:
        return "mass"
    elif unit in ("c", "f", "k"):
        return "temperature"
    else:
        raise UnknownUnitError(unit)


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit == "f":
        from_unit = "c"
        value = (value - 32) * (5 / 9)
    elif from_unit == "k":
        from_unit = "c"
        value = value - 273.15
    if value < -273.15:
        raise BelowAbsoluteZeroError
    if to_unit == "c":
        return value
    elif to_unit == "f":
        return value * (9 / 5) + 32
    else:
        return value + 273.15


def convert(value: float, from_unit: str, to_unit: str) -> float:
    try:
        value = float(value)
    except (ValueError, TypeError):
        raise InvalidValueError(value)
    from_unit = from_unit.strip().lower()
    to_unit = to_unit.strip().lower()
    from_unit_category = _get_category(from_unit)
    to_unit_category = _get_category(to_unit)
    if from_unit_category != to_unit_category:
        raise IncompatibleUnitsError(from_unit, to_unit)
    if from_unit_category == "length":
        return (
            value
            * units_of_measurement[from_unit_category][from_unit]
            / units_of_measurement[from_unit_category][to_unit]
        )
    elif from_unit_category == "mass":
        return (
            value
            * units_of_measurement[from_unit_category][from_unit]
            / units_of_measurement[from_unit_category][to_unit]
        )
    elif from_unit_category == "temperature":
        return _convert_temperature(value, from_unit, to_unit)
