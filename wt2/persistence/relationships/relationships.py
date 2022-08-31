"""Beziehungen zwischen Entitäten und ihre Abbildung auf Tabellen."""


def foreign_key_side(kind):
    """Nennt die Seite, auf der der Fremdschlüssel steht.

    Raises:
        ValueError: bei einer unbekannten Beziehungsart.
    """
    table = {"1:1": "either", "1:n": "many", "n:1": "many", "n:m": "none"}
    if kind not in table:
        raise ValueError("unbekannte Beziehungsart")
    return table[kind]


def needs_join_table(kind):
    """Sagt, ob eine eigene Verbindungstabelle nötig ist."""
    return foreign_key_side(kind) == "none"


def bidirectional_example():
    """Beschreibt eine beidseitige Beziehung zwischen Autor und Buch.

    Im Speicher gibt es zwei Verweise, in der Datenbank nur eine Spalte.
    Die besitzende Seite ist die mit dem Fremdschlüssel; die andere wird
    als abgebildet erklärt und schreibt nichts.

    Returns:
        Abbildung mit der besitzenden Seite und dem Vermerk der anderen.
    """
    return {"owning": "author_id on book",
            "other side is mapped by": True,
            "columns in the database": 1,
            "references in memory": 2}


def forgetting_the_owning_side():
    """Zeigt, was passiert, wenn nur die abgebildete Seite gesetzt wird.

    Die Liste im Autor wird gefüllt, die Spalte im Buch bleibt leer, und
    nach dem Neuladen ist die Beziehung verschwunden.

    Returns:
        Abbildung mit der Zahl der geschriebenen Zeilenänderungen.
    """
    author = {"id": 1, "books": []}
    book = {"id": 7, "author_id": None}
    author["books"].append(book)
    written = 1 if book["author_id"] is not None else 0
    return {"rows written": written, "in memory": len(author["books"]),
            "after reload": 0}


def cascade_example(cascade):
    """Löscht einen Autor mit und ohne Weitergabe an die Bücher.

    Args:
        cascade: ob das Löschen an die Kinder weitergereicht wird.

    Returns:
        Abbildung mit der Zahl der verbliebenen Kinder und der Frage, ob
        sie noch auf einen Autor verweisen, den es nicht mehr gibt.
    """
    authors = {1: {"id": 1}}
    books = {7: {"id": 7, "author_id": 1}, 8: {"id": 8, "author_id": 1}}
    del authors[1]
    if cascade:
        books = {key: row for key, row in books.items()
                 if row["author_id"] != 1}
    dangling = [row for row in books.values()
                if row["author_id"] not in authors]
    return {"children left": len(books), "dangling": len(dangling),
            "cascade": cascade}


def cascade_kinds():
    """Nennt die Weitergaben, die JPA kennt."""
    return ["PERSIST", "MERGE", "REMOVE", "REFRESH", "DETACH", "ALL"]


def orphan_removal():
    """Erklärt den Unterschied zur Weitergabe des Löschens.

    Die Weitergabe wirkt, wenn der Vater gelöscht wird. Das Entfernen
    verwaister Kinder wirkt auch, wenn ein Kind nur aus der Liste
    genommen wird.
    """
    return {"cascade remove": "parent deleted",
            "orphan removal": "child removed from the collection"}
