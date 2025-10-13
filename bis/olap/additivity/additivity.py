"""Additivität: welche Kennzahl über welche Dimension summiert werden darf."""

KINDS = ("additive", "semi additive", "non additive")

MEASURES = {
    "Risiko-Score": "additive",
    "Quartalsbudget": "semi additive",
    "Strategischer Fit": "semi additive",
    "Auslastung": "non additive",
    "Marge": "non additive",
    "Lagerbestand": "semi additive",
}

BUDGETS = (("P1 Kundenportal", "Q4", 220), ("P1 Kundenportal", "Q3", 250),
           ("P2 KI-Prognose", "Q4", 300), ("P2 KI-Prognose", "Q3", 340),
           ("P3 ERP-Migration", "Q4", 500), ("P3 ERP-Migration", "Q3", 520),
           ("P4 Neue Fassade", "Q4", 180), ("P5 IoT Produkt", "Q4", 600))

RISK_KINDS = 3


def kinds():
    """Nennt die drei Arten von Kennzahlen."""
    return list(KINDS)


def classify(measure):
    """Sagt, wie eine Kennzahl sich beim Summieren verhält.

    Additiv heisst: über jede Dimension summierbar. Semi-additiv heisst:
    über manche schon, über andere nicht; ein Lagerbestand darf über
    Artikel summiert werden, über die Zeit nicht. Nicht additiv heisst:
    über keine, weil die Kennzahl ein Verhältnis ist und Verhältnisse
    sich nicht addieren.

    Raises:
        ValueError: bei einer unbekannten Kennzahl.
    """
    if measure not in MEASURES:
        raise ValueError("unbekannte Kennzahl")
    return MEASURES[measure]


def budget_trap():
    """Rechnet die Falle vor, die in der Tabelle steckt.

    Das Quartalsbudget gehört zum Projekt und zum Quartal, nicht zur
    Risikoart. In der Tabelle steht es trotzdem in jeder der drei Zeilen
    eines Projektquartals, weil die Zeilen nach Risikoart aufgeteilt
    sind. Wer über alle Zeilen summiert, zählt jedes Budget dreimal.

    Returns:
        Abbildung mit beiden Summen, dem Faktor und der Regel.
    """
    distinct = sum(amount for _, _, amount in BUDGETS)
    over_rows = distinct * RISK_KINDS
    return {"sum over all rows": over_rows,
            "sum over distinct project quarters": distinct,
            "factor": RISK_KINDS,
            "why": "the budget belongs to the project quarter, not to the "
                   "kind of risk, and the table repeats it per row",
            "rule": "before summing, ask which dimension the measure "
                    "actually depends on"}


def safe_dimensions(measure):
    """Nennt die Dimensionen, über die eine Kennzahl summiert werden darf.

    Raises:
        ValueError: bei einer unbekannten Kennzahl.
    """
    kind = classify(measure)
    if kind == "additive":
        return ["Projekt", "Quartal", "Jahr", "Risikoart"]
    if kind == "non additive":
        return []
    if measure == "Quartalsbudget":
        return ["Projekt", "Quartal"]
    if measure == "Strategischer Fit":
        return []
    return ["Projekt"]


def how_to_notice():
    """Nennt die Probe, die eine falsche Summe auffliegen lässt.

    Wenn dieselbe Zahl in mehreren Zeilen wortgleich steht, gehört sie
    nicht auf die Ebene der Zeilen. Die Gegenprobe ist billig: einmal über
    alle Zeilen summieren, einmal über die unterschiedlichen Schlüssel,
    und die beiden Ergebnisse vergleichen.
    """
    return {"symptom": "the same value repeats across rows of a group",
            "test": "sum over rows against sum over distinct keys",
            "in this table": "8730 against 2910, a factor of three",
            "fix": "aggregate the measure at its own grain first"}
