"""Arbeitseinheit, schmutzige Prüfung und der Zeitpunkt des Schreibens."""


class UnitOfWork:
    """Sammelt Änderungen und schreibt sie erst beim Abschluss.

    Der Speicher merkt sich den Zustand beim Laden; beim Abschluss wird
    verglichen und nur das Geänderte geschrieben. Das ist die schmutzige
    Prüfung, die eine ausdrückliche Speicheranweisung überflüssig macht.
    """

    def __init__(self, store):
        """Legt eine Arbeitseinheit über einem Speicher an."""
        self.store = store
        self.loaded = {}
        self.snapshot = {}
        self.writes = 0
        self.committed = False
        self.detached = set()

    def load(self, key):
        """Lädt eine Zeile und merkt sich ihren Zustand.

        Beim zweiten Aufruf kommt dasselbe Objekt zurück; das ist die
        Identitätskarte der Arbeitseinheit.
        """
        if key not in self.loaded:
            row = dict(self.store[key])
            self.loaded[key] = row
            self.snapshot[key] = dict(row)
        return self.loaded[key]

    def detach(self, key):
        """Nimmt eine Zeile aus der Überwachung."""
        self.detached.add(key)

    def dirty(self):
        """Nennt die Schlüssel, deren Zustand sich geändert hat."""
        return [key for key, row in self.loaded.items()
                if key not in self.detached and row != self.snapshot[key]]

    def flush(self):
        """Schreibt die Änderungen, ohne die Transaktion zu beenden."""
        for key in self.dirty():
            self.store[key] = dict(self.loaded[key])
            self.snapshot[key] = dict(self.loaded[key])
            self.writes += 1

    def commit(self):
        """Schreibt die Änderungen und beendet die Transaktion."""
        self.flush()
        self.committed = True

    def rollback(self):
        """Verwirft alle Änderungen."""
        self.loaded = {}
        self.snapshot = {}
        self.committed = False


def dirty_checking():
    """Misst, wann geschrieben wird: beim Zuweisen oder beim Abschluss.

    Returns:
        Abbildung mit der Zahl der Schreibvorgänge während der Arbeit und
        beim Abschluss.
    """
    store = {1: {"id": 1, "title": "a"}}
    work = UnitOfWork(store)
    row = work.load(1)
    row["title"] = "b"
    during = work.writes
    work.commit()
    return {"writes during": during, "writes at commit": work.writes,
            "value": store[1]["title"]}


def rollback_example():
    """Zeigt, dass ein Rücksetzen den Speicher unberührt lässt.

    Returns:
        Abbildung mit dem Wert vor und nach dem Rücksetzen.
    """
    store = {1: {"id": 1, "title": "a"}}
    before = store[1]["title"]
    work = UnitOfWork(store)
    work.load(1)["title"] = "b"
    work.rollback()
    return {"before": before, "after": store[1]["title"]}


def identity_map_holds():
    """Prüft, dass zweimaliges Laden dasselbe Objekt liefert."""
    store = {1: {"id": 1, "title": "a"}}
    work = UnitOfWork(store)
    return work.load(1) is work.load(1)


def detached_example():
    """Zeigt, dass eine losgelöste Zeile nicht mehr geschrieben wird.

    Returns:
        Abbildung mit der Zahl der Schreibvorgänge.
    """
    store = {1: {"id": 1, "title": "a"}}
    work = UnitOfWork(store)
    row = work.load(1)
    work.detach(1)
    row["title"] = "b"
    work.commit()
    return {"written": work.writes, "value": store[1]["title"]}


def flush_example():
    """Zeigt, dass ein Abgleich schreibt, ohne die Transaktion zu beenden.

    Returns:
        Abbildung mit der Zahl der Schreibvorgänge und dem Abschlussstand.
    """
    store = {1: {"id": 1, "title": "a"}}
    work = UnitOfWork(store)
    work.load(1)["title"] = "b"
    work.flush()
    return {"written before commit": work.writes,
            "committed": work.committed}


def entity_states():
    """Nennt die Zustände, die eine Entität annehmen kann."""
    return {"new": "not yet known to the store",
            "managed": "watched by the unit of work",
            "detached": "known to the store, no longer watched",
            "removed": "scheduled for deletion"}
