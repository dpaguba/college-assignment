"""Die Prozesslandkarte auf Ebene eins und das APQC-Rahmenwerk."""

RULE_OF_THUMB = 20

APQC_NAMES = {1: "Kategorie", 2: "Prozessgruppe", 3: "Prozess",
              4: "Aktivität"}


def check(processes, parties=None):
    """Prüft eine Landkarte gegen die drei Anforderungen.

    Die Landkarte muss für alle Beteiligten verständlich sein, vollständig
    (jede Partei muss ihre Tätigkeit wiederfinden) und kompakt. Die
    Faustregel setzt die Grenze bei zwanzig Geschäftsprozessen; darüber
    hinaus liest sie niemand mehr als Überblick.

    Args:
        processes: die Prozesse auf Ebene eins.
        parties: Abbildung von der Partei auf den Prozess, in dem sie sich
            wiederfinden soll.

    Returns:
        Abbildung mit ``compact``, ``complete``, ``missing`` und ``count``.

    Raises:
        ValueError: bei einer leeren Landkarte.
    """
    if not processes:
        raise ValueError("leere Landkarte")
    known = set(processes)
    missing = sorted(party for party, process in (parties or {}).items()
                     if process not in known)
    return {"count": len(processes),
            "compact": len(processes) <= RULE_OF_THUMB,
            "complete": not missing,
            "missing": missing,
            "rule of thumb": RULE_OF_THUMB}


def apqc_level(identifier):
    """Liest die Ebene aus einer APQC-Nummer.

    Die Notation zählt die Stellen: 1.0 ist eine Kategorie, 1.1 eine
    Prozessgruppe, 1.1.1 ein Prozess, 1.1.1.1 eine Aktivität.

    Raises:
        ValueError: wenn die Nummer nicht aus Zahlen mit Punkten besteht.
    """
    parts = str(identifier).split(".")
    if not all(part.isdigit() for part in parts) or len(parts) < 2:
        raise ValueError("keine gültige APQC-Nummer")
    if len(parts) == 2 and parts[1] == "0":
        return 1
    return len(parts)


def apqc_name(level):
    """Nennt den Namen einer Ebene.

    Raises:
        ValueError: bei einer Ebene ausserhalb von eins bis vier.
    """
    if level not in APQC_NAMES:
        raise ValueError("Ebene liegt ausserhalb von 1 bis 4")
    return APQC_NAMES[level]


def levels_of_an_architecture():
    """Beschreibt den Aufbau in drei Ebenen.

    Ebene eins ist die Wertschöpfungskette, Ebene zwei zerlegt sie in
    Prozesse, Ebene drei in Subprozesse und Aktivitäten. Eine vierte Ebene
    für die Aktivitäten ist möglich, aber nur dort sinnvoll, wo sie auch
    gepflegt wird.
    """
    return {1: "Wertschöpfungskette", 2: "Zerlegung in Prozesse",
            3: "Zerlegung in Subprozesse und Aktivitäten",
            "problem": "die Ableitung ist teilweise sehr komplex",
            "remedy": "Referenzmodelle"}


def reference_models():
    """Nennt, was Referenzmodelle leisten.

    Sie kommen von Konsortien, Forschungsprogrammen, Hochschulen oder
    Vereinen, dienen als Grundlage der eigenen Architektur und
    standardisieren die Abgrenzung der Prozesse, die Quantifizierung des
    Nutzens und die Benennung.
    """
    return {"examples": ["APQC", "SCOR", "eTOM", "ITIL"],
            "standardises": ["die Abgrenzung der Prozesse",
                             "die Quantifizierung des Nutzens",
                             "das Wording"],
            "comparison with competitors": True,
            "per industry": True}


def landscape_example():
    """Die Landkarte der Wiener Linien aus der Vorlesung.

    Returns:
        Abbildung von der Kategorie auf die Prozesse.
    """
    return {
        "management": ["Unternehmen steuern",
                       "Extern und intern kommunizieren",
                       "Prozesse und Projekte managen", "Qualität managen",
                       "Chancen und Gefahren managen",
                       "Innovationen managen"],
        "core": ["Kundenbeziehung managen", "Betriebsmittel betreiben",
                 "Fahrgäste befördern", "Infrastruktur bereitstellen"],
        "support": ["Personal managen", "Finanzen verwalten",
                    "Information und Kommunikation managen",
                    "Beschaffung durchführen",
                    "Störungsmanagement durchführen",
                    "Winterdienst betreiben"],
    }
