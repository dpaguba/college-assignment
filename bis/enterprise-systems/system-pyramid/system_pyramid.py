"""Die Pyramide der Anwendungssysteme nach organisatorischen Ebenen."""

LEVELS = ("operativ", "Management", "strategisch")

TYPES = {
    "operativ": {
        "level": "operativ",
        "input": "Transaktionen, Ereignisse",
        "processing": "Sortieren, Listen erstellen, Zusammenführen, "
                      "Aktualisieren",
        "output": "Detaillierte Berichte, Listen, Übersichten",
        "users": "Mitarbeiter der operativen Ebene, Gruppenleiter"},
    "MIS": {
        "level": "Management",
        "input": "Zusammenfassende Transaktionsdaten, einfache Modelle",
        "processing": "Standardberichte, einfache Modelle, einfache "
                      "Analysen",
        "output": "Zusammenfassungen und Berichte über Ausnahmefälle",
        "users": "Mittleres Management"},
    "DSS": {
        "level": "Management",
        "input": "Geringe Datenmengen oder für die Datenanalyse "
                 "optimierte Datenbanken, analytische Modelle",
        "processing": "Interaktive Bearbeitung, Simulationen, Analyse",
        "output": "Spezialberichte, Entscheidungsanalysen, Antworten auf "
                  "Abfragen",
        "users": "Fachexperten, Personalleiter"},
    "ESS": {
        "level": "strategisch",
        "input": "Aggregierte Daten aus externen und internen Quellen",
        "processing": "Grafiken, Simulationen, interaktive Bearbeitung",
        "output": "Vorhersagen, Antworten auf Abfragen",
        "users": "Topmanagement"},
}

EXAMPLES = {
    "Lohnbuchhaltung": "operativ",
    "Auftragsbearbeitung": "operativ",
    "Personalverwaltung": "operativ",
    "Jährliche Budgetplanung": "MIS",
    "Rentabilitätsanalyse": "MIS",
    "Vertriebsbereichsanalyse": "DSS",
    "Produktionsplanung": "DSS",
    "5-Jahres-Umsatztrend": "ESS",
    "5-Jahres-Geschäftsplan": "ESS",
    "Gewinnplanung": "ESS",
}


def levels():
    """Nennt die drei organisatorischen Ebenen von unten nach oben."""
    return list(LEVELS)


def describe(kind):
    """Beschreibt einen Systemtyp nach Eingabe, Aufbereitung und Ausgabe.

    Raises:
        ValueError: bei einem unbekannten Typ.
    """
    if kind not in TYPES:
        raise ValueError("unbekannter Systemtyp")
    return dict(TYPES[kind])


def classify(application):
    """Ordnet eine Anwendung einem Systemtyp zu.

    Raises:
        ValueError: bei einer unbekannten Anwendung.
    """
    if application not in EXAMPLES:
        raise ValueError("unbekannte Anwendung")
    return EXAMPLES[application]


def functional_areas():
    """Nennt die Funktionsbereiche, die quer zur Pyramide liegen.

    Die Pyramide hat zwei Achsen: die Ebene sagt, wer das System benutzt,
    der Funktionsbereich, worum es geht. Ein Bericht über Personalkosten
    liegt bei Personalwesen und Managementebene zugleich.
    """
    return ["Vertrieb und Marketing", "Produktion",
            "Finanz- und Rechnungswesen", "Personalwesen"]


def what_moves_upward():
    """Sagt, was sich beim Aufstieg in der Pyramide ändert.

    Nach oben werden die Daten weniger und gröber, die Fragen offener und
    die Antworten unsicherer. Ein operatives System weiss genau, welche
    Rechnung offen ist; ein System für die Führungsebene schätzt, wie sich
    der Umsatz in fünf Jahren entwickelt.
    """
    return {"data": "weniger, aggregierter, auch von aussen",
            "questions": "offener, weniger vorhersehbar",
            "answers": "unsicherer",
            "frequency": "vom Minutentakt zum Quartal",
            "consequence": "nach oben zählt Übersicht, unten Genauigkeit"}
