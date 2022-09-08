"""CAPTCHAs: wie viel eine Aufgabe wert ist und was sie kostet."""

import math


def entropy(alphabet, length):
    """Berechnet den Informationsgehalt einer Aufgabe in Bit.

    Raises:
        ValueError: bei nicht positiven Werten.
    """
    if alphabet < 1 or length < 1:
        raise ValueError("Alphabet und Laenge muessen positiv sein")
    return length * math.log2(alphabet)


def guessing_report(alphabet, length):
    """Schätzt, wie oft ein blind ratender Angreifer versuchen muss.

    Returns:
        Abbildung mit der Zahl der Möglichkeiten und den erwarteten
        Versuchen bis zum ersten Treffer.
    """
    space = alphabet ** length
    return {"space": space, "expected attempts": space / 2,
            "entropy": entropy(alphabet, length)}


def partial_solver(alphabet, length, read):
    """Schätzt die Trefferquote eines Lösers, der einen Teil sicher liest.

    Der Rest wird geraten; die Quote fällt also nur mit den ungelesenen
    Zeichen. Das ist der Grund, aus dem eine Aufgabe schon dann wertlos
    ist, wenn sie zu vier Fünfteln maschinell lesbar ist.

    Raises:
        ValueError: wenn mehr gelesen als vorhanden ist.
    """
    if read > length:
        raise ValueError("mehr gelesen als vorhanden")
    unknown = length - read
    rate = 1.0 / (alphabet ** unknown) if unknown else 1.0
    return {"success rate": rate, "attempts per solve": 1 / rate,
            "read": read, "guessed": unknown}


def usability():
    """Stellt Schwierigkeit und menschliche Trefferquote gegenüber.

    Je stärker eine Aufgabe verzerrt wird, desto seltener lösen auch
    Menschen sie richtig; die Aufgabe trennt dann nicht mehr zwischen
    Mensch und Maschine, sondern schliesst beide aus.

    Returns:
        Abbildung mit drei Schwierigkeitsstufen.
    """
    return {"easy": {"human success": 0.95, "machine success": 0.90},
            "medium": {"human success": 0.85, "machine success": 0.40},
            "hard": {"human success": 0.55, "machine success": 0.05}}


def separation():
    """Nennt die Stufe mit dem grössten Abstand zwischen Mensch und Maschine.

    Returns:
        Abbildung mit der besten Stufe und dem Abstand.
    """
    table = usability()
    best = max(table, key=lambda level: table[level]["human success"]
               - table[level]["machine success"])
    return {"best": best,
            "gap": table[best]["human success"]
            - table[best]["machine success"]}


def accessibility():
    """Nennt, wen eine reine Bildaufgabe ausschliesst."""
    return {"excluded": ["blind and partially sighted users",
                         "users with dyslexia", "users on small screens"],
            "alternatives": ["audio", "a simple question",
                             "a check of the behaviour instead of a puzzle"]}


def alternatives():
    """Nennt die Wege, die ohne eine Aufgabe an den Benutzer auskommen."""
    return {"rate limiting": "an attempt costs time",
            "proof of work": "an attempt costs computation",
            "behaviour analysis": "how the form was filled in",
            "honeypot field": "a field a human never sees and never fills"}
