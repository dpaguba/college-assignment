"""Die IT-Projektportfoliomatrix aus Risiko und Nutzen."""

import math

SEGMENTS = ("I", "II", "III")

SCALE = 10.0

PROJECTS = {
    "P1 Kundenportal": {"risks": (4, 3, 2, 5, 4, 3), "fit": (8,) * 6},
    "P2 KI-Prognose": {"risks": (7, 6, 5, 8, 7, 6), "fit": (9,) * 6},
    "P3 ERP-Migration": {"risks": (6, 8, 2, 7, 9, 3), "fit": (6,) * 6},
    "P4 Neue Fassade": {"risks": (3, 4, 3), "fit": (7,) * 3},
    "P5 IoT Produkt": {"risks": (9, 7, 8), "fit": (8, 8, 9)},
}


def segments():
    """Nennt die Segmente von unten nach oben."""
    return list(SEGMENTS)


def meaning(segment):
    """Beschreibt ein Segment.

    Raises:
        ValueError: bei einem unbekannten Segment.
    """
    text = {
        "I": "hohes Risiko und geringer Nutzen: wird möglicherweise nie "
             "realisiert",
        "II": "mittlerer Nutzen oder mittleres Risiko: muss priorisiert "
              "werden, weil diese Projekte um Ressourcen konkurrieren",
        "III": "hoher Nutzen und geringes Risiko: wird zuerst genehmigt",
    }
    if segment not in text:
        raise ValueError("unbekanntes Segment")
    return text[segment]


def place(risk, utility, first=1 / 3, second=2 / 3):
    """Ordnet ein Projekt einem Segment zu.

    Die Matrix trägt den Nutzen nach oben und das Risiko nach links auf,
    und die Segmente sind Viertelkreise um die linke untere Ecke, also um
    hohes Risiko bei geringem Nutzen. Der Abstand von dieser Ecke
    entscheidet: je weiter weg, desto besser das Projekt.

    Args:
        risk: das Risiko auf einer Skala von eins bis zehn.
        utility: der Nutzen auf derselben Skala.
        first: die Grenze zwischen Segment I und II, als Anteil des
            grösstmöglichen Abstands.
        second: die Grenze zwischen II und III.

    Returns:
        Abbildung mit dem Segment, dem Abstand und den Eingaben.

    Raises:
        ValueError: bei einem Wert ausserhalb der Skala oder bei Grenzen
            in falscher Reihenfolge.
    """
    for value in (risk, utility):
        if not 0 <= value <= SCALE:
            raise ValueError("Wert ausserhalb der Skala")
    if not 0 < first < second < 1:
        raise ValueError("die Grenzen müssen aufsteigend zwischen 0 und 1 "
                         "liegen")
    distance = math.hypot(utility, SCALE - risk) / math.hypot(SCALE, SCALE)
    if distance < first:
        segment = "I"
    elif distance < second:
        segment = "II"
    else:
        segment = "III"
    return {"segment": segment, "distance": distance, "risk": risk,
            "utility": utility}


def place_all():
    """Ordnet die fünf Projekte der Tabelle ein.

    Das Risiko eines Projektes ist der Mittelwert seiner Risikowerte über
    alle Zeilen, der Nutzen der Mittelwert des strategischen Fits.

    Returns:
        Abbildung vom Projekt auf seine Einordnung.
    """
    placed = {}
    for name, row in PROJECTS.items():
        risk = sum(row["risks"]) / len(row["risks"])
        utility = sum(row["fit"]) / len(row["fit"])
        placed[name] = place(risk, utility)
    return placed


def reading():
    """Fasst zusammen, was bei diesen fünf Projekten herauskommt.

    Kein Projekt landet in Segment I: die Tabelle enthält keines, das
    zugleich riskant und nutzlos wäre. Die Entscheidung liegt damit nicht
    beim Streichen, sondern bei der Reihenfolge innerhalb von II und III,
    und dafür ist die dritte Grösse gedacht, die im Bild die Kreisgrösse
    trägt: das Budget.
    """
    placed = place_all()
    order = sorted(placed, key=lambda name: -placed[name]["distance"])
    return {"segment I": [name for name in placed
                          if placed[name]["segment"] == "I"],
            "order": order,
            "third dimension": "das Quartalsbudget, im Bild die Kreisgrösse",
            "decision": "nicht streichen, sondern reihen"}
