"""Wiederholbarkeit einer Build: was eine Version festlegt und was nicht."""

import hashlib


def is_reproducible(version):
    """Sagt, ob eine Versionsangabe immer dasselbe Artefakt bezeichnet.

    Ein Bereich, ein Schnappschuss und die Schlüsselwörter für die neueste
    Fassung binden nichts fest: was heute gebaut wird, kann morgen etwas
    anderes sein.

    Raises:
        ValueError: bei einer leeren Angabe.
    """
    if not version:
        raise ValueError("leere Versionsangabe")
    text = version.strip()
    if text.upper() in ("LATEST", "RELEASE"):
        return False
    if text.endswith("-SNAPSHOT"):
        return False
    if text[0] in "[(" or "," in text:
        return False
    if text.endswith("+") or ".x" in text:
        return False
    return True


def resolve_range(specification, available):
    """Wählt aus einem Bereich die höchste passende Version.

    Args:
        specification: Bereich der Form ``[1.0,2.0)``.
        available: die im Verzeichnis vorhandenen Versionen.

    Returns:
        Die gewählte Version oder None.

    Raises:
        ValueError: bei einem unlesbaren Bereich.
    """
    text = specification.strip()
    if text[0] not in "[(" or text[-1] not in "])":
        raise ValueError("kein Bereich")
    lower_closed = text[0] == "["
    upper_closed = text[-1] == "]"
    lower, upper = text[1:-1].split(",")
    fitting = []
    for version in available:
        key = _key(version)
        if lower.strip() and (key < _key(lower) or
                              (key == _key(lower) and not lower_closed)):
            continue
        if upper.strip() and (key > _key(upper) or
                              (key == _key(upper) and not upper_closed)):
            continue
        fitting.append(version)
    if not fitting:
        return None
    return max(fitting, key=_key)


def _key(version):
    """Zerlegt eine Version in ihre Zahlen, damit sie sich ordnen lässt."""
    parts = []
    for piece in version.strip().split("."):
        digits = ""
        for character in piece:
            if character.isdigit():
                digits += character
            else:
                break
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def range_drift():
    """Zeigt, dass zwei Builds mit einem Bereich verschieden ausfallen können.

    Zwischen den beiden Builds erscheint im Verzeichnis eine neue Version,
    die zum Bereich passt; ohne dass sich die Projektdatei ändert, wird
    etwas anderes gebaut.

    Returns:
        Abbildung mit beiden aufgelösten Versionen.
    """
    specification = "[1.0,2.0)"
    before = ["1.0", "1.1"]
    after = ["1.0", "1.1", "1.2"]
    return {"first": resolve_range(specification, before),
            "second": resolve_range(specification, after),
            "specification": specification}


def with_lock_file():
    """Zeigt, was eine festgeschriebene Liste ändert.

    Werden die aufgelösten Versionen einmal festgehalten, ändert eine neue
    Fassung im Verzeichnis nichts mehr.

    Returns:
        Abbildung mit beiden Ergebnissen.
    """
    lock = {"library": "1.1"}
    return {"first": lock["library"], "second": lock["library"],
            "locked": True}


def artefact_hash(sources, timestamp=None):
    """Bildet den Prüfwert eines Artefakts aus den Quellen.

    Wird ein Zeitstempel mit eingerechnet, unterscheiden sich zwei Builds
    derselben Quellen; das ist der häufigste Grund, aus dem ein Artefakt
    nicht bitgleich wiederholbar ist.
    """
    digest = hashlib.sha256()
    for name in sorted(sources):
        digest.update(name.encode("utf-8"))
        digest.update(sources[name].encode("utf-8"))
    if timestamp is not None:
        digest.update(str(timestamp).encode("utf-8"))
    return digest.hexdigest()


def deterministic_output():
    """Prüft, dass gleiche Quellen ohne Zeitstempel gleich hashen."""
    sources = {"Main.java": "class Main {}", "Util.java": "class Util {}"}
    first = artefact_hash(sources)
    second = artefact_hash(dict(reversed(list(sources.items()))))
    stamped = artefact_hash(sources, timestamp=1)
    return first == second and first != stamped
