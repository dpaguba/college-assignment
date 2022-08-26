"""Einseitenanwendungen: was beim ersten Aufruf und was danach geladen wird."""

import re

DOCUMENT_SIZE = 2
BUNDLE_SIZE = 300
DATA_SIZE = 8
SERVER_PAGE_SIZE = 40


def load_sequence():
    """Beschreibt, was beim ersten Aufruf über die Leitung geht.

    Returns:
        Abbildung mit der Liste der Anfragen und der Gesamtgrösse.
    """
    requests = [{"kind": "document", "size": DOCUMENT_SIZE},
                {"kind": "script", "size": BUNDLE_SIZE},
                {"kind": "style", "size": 20},
                {"kind": "data", "size": DATA_SIZE}]
    return {"requests": requests,
            "total": sum(entry["size"] for entry in requests)}


def navigate(path):
    """Beschreibt, was ein Wechsel der Ansicht kostet.

    Nach dem ersten Laden wird das Dokument nicht erneut geholt; nur die
    Daten der neuen Ansicht werden angefordert.

    Returns:
        Abbildung mit der Zahl der Anfragen je Art.
    """
    return {"path": path, "document requests": 0, "data requests": 1,
            "size": DATA_SIZE}


def traffic_comparison(pages):
    """Vergleicht das übertragene Volumen mit einer servergerenderten Seite.

    Die Einseitenanwendung zahlt einmal für das Bündel und danach nur die
    Daten; die servergerenderte Seite zahlt jedes Mal die ganze Seite.

    Raises:
        ValueError: bei einer nicht positiven Seitenzahl.
    """
    if pages < 1:
        raise ValueError("mindestens eine Seite")
    single = DOCUMENT_SIZE + BUNDLE_SIZE + 20 + pages * DATA_SIZE
    server = pages * SERVER_PAGE_SIZE
    return {"single page": single, "server rendered": server,
            "pages": pages,
            "break even": (DOCUMENT_SIZE + BUNDLE_SIZE + 20)
            / (SERVER_PAGE_SIZE - DATA_SIZE)}


def router(routes):
    """Baut eine Zuordnung von Mustern auf Komponenten.

    Ein Bestandteil, der mit einem Doppelpunkt beginnt, ist ein Parameter.
    """
    compiled = []
    for pattern, component in routes.items():
        names = []
        expression = []
        for part in pattern.strip("/").split("/"):
            if part.startswith(":"):
                names.append(part[1:])
                expression.append(r"([^/]+)")
            else:
                expression.append(re.escape(part))
        compiled.append((re.compile("^/" + "/".join(expression) + "$"),
                         names, component))
    return compiled


def resolve(compiled, path):
    """Sucht die Komponente zu einem Pfad.

    Returns:
        Abbildung mit ``component`` und ``parameters`` oder None.
    """
    for expression, names, component in compiled:
        match = expression.match(path)
        if match:
            return {"component": component,
                    "parameters": dict(zip(names, match.groups()))}
    return None


def trade_offs():
    """Nennt, was die Bauart gewinnt und was sie kostet."""
    return {"gains": ["no full reload between views",
                      "less work on the server",
                      "a clear split between data and presentation"],
            "costs": ["a large first load",
                      "the client needs javascript",
                      "search engines and the back button need care"]}
