"""Cleaning: distances between strings, phonetic codes, and dates.

Two records referring to the same thing rarely match exactly. The edit
distance counts the single character changes between them, Soundex maps names
that sound alike to the same code, and date parsing has to accept the formats
the sources use and refuse the ones it cannot read rather than guessing.

The refusal is the part worth insisting on. A transformation that turns
unparseable input into a plausible value moves the error downstream, where it
is no longer visible as an error.
"""


def edit_distance(first, second):
    """The Levenshtein distance between two strings."""
    previous = list(range(len(second) + 1))
    for index, left in enumerate(first, start=1):
        current = [index]
        for position, right in enumerate(second, start=1):
            current.append(min(previous[position] + 1, current[position - 1] + 1,
                               previous[position - 1] + (left != right)))
        previous = current
    return previous[-1]


SOUNDEX_CODES = {"b": "1", "f": "1", "p": "1", "v": "1",
                 "c": "2", "g": "2", "j": "2", "k": "2", "q": "2", "s": "2",
                 "x": "2", "z": "2", "d": "3", "t": "3", "l": "4",
                 "m": "5", "n": "5", "r": "6"}
"""The consonant groups of the Soundex algorithm."""


def soundex(name):
    """The four character phonetic code of a name."""
    text = [character for character in name.lower() if character.isalpha()]
    if not text:
        return "0000"
    result = text[0].upper()
    previous = SOUNDEX_CODES.get(text[0], "")
    for character in text[1:]:
        code = SOUNDEX_CODES.get(character, "")
        if code and code != previous:
            result += code
        if character not in "hw":
            previous = code
        if len(result) == 4:
            break
    return (result + "000")[:4]


def normalise_date(text):
    """A date in one of the accepted formats, or nothing.

    The separator decides the order, because the digits cannot: 05.03.2024
    is the fifth of March in the German convention and 03/05/2024 is the same
    day in the American one, and a parser that guesses from the numbers alone
    is right only when one of them exceeds twelve.
    """
    separator = next((mark for mark in ("-", ".", "/") if mark in text), None)
    if separator is None:
        return None
    parts = text.split(separator)
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        return None
    if separator == "-" and len(parts[0]) == 4:
        year, month, day = parts
    elif separator == ".":
        day, month, year = parts
    elif separator == "/":
        month, day, year = parts
    else:
        return None
    if len(year) != 4:
        return None
    if not 1 <= int(month) <= 12 or not 1 <= int(day) <= 31:
        return None
    return "%04d-%02d-%02d" % (int(year), int(month), int(day))


def normalise_whitespace(text):
    """The text with runs of whitespace collapsed and the ends trimmed."""
    return " ".join(text.split())
