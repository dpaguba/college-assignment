"""RISC-V instruction encoding: six formats, one word.

Every instruction is 32 bits, and the formats differ only in where the
immediate goes and which register fields are present.

| format | used by | immediate |
|---|---|---|
| R | `add`, `sub`, `and`, `or` | none |
| I | `addi`, `ori`, `lw`, `jalr` | 12 bits, sign extended |
| S | `sw` | 12 bits, split in two pieces |
| B | `bne`, `beq` | 13 bits, low bit always zero |
| U | `lui` | 20 bits, high part |
| J | `jal` | 21 bits, low bit always zero |

The splitting of the S and B immediates looks gratuitous and is not: the
register fields sit in the same bits in every format, so the decoder can read
them before it knows the format. The immediate is what gets scattered, because
it is the field the decoder can afford to assemble later.
"""

from __future__ import annotations

ABI_NAMES = {
    "zero": 0, "ra": 1, "sp": 2, "gp": 3, "tp": 4,
    "t0": 5, "t1": 6, "t2": 7, "s0": 8, "fp": 8, "s1": 9,
    "a0": 10, "a1": 11, "a2": 12, "a3": 13, "a4": 14, "a5": 15,
    "a6": 16, "a7": 17,
}
"""The ABI register names the exercise sheets use, such as `a1` for `x11`."""

FORMATS = {
    "add": ("R", 0b0110011, 0b000, 0b0000000),
    "sub": ("R", 0b0110011, 0b000, 0b0100000),
    "and": ("R", 0b0110011, 0b111, 0b0000000),
    "or": ("R", 0b0110011, 0b110, 0b0000000),
    "addi": ("I", 0b0010011, 0b000, None),
    "ori": ("I", 0b0010011, 0b110, None),
    "andi": ("I", 0b0010011, 0b111, None),
    "lw": ("I", 0b0000011, 0b010, None),
    "sw": ("S", 0b0100011, 0b010, None),
    "bne": ("B", 0b1100011, 0b001, None),
    "beq": ("B", 0b1100011, 0b000, None),
}
"""Format, opcode, funct3 and funct7 for the instructions the course uses."""


def register(name):
    """The number of a register, by ABI name or `xN`."""
    if name in ABI_NAMES:
        return ABI_NAMES[name]
    if name.startswith("x") and name[1:].isdigit():
        number = int(name[1:])
        if 0 <= number < 32:
            return number
    raise ValueError(f"unknown register {name}")


def format_of(name):
    """Which encoding format an instruction uses."""
    return FORMATS[name][0]


def encode(name, rd=None, rs1=None, rs2=None, immediate=0):
    """Assemble one instruction into a 32-bit word."""
    kind, opcode, funct3, funct7 = FORMATS[name]

    destination = register(rd) if rd else 0
    source_one = register(rs1) if rs1 else 0
    source_two = register(rs2) if rs2 else 0

    if kind == "R":
        return (funct7 << 25) | (source_two << 20) | (source_one << 15) \
            | (funct3 << 12) | (destination << 7) | opcode

    if kind == "I":
        _check_range(immediate, -2048, 2047)
        return ((immediate & 0xFFF) << 20) | (source_one << 15) \
            | (funct3 << 12) | (destination << 7) | opcode

    if kind == "S":
        _check_range(immediate, -2048, 2047)
        low = immediate & 0x1F
        high = (immediate >> 5) & 0x7F
        return (high << 25) | (source_two << 20) | (source_one << 15) \
            | (funct3 << 12) | (low << 7) | opcode

    if kind == "B":
        _check_range(immediate, -4096, 4094)
        if immediate % 2:
            raise ValueError("a branch offset must be even")
        bit12 = (immediate >> 12) & 1
        bit11 = (immediate >> 11) & 1
        high = (immediate >> 5) & 0x3F
        low = (immediate >> 1) & 0xF
        return (bit12 << 31) | (high << 25) | (source_two << 20) \
            | (source_one << 15) | (funct3 << 12) | (low << 8) | (bit11 << 7) | opcode

    raise ValueError(f"cannot encode format {kind}")


def _check_range(value, low, high):
    """Reject an immediate that does not fit the field."""
    if not low <= value <= high:
        raise ValueError(f"immediate {value} outside {low}..{high}")


def opcode_of(word):
    """The seven-bit opcode field."""
    return word & 0x7F


def fields(word):
    """Every field of an encoded instruction, with the immediate reassembled."""
    opcode = opcode_of(word)
    result = {
        "opcode": opcode,
        "rd": (word >> 7) & 0x1F,
        "funct3": (word >> 12) & 0x7,
        "rs1": (word >> 15) & 0x1F,
        "rs2": (word >> 20) & 0x1F,
        "funct7": (word >> 25) & 0x7F,
    }

    if opcode in (0b0010011, 0b0000011):
        raw = (word >> 20) & 0xFFF
        result["immediate"] = raw - 4096 if raw & 0x800 else raw
    elif opcode == 0b0100011:
        raw = (((word >> 25) & 0x7F) << 5) | ((word >> 7) & 0x1F)
        result["immediate"] = raw - 4096 if raw & 0x800 else raw
    elif opcode == 0b1100011:
        raw = ((((word >> 31) & 1) << 12) | (((word >> 7) & 1) << 11)
               | (((word >> 25) & 0x3F) << 5) | (((word >> 8) & 0xF) << 1))
        result["immediate"] = raw - 8192 if raw & 0x1000 else raw

    return result


def decode(word):
    """Recover the mnemonic and the fields of an encoded instruction."""
    parts = fields(word)

    for name, (kind, opcode, funct3, funct7) in FORMATS.items():
        if parts["opcode"] != opcode or parts["funct3"] != funct3:
            continue
        if funct7 is not None and parts["funct7"] != funct7:
            continue
        return {"name": name, "format": kind, **parts}

    raise ValueError(f"no instruction matches {word:#010x}")


def to_binary(word):
    """The 32-bit pattern, grouped by field, for reading by eye."""
    return format(word, "032b")
