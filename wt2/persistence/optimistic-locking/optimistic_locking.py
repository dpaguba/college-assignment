"""Optimistisches Sperren über eine Versionsspalte."""


class StaleData(Exception):
    """Wird geworfen, wenn eine Zeile inzwischen von jemand anderem änderte."""


class Store:
    """Ein Speicher, dessen Zeilen eine Versionsnummer tragen."""

    def __init__(self, *rows):
        """Legt die Zeilen an, jede mit der Version null."""
        self.rows = {}
        for row in rows:
            entry = dict(row)
            entry["version"] = 0
            self.rows[entry["id"]] = entry

    def read(self, key):
        """Liest eine Zeile samt ihrer Version."""
        return dict(self.rows[key])

    def update(self, key, changes, version):
        """Schreibt eine Zeile, wenn die Version noch stimmt.

        Args:
            key: Schlüssel der Zeile.
            changes: die zu setzenden Felder.
            version: die Version, die beim Lesen galt.

        Raises:
            StaleData: wenn die Zeile inzwischen geändert wurde.
            KeyError: wenn die Zeile fehlt.
        """
        row = self.rows[key]
        if row["version"] != version:
            raise StaleData("Version %d erwartet, %d gefunden"
                            % (version, row["version"]))
        row.update(changes)
        row["version"] += 1
        return row

    def overwrite(self, key, changes):
        """Schreibt ohne Prüfung der Version."""
        row = self.rows[key]
        row.update(changes)
        row["version"] += 1
        return row


def lost_update(locking):
    """Führt zwei gleichzeitige Änderungen derselben Zeile aus.

    Beide lesen dieselbe Fassung, dann schreibt die erste, dann die
    zweite. Mit Versionsprüfung wird die zweite abgewiesen; ohne sie
    überschreibt sie die erste, ohne dass jemand es merkt.

    Returns:
        Abbildung mit dem, was übrig blieb, und ob die zweite abgewiesen
        wurde.
    """
    store = Store({"id": 1, "value": "start"})
    first_read = store.read(1)
    second_read = store.read(1)
    rejected = False
    if locking:
        store.update(1, {"value": "first"}, first_read["version"])
        try:
            store.update(1, {"value": "second"}, second_read["version"])
        except StaleData:
            rejected = True
    else:
        store.overwrite(1, {"value": "first"})
        store.overwrite(1, {"value": "second"})
    return {"survived": store.read(1)["value"],
            "second was rejected": rejected}


def compare_with_pessimistic():
    """Stellt beide Verfahren gegenüber.

    Optimistisch heisst: lesen, arbeiten, beim Schreiben prüfen und im
    Konfliktfall scheitern. Pessimistisch heisst: beim Lesen sperren, so
    dass die zweite Transaktion wartet statt zu scheitern.
    """
    return {"optimistic": "fails at commit", "pessimistic": "waits at read",
            "optimistic suits": "few conflicts, short transactions",
            "pessimistic suits": "many conflicts, long transactions"}


def retry(store, key, change, attempts=3):
    """Wiederholt eine Änderung, bis sie durchgeht.

    Der übliche Umgang mit dem optimistischen Sperren: den Konflikt
    auffangen, neu lesen und die Änderung noch einmal anwenden.

    Raises:
        StaleData: wenn auch der letzte Versuch scheitert.
    """
    for _ in range(attempts):
        row = store.read(key)
        try:
            return store.update(key, change(row), row["version"])
        except StaleData:
            continue
    raise StaleData("nach %d Versuchen aufgegeben" % attempts)
