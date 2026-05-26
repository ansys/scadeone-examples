"""Convert Advent of Code 2024 Day 3 puzzle input to Swan constant files."""

from pathlib import Path

SWAN_25R1_HEADER = "-- version swan: 2025.0 graph: 2.0"


def swan_const(name, type, value):
    """Return a Swan constant declaration as a string.

    Args:
        name: Constant identifier.
        type: Swan type of the constant.
        value: Value of the constant.

    Returns
    -------
        A Swan constant declaration, e.g. ``const FOO: int32 = 42;``.
    """
    return f"const {name}: {type} = {value};\n"


def str_to_char_array(line):
    """Convert a string to a Swan character-array literal.

    Args:
        line: Input string, e.g. ``'abcdef'``.

    Returns
    -------
        A Swan array literal, e.g. ``['a','b','c','d','e','f']``.
    """
    # No f-string for Python 3.11 compatibility
    return "['" + "','".join(list(line)) + "']"


def input_to_swan(base_name):
    """Convert an Advent of Code text input file to a Swan constants file.

    Reads ``<base_name>.txt`` from the same directory as this script and writes
    ``<base_name>.swan`` into the sibling ``assets/`` folder.  The output
    declares two Swan constants: ``<BASE_NAME>_STRING_LENGTH`` (``int32``) and
    ``<BASE_NAME>_STRING`` (``char^<BASE_NAME>_STRING_LENGTH``).

    If the input file is not found, the output Swan file contains a comment
    with instructions for downloading the puzzle input.

    Args:
        base_name: Stem used for both the input file and the output module,
            e.g. ``'input'`` or ``'sample'``.
    """
    input_file, swan_file, swan_prefix = (
        f"{base_name}.txt",
        f"{base_name}.swan",
        base_name.upper(),
    )
    in_path = Path(__file__).parent() / input_file
    out_path = Path(__file__).parent() / ".." / "assets" / swan_file

    with out_path.open("w") as f_out:
        if not Path(in_path).exists():
            f_out.write(
                f"-- Input file {input_file} not found. Please download yours from https://adventofcode.com/2024/day/3 and add it to the resources folder."
            )
            return

        with Path(in_path).open("r") as f_in:
            lines = [line.rstrip() for line in f_in.readlines()]
            string = "".join(lines)

            f_out.write(SWAN_25R1_HEADER + "\n")
            f_out.write(
                swan_const(f"{swan_prefix}_STRING_LENGTH", "int32", len(string))
            )
            f_out.write(
                swan_const(
                    f"{swan_prefix}_STRING",
                    f"char^{swan_prefix}_STRING_LENGTH",
                    str_to_char_array(string),
                )
            )


if __name__ == "__main__":
    input_to_swan("sample")
    input_to_swan("input")
