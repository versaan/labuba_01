import re

from toolkit.errors import EmptyExpressionError
from toolkit.errors import InvalidCharacterError

token_specifications = [
    ("NUMBER", r"\d+(?:\.\d*)?|\.\d+"),  # 123; 123.45; 123.; .123
    ("OPERATOR", r"//|[+\-*/%]"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("SKIP", r"[ \t]+"),
    ("MISMATCH", r"."),
]
token_regex = re.compile("|".join(f"(?P<{name}>{reg})" for name, reg in token_specifications))


def tokenize(expression: str) -> list:
    if not expression.strip():
        raise EmptyExpressionError()
    tokens = []
    for match in re.finditer(token_regex, expression):
        group_name = match.lastgroup
        captured_value = match.group()
        if group_name == "MISMATCH":
            raise InvalidCharacterError(captured_value)
        elif group_name == "SKIP":
            continue
        elif group_name == "NUMBER":
            tokens.append(float(captured_value))
        elif group_name in ("LPAREN", "RPAREN"):
            tokens.append(captured_value)
        elif group_name == "OPERATOR":
            if captured_value in ("+", "-") and (
                (not tokens) or tokens[-1] in ("(", "+", "-", "*", "/", "//", "%", "u-", "u+")
            ):
                tokens.append(f"u{captured_value}")
            else:
                tokens.append(captured_value)
    return tokens
