"""Die Bewertungsgrundsätze und ihr Zusammenspiel."""

PRINCIPLES = {
    "Anschaffungskostenprinzip": "die Anschaffungs- oder "
                                 "Herstellungskosten sind die Obergrenze",
    "Realisationsprinzip": "ein Gewinn wird erst mit dem Umsatzakt "
                          "ausgewiesen",
    "Imparitätsprinzip": "ein drohender Verlust wird vorher ausgewiesen",
    "Vorsichtsprinzip": "im Zweifel die ungünstigere Annahme",
    "Einzelbewertung": "jeder Gegenstand für sich",
    "Stichtagsprinzip": "massgeblich ist der Zustand am Bilanzstichtag",
}


def principles():
    """Nennt die Grundsätze der Bewertung."""
    return dict(PRINCIPLES)


def realise(cost, market, sold):
    """Zeigt, wann ein Gewinn ausgewiesen wird.

    Solange nicht verkauft ist, bleibt der Ansatz bei den
    Anschaffungskosten, auch wenn der Marktwert darüber liegt. Erst der
    Umsatzakt macht aus der Wertsteigerung einen Gewinn. Der Verlust
    dagegen wird schon vorher gezeigt, und diese Ungleichbehandlung ist
    gewollt.

    Raises:
        ValueError: bei negativen Werten.
    """
    if cost < 0 or market < 0:
        raise ValueError("negative Werte")
    if sold:
        return {"value": market, "result": market - cost,
                "why": "der Umsatzakt hat stattgefunden"}
    return {"value": min(cost, market),
            "result": min(0.0, market - cost),
            "why": "ohne Umsatzakt wird nur der Verlust gezeigt"}


def stichtag(value_at_closing, value_when_signed):
    """Zeigt, welcher Zeitpunkt zählt.

    Massgeblich ist der Stichtag. Was zwischen Stichtag und Aufstellung
    bekannt wird, ist zu berücksichtigen, wenn es die Verhältnisse **am
    Stichtag** erhellt, und nicht, wenn es ein neues Ereignis ist. Die
    Unterscheidung heisst werterhellend gegen wertbegründend und ist im
    Einzelfall die schwierigste Frage der ganzen Bewertung.

    Raises:
        ValueError: bei negativen Werten.
    """
    if value_at_closing < 0 or value_when_signed < 0:
        raise ValueError("negative Werte")
    return {"value": value_at_closing,
            "later value": value_when_signed,
            "werterhellend": "erhellt die Lage am Stichtag, wird "
                             "berücksichtigt",
            "wertbegründend": "ein neues Ereignis danach, wird nicht "
                              "berücksichtigt",
            "example": "eine Insolvenz des Kunden im Januar erhellt seine "
                       "Lage im Dezember; ein Brand im Januar tut es nicht"}


def individual_valuation(items, together=False):
    """Vergleicht Einzelbewertung und Gesamtbetrachtung.

    Einzeln bewertet wird jeder Posten für sich auf den niedrigeren
    Wert gesetzt; zusammen betrachtet dürften Verluste des einen mit
    Gewinnen des anderen verrechnet werden. Das Handelsrecht verlangt
    die Einzelbewertung, und deshalb ist der Ansatz strenger als die
    wirtschaftliche Lage.

    Args:
        items: Paare aus Anschaffungskosten und Marktwert.
        together: ob saldiert werden darf.

    Returns:
        Abbildung mit beiden Ergebnissen.

    Raises:
        ValueError: bei einer leeren Liste.
    """
    if not items:
        raise ValueError("keine Posten")
    single = sum(min(cost, market) for cost, market in items)
    combined = min(sum(cost for cost, _ in items),
                   sum(market for _, market in items))
    return {"item by item": single, "in total": combined,
            "difference": combined - single,
            "which applies": "in total" if together else "item by item",
            "why the difference": "einzeln zählt jeder Verlust, "
                                  "zusammen heben sich Verluste und "
                                  "Gewinne teilweise auf"}


def how_they_fit_together():
    """Ordnet die Grundsätze in eine Reihenfolge.

    Über allem steht die Vorsicht. Aus ihr folgen das Realisationsprinzip
    für die Gewinne und das Imparitätsprinzip für die Verluste; beide
    zusammen ergeben die Ungleichbehandlung. Das
    Anschaffungskostenprinzip zieht die Obergrenze, die Einzelbewertung
    verbietet das Verrechnen, und das Stichtagsprinzip legt den Zeitpunkt
    fest. Jeder einzelne Grundsatz wirkt in dieselbe Richtung: das
    ausgewiesene Vermögen ist eher zu klein.
    """
    return {"above all": "Vorsicht",
            "for gains": "Realisationsprinzip",
            "for losses": "Imparitätsprinzip",
            "upper limit": "Anschaffungskostenprinzip",
            "no netting": "Einzelbewertung",
            "the date": "Stichtagsprinzip",
            "all point the same way": "das Vermögen wird eher zu klein "
                                      "gezeigt"}
