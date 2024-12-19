"""Das Flags-Register und was eine Vergleichsoperation darin hinterlässt."""

POSITIONS = {"CF": 0, "PF": 2, "AF": 4, "ZF": 6, "SF": 7, "OF": 11}


def position(flag):
    """Nennt die Bitstelle eines Flags im Register.

    Raises:
        ValueError: bei einem unbekannten Flag.
    """
    if flag not in POSITIONS:
        raise ValueError("unbekanntes Flag")
    return POSITIONS[flag]


def subtract(first, second, bits=32):
    """Führt eine Subtraktion aus und liefert Ergebnis samt Flags.

    Das Übertragsflag gilt der vorzeichenlosen Rechnung und wird gesetzt,
    wenn geborgt werden musste. Das Überlaufflag gilt der
    vorzeichenbehafteten Rechnung und wird gesetzt, wenn das Ergebnis
    nicht mehr in den Wertebereich passt.

    Args:
        first, second: die Operanden.
        bits: Breite der Register.

    Returns:
        Abbildung mit ``result`` und den Flags.

    Raises:
        ValueError: bei einer nicht positiven Breite.
    """
    if bits < 1:
        raise ValueError("Breite muss positiv sein")
    mask = (1 << bits) - 1
    unsigned_first = first & mask
    unsigned_second = second & mask
    raw = unsigned_first - unsigned_second
    result = raw & mask
    signed_first = _to_signed(unsigned_first, bits)
    signed_second = _to_signed(unsigned_second, bits)
    signed_result = signed_first - signed_second
    limit = 1 << (bits - 1)
    return {"result": result,
            "CF": 1 if raw < 0 else 0,
            "ZF": 1 if result == 0 else 0,
            "SF": 1 if result >> (bits - 1) else 0,
            "OF": 1 if not -limit <= signed_result < limit else 0}


def _to_signed(value, bits):
    """Liest ein Bitmuster als Zweierkomplementzahl."""
    if value >> (bits - 1):
        return value - (1 << bits)
    return value


def compare(first, second, bits=32):
    """Vergleicht zwei Werte; das ist eine Subtraktion ohne Zielregister."""
    return subtract(first, second, bits)


def exercise_branches():
    """Wertet die vier Sprünge aus Aufgabe 2.1 aus.

    Verglichen werden 0 und 1234. Das Ergebnis ist nicht null, also
    springen je und jz nicht. Vorzeichenlos ist 0 kleiner als 1234, das
    Übertragsflag ist gesetzt und jb springt. Vorzeichenbehaftet ist 0
    ebenfalls kleiner; jl prüft SF ungleich OF, und das trifft zu.

    Returns:
        Abbildung von Sprungnamen auf die Antwort und die Flags.
    """
    flags = compare(0, 1234)
    return {"je": flags["ZF"] == 1, "jz": flags["ZF"] == 1,
            "jb": flags["CF"] == 1,
            "jl": flags["SF"] != flags["OF"],
            "flags": flags}


def read_register(value):
    """Liest die einzelnen Flags aus einem Registerwert."""
    return {name: (value >> index) & 1 for name, index in POSITIONS.items()}


def exercise_stack(start=0xFFFF):
    """Rechnet die Folge aus Aufgabe 2.1b nach.

    Die Flags werden auf den Stapel gelegt, in ax geholt und dort
    verändert: ``and 0xFFFE`` löscht das Übertragsflag, ``or 0x00C0``
    setzt Null- und Vorzeichenflag, ``and 0xF7FF`` löscht das
    Überlaufflag. Danach gehen sie zurück ins Register.

    Returns:
        Abbildung mit den vier Flags nach der Folge.
    """
    value = start
    value &= 0xFFFE
    value |= 0x00C0
    value &= 0xF7FF
    flags = read_register(value)
    return {"CF": flags["CF"], "ZF": flags["ZF"], "SF": flags["SF"],
            "OF": flags["OF"], "register": value}


def why_cmp_and_test_differ():
    """Nennt den Unterschied zwischen den beiden Prüfbefehlen.

    ``cmp`` subtrahiert, ``test`` verundet; beide verwerfen das Ergebnis
    und behalten nur die Flags. ``test rcx, rcx`` ist der übliche Weg, ein
    Register auf null oder auf ein negatives Vorzeichen zu prüfen.
    """
    return {"cmp": "subtracts, keeps the flags", "test": "ands, keeps the "
            "flags", "neither writes": "the destination register"}
