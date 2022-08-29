"""Abbildung von Objekten auf Tabellenzeilen."""


class Entity:
    """Ein Objekt, das einer Zeile entspricht.

    Die Gleichheit richtet sich nach dem Schlüssel, nicht nach den
    Feldern: zwei Objekte mit demselben Schlüssel bezeichnen dieselbe
    Zeile, auch wenn eines davon geändert wurde.
    """

    def __init__(self, kind, fields, key):
        """Legt ein Objekt an.

        Args:
            kind: Name der Klasse.
            fields: Abbildung der Feldnamen auf Werte.
            key: Name des Schlüsselfelds.

        Raises:
            ValueError: wenn kein Schlüsselfeld genannt ist oder es fehlt.
        """
        if not key:
            raise ValueError("eine Entitaet braucht einen Schluessel")
        if key not in fields:
            raise ValueError("das Schluesselfeld fehlt")
        self.kind = kind
        self.fields = dict(fields)
        self.key = key

    @property
    def identifier(self):
        """Der Wert des Schlüsselfelds, None vor dem Einfügen."""
        return self.fields[self.key]

    def __eq__(self, other):
        """Vergleicht zwei Objekte über Klasse und Schlüssel."""
        if not isinstance(other, Entity):
            return NotImplemented
        if self.identifier is None or other.identifier is None:
            return self is other
        return (self.kind, self.identifier) == (other.kind, other.identifier)

    def __hash__(self):
        """Streuwert aus Klasse und Schlüssel."""
        return hash((self.kind, self.identifier))

    def __repr__(self):
        """Kurze Darstellung für Fehlermeldungen."""
        return "Entity(%s, %s)" % (self.kind, self.identifier)


class Store:
    """Ein sehr kleines Speicherabbild mit fortlaufenden Schlüsseln."""

    def __init__(self):
        """Legt einen leeren Speicher an."""
        self.rows = {}
        self.next_key = 1

    def insert(self, entity):
        """Fügt ein Objekt ein und vergibt dabei den Schlüssel.

        Vor dem Einfügen ist der Schlüssel unbekannt; das ist der Grund,
        aus dem er sich nicht für die Gleichheit im Hauptspeicher eignet,
        solange das Objekt neu ist.
        """
        if entity.identifier is None:
            entity.fields[entity.key] = self.next_key
            self.next_key += 1
        self.rows[entity.identifier] = dict(entity.fields)
        return entity


def identity_versus_equality():
    """Vergleicht die Gleichheit nach Schlüssel mit der nach Feldern.

    Dieselbe Zeile, einmal frisch gelesen und einmal geändert, ist nach
    Feldern zweimal verschieden und landet zweimal in einer Menge.

    Returns:
        Abbildung mit den Grössen beider Mengen.
    """
    first = Entity("Book", {"id": 1, "title": "a"}, "id")
    second = Entity("Book", {"id": 1, "title": "b"}, "id")
    by_key = {first, second}
    by_fields = {(entity.kind, tuple(sorted(entity.fields.items())))
                 for entity in (first, second)}
    return {"by key": len(by_key), "by fields": len(by_fields)}


def table_name(class_name, override=None):
    """Bestimmt den Tabellennamen zu einer Klasse.

    Ohne Angabe gilt die Namenskonvention: der Klassenname in
    Kleinbuchstaben.
    """
    return override if override else class_name.lower()


def columns(fields, transient=()):
    """Nennt die Felder, die in die Tabelle geschrieben werden."""
    return {name: value for name, value in fields.items()
            if name not in transient}


def key_strategies():
    """Nennt die Wege, einen Schlüssel zu vergeben."""
    return {"identity": "the database counts, known only after the insert",
            "sequence": "a database sequence, can be read in advance",
            "table": "a table of counters, portable and slow",
            "assigned": "the application supplies it"}
