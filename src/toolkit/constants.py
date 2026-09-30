import re

UNITS_OF_MEASUREMEN: dict[str, dict[str, float]] = {
    "length": {"mm": 1.0, "cm": 10.0, "m": 1000.0, "km": 1_000_000.0},
    "mass": {"g": 1.0, "kg": 1_000.0},
}
token_specifications = [
    ("NUMBER", r"\d+(?:\.\d*)?|\.\d+"),  # 123; 123.45; 123.; .123
    ("OPERATOR", r"//|[+\-*/%]"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("SKIP", r"[ \t]+"),
    ("MISMATCH", r"."),
]
TOKEN_REGEX = re.compile("|".join(f"(?P<{name}>{reg})" for name, reg in token_specifications))
BINARY_OPERATOR = {"+", "-", "*", "/", "//", "%"}
PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "//": 2,
    "%": 2,
    "u-": 3,
}
