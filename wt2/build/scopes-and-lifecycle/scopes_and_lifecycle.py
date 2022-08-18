"""Lebenszyklus einer Standardbuild und die Sichtbarkeit der Abhängigkeiten."""

PHASES = ["validate", "compile", "test", "package", "verify", "install",
          "deploy"]

SCOPES = {
    "compile": {"compile": True, "test": True, "runtime": True},
    "provided": {"compile": True, "test": True, "runtime": False},
    "runtime": {"compile": False, "test": True, "runtime": True},
    "test": {"compile": False, "test": True, "runtime": False},
    "system": {"compile": True, "test": True, "runtime": False},
}


def phases():
    """Nennt die Phasen des Standardlebenszyklus in ihrer Reihenfolge."""
    return list(PHASES)


def run(phase):
    """Bestimmt, welche Phasen bis zur genannten ausgeführt werden.

    Eine Phase anzustossen bedeutet, alle vorangehenden mit auszuführen;
    das ist der Grund, aus dem der Aufruf von ``install`` auch testet.

    Raises:
        ValueError: bei einer unbekannten Phase.
    """
    if phase not in PHASES:
        raise ValueError("unbekannte Phase")
    return PHASES[:PHASES.index(phase) + 1]


def available(scope, moment):
    """Sagt, ob eine Abhängigkeit zu diesem Zeitpunkt im Klassenpfad steht.

    Args:
        scope: der deklarierte Geltungsbereich.
        moment: ``compile``, ``test`` oder ``runtime``.

    Raises:
        ValueError: bei unbekanntem Bereich oder Zeitpunkt.
    """
    if scope not in SCOPES:
        raise ValueError("unbekannter Geltungsbereich")
    if moment not in ("compile", "test", "runtime"):
        raise ValueError("unbekannter Zeitpunkt")
    return SCOPES[scope][moment]


def why_provided():
    """Erklärt, wofür der Bereich ``provided`` gedacht ist.

    Die Abhängigkeit wird zum Übersetzen gebraucht, liegt zur Laufzeit
    aber schon in der Umgebung; sie zweimal auszuliefern führt zu zwei
    Fassungen derselben Klasse im Klassenpfad.
    """
    return {"needed to compile": True, "shipped in the artefact": False,
            "example": "the servlet api, provided by the container"}


def convention_over_configuration():
    """Nennt die Verzeichnisse, die ohne Konfiguration erwartet werden."""
    return {"src/main/java": "sources", "src/main/resources": "resources",
            "src/test/java": "test sources", "target": "output"}
