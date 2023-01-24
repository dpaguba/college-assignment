"""Revenue Management: feste Kapazität, verderbliches Gut, zwei Klassen."""

DEMAND = {0: 0.05, 10: 0.10, 20: 0.20, 30: 0.30, 40: 0.20, 50: 0.15}


def conditions():
    """Nennt die Bedingungen, unter denen das Verfahren passt.

    Feste Kapazität, die kurzfristig nicht zu ändern ist; ein Gut, das
    verfällt, wenn es nicht verkauft wird; Kunden mit sehr verschiedener
    Zahlungsbereitschaft; und die Möglichkeit, im Voraus zu verkaufen.
    Der Flugplatz erfüllt alle vier, ein Regal im Supermarkt keine.
    """
    return ["feste Kapazität",
            "das Gut verfällt zum Abflug",
            "sehr verschiedene Zahlungsbereitschaften",
            "Verkauf im Voraus möglich",
            "die variablen Kosten je Sitz sind fast null"]


def survival(protected, demand=None):
    """Die Wahrscheinlichkeit einer mindestens so grossen Nachfrage.

    Gefragt wird ``P(D ≥ y)`` und nicht ``P(D > y)``: der y-te
    zurückgehaltene Platz wird genau dann verkauft, wenn die Nachfrage
    mindestens y beträgt. Mit dem echten Grösserzeichen ergibt die Regel
    eine Schutzmenge zu wenig, und bei einer Verteilung mit Sprüngen ist
    das eine ganze Stufe.

    Raises:
        ValueError: bei einer negativen Schutzmenge.
    """
    if protected < 0:
        raise ValueError("negative Schutzmenge")
    demand = DEMAND if demand is None else demand
    return sum(weight for value, weight in demand.items()
               if value >= protected)


def littlewood(high, low, demand=None):
    """Die Schutzmenge nach der Regel von Littlewood.

    Ein Platz wird für die teure Klasse zurückgehalten, solange die
    erwartete Einnahme daraus über dem sicheren billigen Erlös liegt, also
    solange ``P(D_hoch > y)·h ≥ l``. Die Regel vergleicht damit einen
    sicheren kleinen Erlös mit einem unsicheren grossen, und die
    Schutzmenge ist die grösste Zahl, bei der der Vergleich noch für die
    teure Klasse ausgeht.

    Args:
        high: der Erlös der teuren Klasse.
        low: der Erlös der billigen.
        demand: die Verteilung der teuren Nachfrage.

    Returns:
        Die Schutzmenge.

    Raises:
        ValueError: wenn der billige Erlös nicht unter dem teuren liegt.
    """
    if not 0 < low < high:
        raise ValueError("der billige Erlös muss zwischen null und dem "
                         "teuren liegen")
    demand = DEMAND if demand is None else demand
    ratio = low / high
    best = 0
    for level in sorted(demand):
        if level > 0 and survival(level, demand) >= ratio:
            best = level
    return best


def expected_revenue(protected, capacity, high, low, demand=None,
                     low_demand=None):
    """Der erwartete Erlös bei einer Schutzmenge.

    Die billige Nachfrage wird als gross genug angenommen, um die
    freigegebenen Plätze zu füllen; das ist der Fall, für den die Regel
    gemacht ist.

    Raises:
        ValueError: bei einer unzulässigen Schutzmenge.
    """
    if not 0 <= protected <= capacity:
        raise ValueError("die Schutzmenge passt nicht zur Kapazität")
    demand = DEMAND if demand is None else demand
    low_demand = capacity if low_demand is None else low_demand
    sold_low = min(capacity - protected, low_demand)
    total = 0.0
    for value, weight in demand.items():
        sold_high = min(value, capacity - sold_low)
        total += weight * (sold_high * high + sold_low * low)
    return total


def best_protection(capacity, high, low, demand=None):
    """Sucht die beste Schutzmenge durch Ausprobieren.

    Das ist die Gegenrechnung zur Regel: alle Schutzmengen werden
    durchgerechnet und die beste genommen. Stimmt sie mit der Regel
    überein, so ist die Regel bestätigt und nicht nur zitiert.

    Raises:
        ValueError: bei einer nicht positiven Kapazität.
    """
    if capacity < 1:
        raise ValueError("die Kapazität muss positiv sein")
    demand = DEMAND if demand is None else demand
    best = None
    for protected in range(capacity + 1):
        value = expected_revenue(protected, capacity, high, low, demand)
        if best is None or value > best[1]:
            best = (protected, value)
    return {"protection": best[0], "revenue": best[1]}


def the_rule_agrees(capacity=60, high=400.0, low=150.0, demand=None):
    """Vergleicht die Regel mit der Suche.

    Returns:
        Abbildung mit beiden Schutzmengen.
    """
    demand = DEMAND if demand is None else demand
    rule = littlewood(high, low, demand)
    search = best_protection(capacity, high, low, demand)
    return {"by the rule": rule, "by search": search["protection"],
            "revenue at the rule": expected_revenue(rule, capacity, high,
                                                    low, demand),
            "best revenue": search["revenue"],
            "agree": abs(expected_revenue(rule, capacity, high, low, demand)
                         - search["revenue"]) < 1e-9}


def the_ratio_decides(high=400.0, demand=None):
    """Zeigt, wie die Schutzmenge vom Preisverhältnis abhängt.

    Je näher der billige Preis am teuren liegt, desto weniger wird
    zurückgehalten: der sichere Erlös wird attraktiver. Fällt der billige
    Preis, steigt die Schutzmenge. Die absoluten Preise spielen keine
    Rolle, nur ihr Verhältnis.

    Returns:
        Abbildung vom Verhältnis auf die Schutzmenge.
    """
    demand = DEMAND if demand is None else demand
    return {round(share, 2): littlewood(high, high * share, demand)
            for share in (0.2, 0.4, 0.6, 0.8)}


def what_it_costs_the_customer():
    """Nennt die Kehrseite, die in der Vorlesung mitkommt.

    Das Verfahren schöpft Zahlungsbereitschaft ab, und die Kunden merken
    es. Wer neben jemandem sitzt, der die Hälfte gezahlt hat, empfindet
    den eigenen Preis als Strafe, nicht als Marktergebnis. Die
    Branchen, in denen es funktioniert, haben deshalb entweder eine
    Erklärung dafür (wer früh bucht, zahlt weniger) oder gar keine
    Wahl für den Kunden.
    """
    return {"works because": "der Preis ist an eine Regel gebunden, die "
                             "der Kunde beeinflussen kann",
            "fails when": "die Regel als willkürlich empfunden wird",
            "the seat next to you": "derselbe Platz, halber Preis",
            "consequence": "die Erklärung ist Teil des Verfahrens"}
