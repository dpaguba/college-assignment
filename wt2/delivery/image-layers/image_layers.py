"""Schichten eines Abbilds und der Zwischenspeicher der Erstellung."""

import hashlib


def build(instructions, cache=None):
    """Baut ein Abbild aus einer Beschreibung.

    Jede Anweisung wird zu einer Schicht. Der Bezeichner einer Schicht
    hängt von der Anweisung und von allem darüber ab; ändert sich eine
    Zeile, ändert sich jede Schicht darunter und muss neu gebaut werden.

    Args:
        instructions: die Zeilen der Beschreibung.
        cache: die Schichten eines früheren Baus.

    Returns:
        Abbildung mit ``layers``, der Zahl der neu gebauten Schichten und
        der Zahl der Treffer im Zwischenspeicher.

    Raises:
        ValueError: bei einer leeren Beschreibung.
    """
    if not instructions:
        raise ValueError("leere Beschreibung")
    cached = list(cache or [])
    layers = []
    rebuilt = 0
    hits = 0
    parent = ""
    still_matching = True
    for index, line in enumerate(instructions):
        identifier = hashlib.sha256((parent + "|" + line).encode("utf-8")
                                    ).hexdigest()[:12]
        if still_matching and index < len(cached) \
                and cached[index] == identifier:
            hits += 1
        else:
            still_matching = False
            rebuilt += 1
        layers.append(identifier)
        parent = identifier
    return {"layers": layers, "rebuilt": rebuilt, "cache hits": hits,
            "instructions": list(instructions)}


def ordering_report():
    """Vergleicht zwei Reihenfolgen derselben Anweisungen.

    Werden die Abhängigkeiten vor den Quellen kopiert, so überlebt ihre
    Installation eine Änderung am Quelltext. In der anderen Reihenfolge
    wird sie jedes Mal wiederholt.

    Returns:
        Abbildung mit der Zahl der neu gebauten Schichten in beiden
        Reihenfolgen.
    """
    dependencies_first = ["FROM base", "COPY requirements.txt /app/",
                          "RUN install", "COPY . /app", "CMD run"]
    sources_first = ["FROM base", "COPY . /app",
                     "COPY requirements.txt /app/", "RUN install", "CMD run"]
    results = {}
    for name, lines in (("dependencies first", dependencies_first),
                        ("sources first", sources_first)):
        first = build(lines)
        changed = list(lines)
        position = changed.index("COPY . /app")
        changed[position] = "COPY . /app # sources changed"
        results[name] = build(changed, cache=first["layers"])["rebuilt"]
    return results


def deleted_file_still_costs(size=100):
    """Zeigt, dass eine spätere Löschung den Platz nicht zurückgibt.

    Eine Schicht schreibt nur hinzu. Wird eine Datei in einer späteren
    Schicht entfernt, so ist sie im fertigen Abbild unsichtbar, liegt aber
    weiterhin in der Schicht darunter.

    Returns:
        Abbildung mit der Grösse des Abbilds und der sichtbaren Dateien.
    """
    layers = [{"adds": {"big.tar": size}}, {"removes": ["big.tar"]}]
    total = sum(sum(layer.get("adds", {}).values()) for layer in layers)
    visible = {}
    for layer in layers:
        visible.update(layer.get("adds", {}))
        for name in layer.get("removes", []):
            visible.pop(name, None)
    return {"size": total, "visible files": len(visible),
            "lesson": "add and remove in one instruction"}


def objects():
    """Nennt die drei Objekte, um die es geht."""
    return {"dockerfile": "the description of an image",
            "image": "a read only stack of layers",
            "container": "a running instance with a writable layer on top"}


def why_layers():
    """Nennt, was die Schichtung einbringt."""
    return ["a shared base is stored once",
            "an unchanged step is not repeated",
            "only the changed layers travel over the network",
            "the same image runs everywhere the runtime does"]
