"""Text encodings: ASCII and UTF-8.

ASCII is seven bits and covers English. UTF-8 extends it to every Unicode code
point while keeping ASCII byte-for-byte unchanged, which is why it displaced
every alternative: existing files were already valid.

The encoding is prefix-free by construction:

| code point | bytes | first byte | continuation bytes |
|---|---|---|---|
| up to 7 bits | 1 | `0xxxxxxx` | |
| up to 11 | 2 | `110xxxxx` | `10xxxxxx` |
| up to 16 | 3 | `1110xxxx` | `10xxxxxx` |
| up to 21 | 4 | `11110xxx` | `10xxxxxx` |

A continuation byte always starts with `10`, so a reader that lands in the
middle of a character can find the next boundary by scanning forward. That
property is why a corrupted byte costs one character rather than the rest of
the file.
"""

from __future__ import annotations


def ascii_code(character):
    """The ASCII code of a character."""
    code = ord(character)
    if code > 127:
        raise ValueError(f"{character!r} is not an ASCII character")
    return code


def utf8(character):
    """The UTF-8 bytes of a character, as integers."""
    code = ord(character)

    if code < 0x80:
        return [code]
    if code < 0x800:
        return [0xC0 | (code >> 6), 0x80 | (code & 0x3F)]
    if code < 0x10000:
        return [0xE0 | (code >> 12),
                0x80 | ((code >> 6) & 0x3F),
                0x80 | (code & 0x3F)]

    return [0xF0 | (code >> 18),
            0x80 | ((code >> 12) & 0x3F),
            0x80 | ((code >> 6) & 0x3F),
            0x80 | (code & 0x3F)]


def decode_utf8(stream):
    """Decode a byte sequence back into characters."""
    result = []
    index = 0

    while index < len(stream):
        first = stream[index]
        length = byte_count(first)
        code = first & (0xFF >> (length + 1)) if length > 1 else first

        for offset in range(1, length):
            code = (code << 6) | (stream[index + offset] & 0x3F)

        result.append(chr(code))
        index += length

    return "".join(result)


def byte_count(first):
    """How many bytes a character starting with this byte occupies."""
    if first < 0x80:
        return 1
    if first >= 0xF0:
        return 4
    if first >= 0xE0:
        return 3
    if first >= 0xC0:
        return 2
    raise ValueError("continuation byte cannot start a character")


def is_continuation(byte):
    """Whether a byte is a continuation byte."""
    return 0x80 <= byte < 0xC0


def resynchronise(stream, position):
    """The next character boundary at or after a position.

    The self-synchronising property in one function. A reader that starts in
    the middle of a multi-byte character skips continuation bytes until it
    finds a lead byte, and loses only the character it landed inside.
    """
    while position < len(stream) and is_continuation(stream[position]):
        position += 1
    return position


def encoded_length(text):
    """How many bytes a string occupies in UTF-8.

    Not the number of characters, which is the mistake behind every truncated
    string that ends in a broken character. A language with a fixed-width
    string type hides the distinction and a byte-oriented one does not.
    """
    return sum(len(utf8(character)) for character in text)
