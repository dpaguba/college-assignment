"""Relative und absolute Bezüge und was Kopieren mit ihnen macht."""

import re

ADDRESS = re.compile(r"(\$?)([A-Z]{1,3})(\$?)([1-9][0-9]*)")


def _number(letters):
    """Rechnet Spaltenbuchstaben in eine Nummer um."""
    number = 0
    for character in letters:
        number = number * 26 + (ord(character) - ord("A") + 1)
    return number


def _letters(number):
    """Rechnet eine Spaltennummer zurück in Buchstaben."""
    letters = ""
    while number:
        number, rest = divmod(number - 1, 26)
        letters = chr(ord("A") + rest) + letters
    return letters


def kind(address):
    """Nennt die Art eines Bezugs.

    Raises:
        ValueError: bei einer fehlerhaften Adresse.
    """
    match = ADDRESS.fullmatch(str(address).strip().upper())
    if not match:
        raise ValueError("keine gültige Adresse")
    column_mark, _, row_mark, _ = match.groups()
    if column_mark and row_mark:
        return "absolut"
    if not column_mark and not row_mark:
        return "relativ"
    return "gemischt"


def shift(address, columns, rows):
    """Verschiebt einen Bezug um so viele Spalten und Zeilen.

    Der relative Anteil wandert mit, der absolute bleibt stehen. Genau
    das passiert beim Kopieren einer Formel, und es ist der Grund,
    weshalb ``$`` überhaupt existiert.

    Raises:
        ValueError: bei einer fehlerhaften Adresse oder wenn die
            Verschiebung aus dem Blatt hinausführt.
    """
    match = ADDRESS.fullmatch(str(address).strip().upper())
    if not match:
        raise ValueError("keine gültige Adresse")
    column_mark, letters, row_mark, digits = match.groups()
    column = _number(letters) + (0 if column_mark else columns)
    row = int(digits) + (0 if row_mark else rows)
    if column < 1 or row < 1:
        raise ValueError("die Verschiebung führt aus dem Blatt hinaus")
    return "%s%s%s%d" % (column_mark, _letters(column), row_mark, row)


def copy_formula(formula, source, target):
    """Kopiert eine Formel von einer Zelle in eine andere.

    Der Versatz ergibt sich aus den beiden Zellen; jede Adresse in der
    Formel wird um ihn verschoben, soweit sie relativ ist.

    Args:
        formula: die Formel, etwa ``=C6*(1+$D$22)``.
        source: die Zelle, in der sie steht.
        target: die Zelle, in die sie kommt.

    Returns:
        Die angepasste Formel.

    Raises:
        ValueError: bei einer fehlerhaften Adresse.
    """
    first = ADDRESS.fullmatch(str(source).strip().upper())
    second = ADDRESS.fullmatch(str(target).strip().upper())
    if not first or not second:
        raise ValueError("keine gültige Adresse")
    columns = _number(second.group(2)) - _number(first.group(2))
    rows = int(second.group(4)) - int(first.group(4))

    def move(match):
        """Verschiebt eine einzelne Adresse in der Formel."""
        return shift(match.group(0), columns, rows)

    return ADDRESS.sub(move, str(formula).upper())


def fill_down(formula, source, count):
    """Füllt eine Formel nach unten aus.

    Returns:
        Liste der Formeln, die erste ist die ursprüngliche.

    Raises:
        ValueError: bei einer nicht positiven Zahl oder einer fehlerhaften
            Adresse.
    """
    if count < 1:
        raise ValueError("mindestens eine Zelle")
    match = ADDRESS.fullmatch(str(source).strip().upper())
    if not match:
        raise ValueError("keine gültige Adresse")
    row = int(match.group(4))
    letters = match.group(2)
    return [copy_formula(formula, source, "%s%d" % (letters, row + step))
            for step in range(count)]


def the_receipt_mistake():
    """Zeigt den Fehler, den die Aufgabe verhindern will.

    Der Bruttopreis in D6 ist ``=C6*(1+$D$22)``. Wird die Formel nach
    unten ausgefüllt, wandert C6 mit und $D$22 bleibt. Ohne die
    Dollarzeichen wandert auch der Steuersatz: in D7 stünde D23, in D8
    dann D24, und weil dort nichts steht, rechnet die Tabelle mit null.
    Das Ergebnis ist kein Fehler, sondern der Nettopreis, und genau
    deshalb fällt es nicht auf.

    Returns:
        Abbildung mit beiden Varianten über acht Zeilen.
    """
    good = fill_down("=C6*(1+$D$22)", "D6", 8)
    bad = fill_down("=C6*(1+D22)", "D6", 8)
    return {"with dollars": good, "without": bad,
            "consequence": "ohne Dollarzeichen zeigt der Steuersatz nach "
                           "acht Zeilen auf eine leere Zelle",
            "and then": "die Formel rechnet mit null und liefert den "
                        "Nettopreis, ohne eine Fehlermeldung"}
