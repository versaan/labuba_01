"""CLI entry point for the toolkit package."""

import argparse
import sys

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the CLI argument parser.

    Returns:
        argparse.ArgumentParser: Configured parser with calc and convert subparsers.
    """
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Console toolkit: calculator and unit converter.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for calculator
    calc_parser = subparsers.add_parser("calc", help="Calculate a mathematical expression.")
    calc_parser.add_argument("expression", type=str, help="Mathematical expression string.")

    # Subparser for converter
    convert_parser = subparsers.add_parser("convert", help="Convert units of measurement.")
    convert_parser.add_argument("value", help="Value to convert.")
    convert_parser.add_argument(
        "--from",
        dest="from_unit",
        required=True,
        help="Source unit.",
    )
    convert_parser.add_argument(
        "--to",
        dest="to_unit",
        required=True,
        help="Target unit.",
    )

    return parser


def main() -> None:
    """Main CLI execution function.

    Parses arguments, executes the requested command, and handles errors.
    """
    parser = create_parser()
    args = parser.parse_args()

    try:
        if args.command == "calc":
            result = calculate(args.expression)
            print(result)
            sys.exit(0)
        elif args.command == "convert":
            result = convert(args.value, args.from_unit, args.to_unit)
            print(result)
            sys.exit(0)
    except ToolkitError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
