import re

from toolkit.constants import BINARY_OPERATOR
from toolkit.constants import PRECEDENCE
from toolkit.constants import TOKEN_REGEX
from toolkit.errors import ConsecutiveOperatorsError
from toolkit.errors import DivisionByZeroError
from toolkit.errors import EmptyExpressionError
from toolkit.errors import InvalidCharacterError
from toolkit.errors import MissingOperandError
from toolkit.errors import UnbalancedParenthesesError


def tokenize(expression: str) -> list[float | str]:
    if not expression.strip():
        raise EmptyExpressionError()
    tokens = []
    for match in re.finditer(TOKEN_REGEX, expression):
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
                (not tokens) or tokens[-1] in ("(", "u-") or tokens[-1] in BINARY_OPERATOR
            ):
                if captured_value == "-":
                    tokens.append("u-")
                else:
                    continue
            else:
                tokens.append(captured_value)
    return tokens


def validate(tokens: list[float | str]) -> None:
    if not tokens:  # Тк унарный плюс скипается, список токенов придет в валидатор пустым, если на вход дали только +
        raise MissingOperandError("+", "Expression cannot consist solely of an operator")
    if tokens[0] == ")" or tokens[0] in BINARY_OPERATOR:
        raise MissingOperandError(tokens[0], "Expression cannot start with binary operator")
    elif tokens[-1] in ("(", "u-") or tokens[-1] in BINARY_OPERATOR:
        raise MissingOperandError(tokens[-1], "Expression cannot end with an operator")
    open_paren = 0
    for t in tokens:  # проверка на количество скобок
        if t == "(":
            open_paren += 1
        elif t == ")":
            open_paren -= 1
            if open_paren < 0:
                raise UnbalancedParenthesesError("Closing parenthesis without opening one.")
    if open_paren != 0:
        raise UnbalancedParenthesesError("Unclosed opening parenthesis.")
    for prev, curr in zip(tokens, tokens[1:]):
        if prev == "(" and curr == ")":  # Пустые скобки: ()
            raise UnbalancedParenthesesError("Empty parentheses are not allowed.")
        if prev in BINARY_OPERATOR and curr in BINARY_OPERATOR:  # Два бинарных оператора подряд: 2 + * 3
            raise ConsecutiveOperatorsError(prev, curr)
        if prev == "(" and curr in BINARY_OPERATOR:  # Бинарный оператор сразу после открывающей скобки: ( * 3)
            raise MissingOperandError(curr, "Operator cannot follow open parenthesis.")
        if prev in BINARY_OPERATOR and curr == ")":  # Бинарный оператор перед закрывающей скобкой: (3 + )
            raise MissingOperandError(prev, "Operator cannot precede close parenthesis.")
        # Ошибки вокруг унарного минуса:
        # После u- не может идти бинарный знак (например, 2 * - * 3) или закрывающая скобка (-)
        if prev == "u-" and (curr in BINARY_OPERATOR or curr == ")"):
            raise MissingOperandError(curr, "Invalid token after unary minus.")
        if prev == "u-" and curr == "u-":  # Запрет цепочек унарных минусов без скобок: --3 (то есть ['u-', 'u-'])
            raise ConsecutiveOperatorsError(prev, curr, "Consecutive unary operators are not allowed.")
        if isinstance(prev, float) and isinstance(curr, float):  # Два числа подряд без знака операции: 2.0 3.0
            raise MissingOperandError("operator", f"Missing operator between numbers {prev} and {curr}.")
        if (
            (isinstance(prev, float) and curr == "(")
            or (prev == ")" and isinstance(curr, float))
            or (prev == ")" and curr == "(")
        ):  # Неявное умножение: 2(3) или (2)3 или (2)(3)
            raise MissingOperandError("*", "Implicit multiplication is not supported.")


def _sort_station(infix_notation: list[float | str]) -> list[float | str]:  # перевод в RPN
    result = []
    stack = []
    for token in infix_notation:
        if isinstance(token, float):
            result.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                result.append(stack.pop())
            stack.pop()
        elif token in PRECEDENCE:
            while stack and stack[-1] != "(" and PRECEDENCE[stack[-1]] >= PRECEDENCE[token]:
                result.append(stack.pop())
            stack.append(token)
    while stack:
        result.append(stack.pop())
    return result


def _eval_rpn(rpn: list[float | str]) -> float:
    stack = []
    for token in rpn:
        if isinstance(token, float):
            stack.append(token)
        elif token in BINARY_OPERATOR:
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token in ("/", "//", "%"):
                if b == 0:
                    raise DivisionByZeroError()
                elif token == "/":
                    stack.append(a / b)
                elif token == "//":
                    stack.append(a // b)
                elif token == "%":
                    stack.append(a % b)
        elif token == "u-":
            stack[-1] = stack[-1] * (-1)
    return stack[0]


def calculate(expression: str) -> float:
    tokens = tokenize(expression)
    validate(tokens)
    return _eval_rpn(_sort_station(tokens))
