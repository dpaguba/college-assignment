"""Der Produktlebenszyklus und das Portfolio."""

PHASES = ("Einführung", "Wachstum", "Reife", "Sättigung", "Degeneration")

FEATURES = {
    "Einführung": {"sales": "gering, steigend", "profit": "negativ",
                   "competitors": "keine bis wenige",
                   "focus": "Bekanntheit schaffen"},
    "Wachstum": {"sales": "stark steigend", "profit": "steigend",
                 "competitors": "kommen dazu",
                 "focus": "Marktanteil sichern"},
    "Reife": {"sales": "steigend, langsamer", "profit": "am höchsten",
              "competitors": "viele",
              "focus": "Differenzierung"},
    "Sättigung": {"sales": "Maximum erreicht", "profit": "fallend",
                  "competitors": "Verdrängung beginnt",
                  "focus": "Kosten und Bindung"},
    "Degeneration": {"sales": "fallend", "profit": "fallend bis negativ",
                     "competitors": "ziehen sich zurück",
                     "focus": "auslaufen lassen oder erneuern"},
}


def phases():
    """Nennt die Phasen in ihrer Reihenfolge."""
    return list(PHASES)


def describe(phase):
    """Beschreibt eine Phase.

    Raises:
        ValueError: bei einer unbekannten Phase.
    """
    if phase not in FEATURES:
        raise ValueError("unbekannte Phase")
    return dict(FEATURES[phase])


def phase_of(growth, share_of_peak):
    """Ordnet ein Produkt einer Phase zu.

    Args:
        growth: das Absatzwachstum als Anteil.
        share_of_peak: der Absatz im Verhältnis zum bisherigen Höchstwert.

    Returns:
        Die Phase.

    Raises:
        ValueError: bei einem Anteil ausserhalb von null bis eins.
    """
    if not 0 <= share_of_peak <= 1:
        raise ValueError("Anteil ausserhalb von 0 bis 1")
    if growth < -0.05:
        return "Degeneration"
    if growth > 0.2:
        return "Einführung" if share_of_peak < 0.3 else "Wachstum"
    if growth > 0.02:
        return "Reife"
    return "Sättigung"


def portfolio(share, growth, high_growth=0.1, high_share=1.0):
    """Ordnet ein Produkt in die vier Felder der Portfoliomatrix.

    Die Achsen sind der relative Marktanteil, also der eigene geteilt
    durch den des grössten Wettbewerbers, und das Marktwachstum. Der
    relative Anteil und nicht der absolute, weil es darauf ankommt, ob
    man vorn liegt, und nicht darauf, wie gross der Markt ist.

    Raises:
        ValueError: bei einem negativen relativen Anteil.
    """
    if share < 0:
        raise ValueError("negativer relativer Marktanteil")
    if growth >= high_growth:
        return "Star" if share >= high_share else "Fragezeichen"
    return "Melkkuh" if share >= high_share else "Armer Hund"


def cash_flow_logic():
    """Erklärt, wozu die Felder gut sind.

    Die Matrix ist ein Modell über Geldströme. Melkkühe erwirtschaften
    mehr, als sie brauchen, weil der Markt nicht mehr wächst und keine
    Investition verlangt. Stars brauchen ihr Geld selbst, um mit dem
    Markt mitzuwachsen. Fragezeichen brauchen Geld und liefern keines,
    und über sie muss entschieden werden. Arme Hunde binden Geld ohne
    Aussicht.

    Der Sinn ist die Umleitung: von den Melkkühen zu den Fragezeichen,
    aus denen Stars werden sollen, aus denen später Melkkühe werden.
    """
    return {"Melkkuh": "liefert Geld, braucht keines",
            "Star": "braucht sein Geld selbst",
            "Fragezeichen": "braucht Geld, liefert keines, muss "
                            "entschieden werden",
            "Armer Hund": "bindet Geld ohne Aussicht",
            "the flow": "von den Melkkühen zu den Fragezeichen"}


def what_the_curve_hides():
    """Nennt, warum der Zyklus schlecht als Prognose taugt.

    Die Phase lässt sich erst im Rückblick sicher benennen: ein Rückgang
    kann Sättigung sein oder eine Delle. Wer ihn als Sättigung liest und
    die Werbung einstellt, erzeugt die Sättigung, die er gemessen hat.
    Der Zyklus beschreibt gut und sagt schlecht voraus, und er ist
    zudem keine Naturkonstante, sondern das Ergebnis der Massnahmen, die
    ergriffen wurden.
    """
    return {"good at": "beschreiben, im Rückblick",
            "bad at": "vorhersagen",
            "self fulfilling": "wer die Sättigung annimmt und aufhört zu "
                               "investieren, erzeugt sie",
            "not a law": "die Kurve ist das Ergebnis der Massnahmen"}
