"""Entscheidungen gegen den Würfel."""

from itertools import product

WAYS = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2,
        12: 1}


def value(tree, node, tolerance=1e-9):
    """Rechnet den Wert eines Knotens aus.

    Ein Blatt trägt seinen Wert, ein Entscheidungsknoten nimmt das
    Beste seiner Kinder, und ein Zufallsknoten mittelt sie mit ihren
    Wahrscheinlichkeiten. Der Unterschied zum Minimax ist genau dieser
    dritte Fall: gegen den Würfel gibt es nichts zu maximieren, nur zu
    mitteln.

    Raises:
        ValueError: bei einem unbekannten Knoten, einer unbekannten Art
            oder Wahrscheinlichkeiten, die nicht auf eins summieren.
    """
    if node not in tree:
        raise ValueError("unbekannter Knoten: %s" % node)
    row = tree[node]
    kind = row.get("kind")
    if kind == "leaf":
        return float(row["value"])
    if kind == "max":
        return max(value(tree, child, tolerance)
                   for child in row["children"])
    if kind == "chance":
        total = sum(chance for _, chance in row["children"])
        if abs(total - 1.0) > tolerance:
            raise ValueError("die Wahrscheinlichkeiten summieren nicht "
                             "auf eins")
        return sum(chance * value(tree, child, tolerance)
                   for child, chance in row["children"])
    raise ValueError("unbekannte Art: %s" % kind)


def best_policy(tree, node):
    """Prüft den Wert gegen alle festen Entscheidungsregeln.

    Der Wert eines Baums mit Entscheidungs- und Zufallsknoten ist der
    grösste Erwartungswert über alle festen Regeln, die an jedem
    Entscheidungsknoten ein Kind wählen. Diese Rechnung zählt alle
    Regeln auf und ist damit unabhängig von der Rekursion oben.

    Returns:
        Abbildung mit dem besten Wert und allen Regeln.

    Raises:
        ValueError: wie bei ``value``.
    """
    choices = sorted(name for name, row in tree.items()
                     if row.get("kind") == "max")
    options = [tree[name]["children"] for name in choices]
    found = []
    for taken in product(*options) if options else [()]:
        policy = dict(zip(choices, taken))
        found.append({"policy": policy,
                      "value": _under(tree, node, policy)})
    best = max(found, key=lambda row: row["value"])
    return {"value": best["value"], "policy": best["policy"],
            "policies tried": len(found), "all": found}


def _under(tree, node, policy):
    """Rechnet den Erwartungswert unter einer festen Regel aus.

    Raises:
        ValueError: bei einer unbekannten Art von Knoten.
    """
    row = tree[node]
    kind = row.get("kind")
    if kind == "leaf":
        return float(row["value"])
    if kind == "max":
        return _under(tree, policy[node], policy)
    if kind == "chance":
        return sum(chance * _under(tree, child, policy)
                   for child, chance in row["children"])
    raise ValueError("unbekannte Art: %s" % kind)


def dice_tree():
    """Baut einen kleinen Baum mit einem Zug und einem Wurf.

    Gewählt wird zwischen zwei Kreuzungen, danach fällt der Würfel. Die
    eine Kreuzung liegt an einer Sechs und einer Acht, die andere an
    einer Zwei und einer Zwölf mit einem höheren Ertrag je Treffer.

    Returns:
        Der Baum.
    """
    tree = {"root": {"kind": "max", "children": ["sechs und acht",
                                                 "zwei und zwölf"]}}
    for name, tokens, payoff in (("sechs und acht", (6, 8), 1.0),
                                 ("zwei und zwölf", (2, 12), 4.0)):
        children = []
        for number in range(2, 13):
            leaf = "%s:%d" % (name, number)
            children.append((leaf, WAYS[number] / 36.0))
            tree[leaf] = {"kind": "leaf",
                          "value": payoff * tokens.count(number)}
        tree[name] = {"kind": "chance", "children": children}
    return tree


def the_average_is_not_the_best_case():
    """Vergleicht die Wahl nach dem Mittel mit der nach dem besten Fall.

    Die Kreuzung an der Sechs und der Acht liefert im Mittel zehn
    Sechsunddreissigstel einer Karte je Wurf. Die an der Zwei und der
    Zwölf liefert selten, dafür vier Karten auf einmal, also im Mittel
    acht Sechsunddreissigstel. Nach dem Erwartungswert gewinnt die
    erste, nach dem besten Fall die zweite.

    Wer nach dem besten Fall entscheidet, spielt auf die Zwölf und
    wartet im Schnitt sechsunddreissig Würfe darauf. Genau das ist der
    Fehler, den eine Bewertungsfunktion ohne Wahrscheinlichkeiten macht.

    Returns:
        Abbildung mit beiden Entscheidungen.
    """
    tree = dice_tree()
    scored = {}
    for name in tree["root"]["children"]:
        outcomes = [tree[child]["value"]
                    for child, _ in tree[name]["children"]]
        scored[name] = {"expectation": value(tree, name),
                        "best case": max(outcomes),
                        "worst case": min(outcomes)}
    by_mean = max(scored, key=lambda name: scored[name]["expectation"])
    by_best = max(scored, key=lambda name: scored[name]["best case"])
    return {"scored": scored, "move by expectation": by_mean,
            "move by best case": by_best,
            "expectimax": value(tree, "root"),
            "best case": max(row["best case"] for row in scored.values()),
            "worst case": min(row["worst case"]
                              for row in scored.values()),
            "what it costs": "wer auf die Zwölf spielt, wartet im "
                             "Schnitt sechsunddreissig Würfe"}


def the_seven_belongs_in_the_tree(hand=9):
    """Zeigt, was das Weglassen der Sieben kostet.

    Die Sieben liefert keinem Feld etwas und ist deshalb leicht zu
    übersehen. Sie ist aber der häufigste Wurf und kostet jeden mit mehr
    als sieben Karten die Hälfte davon. Ein Baum ohne diesen Ast
    bewertet das Sammeln systematisch zu gut.

    Args:
        hand: die Zahl der Handkarten vor dem Wurf.

    Returns:
        Abbildung mit dem Wert mit und ohne den Ast.

    Raises:
        ValueError: bei einer negativen Handkartenzahl.
    """
    if hand < 0:
        raise ValueError("negative Handkartenzahl")
    loss = 0 if hand <= 7 else hand // 2
    without = {"root": {"kind": "chance", "children": []}}
    with_seven = {"root": {"kind": "chance", "children": []}}
    outside = sum(WAYS[number] for number in WAYS if number != 7)
    for number in WAYS:
        leaf = "roll %d" % number
        gain = 1.0 if number in (6, 8) else 0.0
        with_seven[leaf] = {"kind": "leaf",
                            "value": gain - (loss if number == 7 else 0)}
        with_seven["root"]["children"].append((leaf, WAYS[number] / 36.0))
        if number != 7:
            without[leaf] = {"kind": "leaf", "value": gain}
            without["root"]["children"].append((leaf,
                                                WAYS[number] / outside))
    return {"with the seven": value(with_seven, "root"),
            "without the seven": value(without, "root"),
            "hand": hand, "cards lost on a seven": loss,
            "why it is missed": "die Sieben liefert keinem Feld etwas "
                                "und fällt deshalb aus der Rechnung"}
