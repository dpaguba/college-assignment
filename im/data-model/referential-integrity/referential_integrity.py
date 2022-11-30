"""Referentielle Integrität: Reihenfolge und verwaiste Verweise."""

REFERENCES = {
    "kunde": (),
    "artikel": (),
    "lager": (),
    "verkaeufer": (),
    "liegt_in": ("lager", "artikel"),
    "kunde_wirbt_kunde": ("kunde",),
    "kassenbon": ("kunde",),
    "k_position": ("kassenbon", "artikel"),
    "betreut": ("kassenbon", "artikel", "verkaeufer"),
}


def creation_order():
    """Nennt eine Reihenfolge, in der die Tabellen angelegt werden können.

    Eine Tabelle kann erst entstehen, wenn alles existiert, worauf sie
    verweist. Das ist eine topologische Sortierung des Verweisgraphen,
    und sie ist nicht eindeutig: die vier Tabellen ohne Verweise können
    in beliebiger Reihenfolge kommen.

    Raises:
        ValueError: wenn die Verweise einen Kreis bilden.
    """
    done = []
    remaining = dict(REFERENCES)
    while remaining:
        ready = sorted(name for name, needs in remaining.items()
                       if all(other in done for other in needs))
        if not ready:
            raise ValueError("die Verweise bilden einen Kreis")
        done.extend(ready)
        for name in ready:
            del remaining[name]
    return done


def drop_order():
    """Nennt die Reihenfolge beim Löschen: die umgekehrte."""
    return list(reversed(creation_order()))


def orphans(rows, referenced, column, key):
    """Findet Verweise, deren Ziel fehlt.

    Args:
        rows: die verweisenden Zeilen.
        referenced: die Zeilen, auf die verwiesen wird.
        column: die Spalte mit dem Fremdschlüssel.
        key: die Spalte mit dem Primärschlüssel.

    Returns:
        Die Werte ohne Ziel, sortiert.

    Raises:
        ValueError: bei einer fehlenden Spalte.
    """
    if rows and column not in rows[0]:
        raise ValueError("unbekannte Spalte: %s" % column)
    if referenced and key not in referenced[0]:
        raise ValueError("unbekannte Spalte: %s" % key)
    targets = {row[key] for row in referenced}
    return sorted({row[column] for row in rows if row[column] not in targets})


def on_delete_options():
    """Nennt die drei Antworten auf eine Löschung mit Verweisen.

    RESTRICT lehnt die Löschung ab, solange noch verwiesen wird. CASCADE
    löscht die verweisenden Zeilen mit. SET NULL lässt sie stehen und
    leert den Verweis. Welche richtig ist, hängt daran, ob die
    verweisende Zeile ohne ihr Ziel noch Sinn ergibt: eine Bonposition
    ohne Bon nicht, ein Bon ohne Verkäufer schon.
    """
    return {"RESTRICT": "die Löschung wird abgelehnt",
            "CASCADE": "die verweisenden Zeilen werden mitgelöscht",
            "SET NULL": "der Verweis wird geleert, die Zeile bleibt",
            "question": "ergibt die verweisende Zeile ohne ihr Ziel noch "
                        "Sinn"}


def why_sqlite_needs_a_pragma():
    """Nennt eine Falle der Umgebung.

    In sqlite ist die Fremdschlüsselprüfung aus historischen Gründen
    standardmässig ausgeschaltet und muss je Verbindung mit ``PRAGMA
    foreign_keys = ON`` eingeschaltet werden. Wer das vergisst, bekommt
    eine Datenbank, die verwaiste Verweise klaglos annimmt, und merkt es
    erst, wenn eine Abfrage weniger Zeilen liefert als erwartet.
    """
    return {"default": "aus", "switch": "PRAGMA foreign_keys = ON",
            "scope": "je Verbindung, nicht je Datenbank",
            "symptom": "verwaiste Verweise fallen erst beim Verbund auf"}
