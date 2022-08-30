"""Ladestrategien und das Problem der n + 1 Abfragen."""


class CountingStore:
    """Ein Speicherabbild, das mitzählt, wie oft es befragt wird."""

    def __init__(self, parents, children):
        """Legt Väter und Kinder an.

        Args:
            parents: Liste der Vaterzeilen.
            children: Abbildung von Vaterschlüssel auf die Kinderzeilen.
        """
        self.parents = parents
        self.children = children
        self.queries = 0
        self.rows = 0

    def all_parents(self):
        """Liest alle Väter, eine Abfrage."""
        self.queries += 1
        self.rows += len(self.parents)
        return list(self.parents)

    def children_of(self, key):
        """Liest die Kinder eines Vaters, eine Abfrage."""
        self.queries += 1
        found = self.children.get(key, [])
        self.rows += len(found)
        return list(found)

    def joined(self):
        """Liest Väter und Kinder in einer Abfrage."""
        self.queries += 1
        rows = []
        for parent in self.parents:
            found = self.children.get(parent["id"], [])
            self.rows += len(found) if found else 1
            for child in found:
                rows.append((parent, child))
            if not found:
                rows.append((parent, None))
        return rows


def _example():
    """Baut drei Väter mit je zwei Kindern."""
    parents = [{"id": key} for key in (1, 2, 3)]
    children = {key: [{"id": key * 10 + step} for step in range(2)]
                for key in (1, 2, 3)}
    return parents, children


def load(strategy, touch_children):
    """Lädt die Väter und zählt die Abfragen.

    Args:
        strategy: ``lazy``, ``eager`` oder ``join``.
        touch_children: ob auf die Kinder zugegriffen wird.

    Returns:
        Abbildung mit der Zahl der Abfragen, der gelesenen Zeilen und der
        Väter.

    Raises:
        ValueError: bei einer unbekannten Strategie.
    """
    if strategy not in ("lazy", "eager", "join"):
        raise ValueError("unbekannte Ladestrategie")
    parents, children = _example()
    store = CountingStore(parents, children)
    if strategy == "join":
        store.joined()
    elif strategy == "eager":
        for parent in store.all_parents():
            store.children_of(parent["id"])
    else:
        loaded = store.all_parents()
        if touch_children:
            for parent in loaded:
                store.children_of(parent["id"])
    children_total = sum(len(entries) for entries in children.values())
    return {"queries": store.queries, "rows read": store.rows,
            "parents": len(parents), "children": children_total,
            "parent columns repeated": children_total - len(parents)
            if strategy == "join" else 0,
            "strategy": strategy}


def n_plus_one(parents):
    """Zahl der Abfragen beim verzögerten Laden mit Zugriff auf die Kinder."""
    if parents < 0:
        raise ValueError("negative Anzahl")
    return parents + 1


def join_versus_n_plus_one():
    """Stellt beide Wege gegenüber, die dieselben Daten holen.

    Der Verbund braucht eine Abfrage und liefert weniger Zeilen, wiederholt
    darin aber die Spalten des Vaters. Das verzögerte Laden mit Zugriff
    braucht n + 1 Abfragen und überträgt jede Vaterzeile genau einmal.

    Returns:
        Abbildung mit Abfragen, Zeilen und der Zahl der Wiederholungen.
    """
    joined = load("join", touch_children=True)
    lazily = load("lazy", touch_children=True)
    return {"join queries": joined["queries"],
            "lazy queries": lazily["queries"],
            "join rows": joined["rows read"],
            "lazy rows": lazily["rows read"],
            "parent columns repeated": joined["parent columns repeated"]}


def strategies():
    """Beschreibt, wofür jede Strategie gedacht ist."""
    return {"lazy": "load when touched, cheap until then",
            "eager": "load always, one query per parent unless joined",
            "join fetch": "one query, rows repeat the parent columns",
            "batch": "load the children of many parents in one query"}
