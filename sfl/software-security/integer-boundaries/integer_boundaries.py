"""Grenzen der Ganzzahlarithmetik und was an ihnen schiefgeht."""


def maximum(bits, signed=True):
    """Grösster darstellbarer Wert.

    Raises:
        ValueError: bei einer Breite kleiner als eins.
    """
    if bits < 1:
        raise ValueError("Breite muss positiv sein")
    return (1 << (bits - 1)) - 1 if signed else (1 << bits) - 1


def minimum(bits, signed=True):
    """Kleinster darstellbarer Wert.

    Raises:
        ValueError: bei einer nicht positiven Breite.
    """
    if bits < 1:
        raise ValueError("Breite muss positiv sein")
    return -(1 << (bits - 1)) if signed else 0


def wrap_signed(value, bits):
    """Bildet einen Wert auf den vorzeichenbehafteten Bereich ab."""
    mask = (1 << bits) - 1
    value &= mask
    if value >> (bits - 1):
        value -= 1 << bits
    return value


def add_signed(first, second, bits=32):
    """Addiert mit Überlauf, wie es die Maschine tut.

    In C ist ein Überlauf vorzeichenbehafteter Zahlen nicht festgelegt;
    die Maschine rechnet trotzdem im Zweierkomplement weiter, und aus zwei
    grossen positiven Zahlen wird eine negative.
    """
    return wrap_signed(first + second, bits)


def subtract_unsigned(first, second, bits=32):
    """Subtrahiert vorzeichenlos; unter null wird zur grössten Zahl."""
    mask = (1 << bits) - 1
    return (first - second) & mask


def overflows(first, second, bits=32):
    """Sagt, ob eine Addition den Bereich verlässt."""
    return not minimum(bits) <= first + second <= maximum(bits)


def exercise_inputs(bits=32):
    """Liefert zwei positive Zahlen, deren Summe negativ wird.

    Das ist die Aufgabe 3.1: das Programm nimmt zwei positive Zahlen und
    addiert sie; bestanden hat, wer ein negatives Ergebnis erzeugt. Zwei
    Werte etwas über der halben Obergrenze genügen.

    Returns:
        Abbildung mit beiden Zahlen, der Summe und der Grenze.
    """
    first = maximum(bits) // 2 + 1000
    second = maximum(bits) // 2 + 1000
    return {"first": first, "second": second,
            "sum": add_signed(first, second, bits),
            "mathematical sum": first + second,
            "limit": maximum(bits)}


def widen(value, from_bits, to_bits):
    """Erweitert einen vorzeichenbehafteten Wert auf mehr Bits.

    Das Vorzeichen wird fortgesetzt, deshalb bleibt −1 auch als breitere
    Zahl −1.

    Raises:
        ValueError: wenn nicht erweitert, sondern verkürzt wird.
    """
    if to_bits < from_bits:
        raise ValueError("das ist keine Erweiterung")
    return wrap_signed(value, to_bits)


def narrow(value, from_bits, to_bits):
    """Verkürzt einen Wert auf weniger Bits.

    Die oberen Bits fallen weg; aus 256 wird in acht Bit null.

    Raises:
        ValueError: wenn nicht verkürzt, sondern erweitert wird.
    """
    if to_bits > from_bits:
        raise ValueError("das ist keine Verkuerzung")
    return wrap_signed(value, to_bits)


def length_check_bypass(buffer_size=64):
    """Zeigt eine Längenprüfung, die sich mit einem negativen Wert umgehen lässt.

    Die Prüfung vergleicht vorzeichenbehaftet gegen die Puffergrösse; die
    Kopierfunktion nimmt die Länge vorzeichenlos. Eine negative Länge ist
    kleiner als die Grösse, besteht also die Prüfung, und wird beim
    Kopieren zu einer sehr grossen Zahl.

    Returns:
        Abbildung mit dem Ergebnis der Prüfung und der kopierten Menge.
    """
    length = -1
    passed = length < buffer_size
    copied = length & 0xFFFFFFFF
    return {"declared length": length, "check passed": passed,
            "buffer size": buffer_size, "bytes copied": copied,
            "reason": "the check is signed, the copy is not"}


def where_it_bites():
    """Nennt die Stellen, an denen die Grenzen in der Praxis auffallen."""
    return ["a length or size computed by addition or multiplication",
            "a subtraction that can go below zero on unsigned values",
            "a cast between a signed and an unsigned type",
            "an index computed from user input",
            "a difference of two pointers"]
