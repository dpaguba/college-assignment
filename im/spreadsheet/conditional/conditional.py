"""Die WENN-Funktion, Wahrheitswerte und Verschachtelung."""

GIFTS = ("Postkarte", "Blumenstrauss", "nichts")


def wenn(condition, then_value, else_value):
    """Bildet die WENN-Funktion nach.

    Sie wertet beide Zweige nicht aus, sondern wählt einen Wert; das ist
    der Unterschied zu einer Rechnung, in der beide Seiten schon
    dastehen. In einer Tabellenkalkulation fällt er selten auf, weil dort
    keine Nebenwirkungen möglich sind.
    """
    return then_value if condition else else_value


def und(*conditions):
    """Bildet UND über beliebig viele Bedingungen ab.

    Raises:
        ValueError: ohne Bedingung.
    """
    if not conditions:
        raise ValueError("mindestens eine Bedingung")
    return all(bool(value) for value in conditions)


def oder(*conditions):
    """Bildet ODER über beliebig viele Bedingungen ab.

    Raises:
        ValueError: ohne Bedingung.
    """
    if not conditions:
        raise ValueError("mindestens eine Bedingung")
    return any(bool(value) for value in conditions)


def jubilee_gift(customer_since, purchases, today=2018,
                 purchases_this_year=None):
    """Entscheidet über das Geschenk, Aufgabe 4 des neunten Tutoriums.

    Die Aufgabe nennt zwei Regeln. Eine Postkarte bekommt, wer erst seit
    2014 oder später Kunde ist **und** bisher nicht mehr als fünf Käufe
    getätigt hat. Einen Blumenstrauss bekommt, wer länger als vier Jahre
    Kunde ist **oder** mehr als fünf Käufe in diesem Jahr getätigt hat.

    Args:
        customer_since: das Jahr der Erfassung.
        purchases: die Käufe, auf die sich die Postkartenregel bezieht.
        today: das laufende Jahr.
        purchases_this_year: die Käufe des laufenden Jahres, falls sie
            von der ersten Zahl abweichen; ohne Angabe dieselbe Zahl.

    Returns:
        Abbildung mit dem Geschenk und den beiden Bedingungen.
    """
    recent = purchases if purchases_this_year is None else \
        purchases_this_year
    postcard = und(customer_since >= 2014, purchases <= 5)
    bouquet = oder(today - customer_since > 4, recent > 5)
    if postcard and bouquet:
        gift = "Blumenstrauss"
    elif postcard:
        gift = "Postkarte"
    elif bouquet:
        gift = "Blumenstrauss"
    else:
        gift = "nichts"
    return {"gift": gift, "postcard rule": postcard,
            "bouquet rule": bouquet,
            "both apply": postcard and bouquet,
            "neither applies": not postcard and not bouquet}


def readings(today=2018):
    """Vergleicht die beiden Lesarten der Aufgabe.

    Die Aufgabe sagt bei der Postkarte «bisher nicht mehr als fünf Käufe»
    und beim Blumenstrauss «mehr als fünf Käufe in diesem Jahr». Ob damit
    dieselbe Zahl gemeint ist, sagt sie nicht, und daran hängt alles.

    Ist es dieselbe Zahl, so sind die beiden Regeln exakte Gegenstücke:
    ``seit >= 2014 und Käufe <= 5`` und ihre Verneinung ``seit < 2014
    oder Käufe > 5``. Jeder Kunde fällt dann in genau eine Regel, es gibt
    weder Überschneidung noch Lücke, und die Fallunterscheidung im Code
    ist überflüssig.

    Sind es zwei verschiedene Zahlen, so zerfällt die saubere Teilung.
    Ein Kunde von 2016 mit drei Käufen insgesamt, davon sechs in diesem
    Jahr, ist unmöglich; ein Kunde von 2016 mit acht Käufen insgesamt und
    zweien in diesem Jahr erfüllt keine Regel und bekommt nichts.

    Returns:
        Abbildung mit beiden Lesarten und den Fällen, die sie trennen.
    """
    same = []
    for since in range(2008, 2019):
        for purchases in range(0, 12):
            report = jubilee_gift(since, purchases, today)
            same.append((report["both apply"], report["neither applies"]))
    partition = not any(both or neither for both, neither in same)
    gap = jubilee_gift(2016, 8, today, purchases_this_year=2)
    return {"one number": {"partitions exactly": partition,
                           "overlaps": 0, "gaps": 0,
                           "cases checked": len(same)},
            "two numbers": {"example": {"since": 2016, "total": 8,
                                        "this year": 2},
                            "gift": gap["gift"],
                            "postcard rule": gap["postcard rule"],
                            "bouquet rule": gap["bouquet rule"]},
            "what the sheet leaves open": "ob «bisher» und «in diesem "
                                          "Jahr» dieselbe Zahl meinen",
            "consequence": "bei einer Zahl ist die zweite Regel die "
                           "Verneinung der ersten, bei zwei Zahlen nicht"}


def nesting_depth(levels):
    """Nennt, wie viele Fälle eine geschachtelte WENN-Funktion trennt.

    Jede Ebene fügt einen Zweig hinzu, also trennt eine n-fach
    geschachtelte Funktion n plus einen Fall. Ab drei Ebenen wird die
    Formel unlesbar, und dann ist eine Verweistabelle die bessere Wahl.

    Raises:
        ValueError: bei einer negativen Zahl von Ebenen.
    """
    if levels < 0:
        raise ValueError("negative Verschachtelung")
    return {"levels": levels, "cases": levels + 1,
            "readable up to": 3,
            "beyond that": "eine Verweistabelle statt der Verschachtelung"}
