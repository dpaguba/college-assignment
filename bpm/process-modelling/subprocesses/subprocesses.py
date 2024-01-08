"""Teilprozesse: eingeklappt lesbar, ausgeklappt ausführbar."""


def example():
    """Der Bestellprozess mit einem Teilprozess in der Mitte.

    Returns:
        Abbildung vom Knoten auf seine Bestandteile; Blätter fehlen darin.
    """
    return {
        "root": ["Bestellung bestätigen", "Versand und Rechnung",
                 "Bestellung archivieren"],
        "Versand und Rechnung": ["Versandadresse empfangen",
                                 "Artikel versenden", "Rechnung erstellen",
                                 "Eingang verbuchen"],
    }


def top_level(model):
    """Nennt die Aktivitäten der obersten Ebene, eingeklappt."""
    return list(model["root"])


def is_subprocess(model, name):
    """Sagt, ob eine Aktivität einen Inhalt hat."""
    return name in model and name != "root"


def flatten(model, name="root", seen=None):
    """Klappt alle Teilprozesse aus und liefert die Blätter.

    Args:
        model: die Hierarchie.
        name: der Knoten, ab dem ausgeklappt wird.
        seen: die Knoten auf dem Weg dorthin, gegen Kreise.

    Returns:
        Liste der Blätter in der Reihenfolge des Modells.

    Raises:
        ValueError: wenn ein Teilprozess sich selbst enthält.
    """
    seen = set() if seen is None else seen
    if name in seen:
        raise ValueError("ein Teilprozess enthält sich selbst")
    leaves = []
    for child in model.get(name, ()):
        if is_subprocess(model, child):
            leaves.extend(flatten(model, child, seen | {name}))
        else:
            leaves.append(child)
    return leaves


def depth(model, name="root", seen=None):
    """Misst, wie tief die Hierarchie geschachtelt ist.

    Raises:
        ValueError: wenn ein Teilprozess sich selbst enthält.
    """
    seen = set() if seen is None else seen
    if name in seen:
        raise ValueError("ein Teilprozess enthält sich selbst")
    below = [depth(model, child, seen | {name})
             for child in model.get(name, ()) if is_subprocess(model, child)]
    return 1 + max(below, default=0)


def why_collapse():
    """Sagt, wozu das Einklappen dient.

    Ein Modell mit allen Aktivitäten auf einer Ebene ist vollständig und
    unlesbar. Der Teilprozess gibt dem Leser die Wahl: der Überblick zeigt
    drei Kästen, wer es genau wissen will, klappt den mittleren auf.
    """
    return {"collapsed": "drei Kästen für den Überblick",
            "expanded": "die Einzelheiten für die Ausführung",
            "same model": True,
            "rule of thumb": "eine Ebene passt auf eine Seite"}


def call_activity():
    """Trennt den eingebetteten vom aufgerufenen Teilprozess.

    Der eingebettete gehört zu seinem Elternprozess und wird nur dort
    benutzt. Der aufgerufene ist ein eigener Prozess, den mehrere
    Elternprozesse aufrufen; er wird einmal gepflegt und überall
    mitgeändert.
    """
    return {"embedded": {"lives in": "its parent", "reused": False},
            "call activity": {"lives in": "its own model", "reused": True},
            "choose call activity when": "more than one process needs it"}
