"""Spezialisierung und Generalisierung mit (T/P, D/N)."""

LABELS = ("T", "P", "D", "N")

MEANING = {
    "T": "total: jede Entität gehört mindestens einem Spezialfall an",
    "P": "partiell: eine Entität darf, muss aber nicht",
    "D": "disjunkt: höchstens ein Spezialfall je Entität",
    "N": "nicht disjunkt: beliebig viele Spezialfälle je Entität",
}


def labels():
    """Nennt die vier Buchstaben in der Reihenfolge der Paare."""
    return list(LABELS)


def meaning(label):
    """Erklärt einen Buchstaben.

    Raises:
        ValueError: bei einem unbekannten Buchstaben.
    """
    if label not in MEANING:
        raise ValueError("unbekannte Beschriftung")
    return MEANING[label]


def model(completeness, overlap, cases, members_of, members):
    """Baut eine Spezialisierung samt Ausprägung.

    Args:
        completeness: ``T`` oder ``P``.
        overlap: ``D`` oder ``N``.
        cases: die Namen der Spezialfälle.
        members_of: Abbildung vom Spezialfall auf seine Entitäten.
        members: alle Entitäten des Obertyps.

    Raises:
        ValueError: bei einer unzulässigen Beschriftung.
    """
    if completeness not in ("T", "P"):
        raise ValueError("die Vollständigkeit ist T oder P")
    if overlap not in ("D", "N"):
        raise ValueError("die Überlappung ist D oder N")
    return {"completeness": completeness, "overlap": overlap,
            "cases": list(cases),
            "members of": {name: list(values)
                           for name, values in members_of.items()},
            "members": list(members)}


def check(model):
    """Prüft eine Ausprägung gegen die beiden Beschriftungen.

    Returns:
        Abbildung mit den Verstössen und der Zuordnung je Entität.
    """
    belongs = {}
    for name in model["cases"]:
        for member in model["members of"].get(name, ()):
            belongs.setdefault(member, []).append(name)
    violations = []
    if model["completeness"] == "T":
        for member in model["members"]:
            if not belongs.get(member):
                violations.append("%s ist in keinem Spezialfall" % member)
    if model["overlap"] == "D":
        for member in sorted(belongs):
            if len(belongs[member]) > 1:
                violations.append("%s ist in %d Spezialfällen"
                                  % (member, len(belongs[member])))
    return {"violations": violations, "belongs to": belongs}


def employee_example():
    """Das Beispiel des Merkblatts: Mitarbeiter, partiell und disjunkt.

    Mitarbeiter werden in Verwaltungskräfte und Werkstudenten unterteilt.
    Partiell, weil es an einer Universität auch wissenschaftliche
    Angestellte gibt, die in keine der beiden Gruppen fallen. Disjunkt,
    weil eine Verwaltungskraft kein Werkstudent ist und umgekehrt.
    """
    return {"parent": "Mitarbeiter", "attribute": "MANummer",
            "cases": ["Verwaltungskraft", "Werkstudent"],
            "extra attribute": {"Werkstudent": "Studiengang"},
            "completeness": "P", "overlap": "D",
            "why partial": "es gibt auch wissenschaftliche Angestellte",
            "why disjoint": "die beiden Rollen schliessen einander aus"}


def combinations():
    """Nennt die vier möglichen Paare und je ein Beispiel."""
    return {
        ("T", "D"): "jede Person ist genau eines von: minderjährig, "
                    "volljährig",
        ("T", "N"): "jedes Fahrzeug hat mindestens einen Antrieb, ein "
                    "Hybrid hat zwei",
        ("P", "D"): "Mitarbeiter: Verwaltungskraft oder Werkstudent oder "
                    "keines von beiden",
        ("P", "N"): "Kunde: Newsletterbezieher, Beschwerdeführer, beides "
                    "oder keines",
    }
