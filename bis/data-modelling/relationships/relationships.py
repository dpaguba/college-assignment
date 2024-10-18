"""Relationen und die (min,max)-Notation."""


def relation(name, between, cardinalities):
    """Beschreibt eine Relation zwischen Entitätstypen.

    Eine Relation verbindet mindestens zwei Entitätstypen und wird nach
    einem Substantiv benannt: ``Besuch``, nicht ``hört``. Ein Verb legt
    eine Leserichtung fest, die es in der Relation nicht gibt.

    Args:
        name: der Name der Relation.
        between: die beteiligten Entitätstypen.
        cardinalities: je Beteiligtem ein Paar aus Minimum und Maximum.

    Returns:
        Abbildung mit den Angaben und der Darstellung.

    Raises:
        ValueError: bei weniger als zwei Beteiligten oder wenn die Zahl
            der Kardinalitäten nicht passt.
    """
    if len(between) < 2:
        raise ValueError("eine Relation verbindet mindestens zwei Typen")
    if len(cardinalities) != len(between):
        raise ValueError("je Beteiligtem eine Kardinalität")
    return {"name": name, "between": list(between),
            "cardinalities": list(cardinalities), "shape": "Raute",
            "named after": "ein Substantiv"}


def read(notation):
    """Liest ein (min,max)-Paar.

    Das Minimum sagt, wie oft eine Entität die Beziehung eingehen
    **muss**, das Maximum, wie oft sie sie eingehen **kann**. Ein n steht
    für beliebig viele.

    Raises:
        ValueError: bei einer Angabe, die nicht der Notation folgt.
    """
    text = str(notation).strip()
    if not (text.startswith("(") and text.endswith(")") and "," in text):
        raise ValueError("keine (min,max)-Notation")
    low, high = (part.strip() for part in text[1:-1].split(",", 1))
    if not low.isdigit():
        raise ValueError("das Minimum muss eine Zahl sein")
    if high != "n" and not high.isdigit():
        raise ValueError("das Maximum muss eine Zahl oder n sein")
    return {"minimum": int(low),
            "maximum": "n" if high == "n" else int(high),
            "notation": text}


def mandatory(notation):
    """Sagt, ob die Teilnahme an der Beziehung Pflicht ist.

    Raises:
        ValueError: bei einer fehlerhaften Notation.
    """
    return read(notation)["minimum"] > 0


def kind(first, second):
    """Bestimmt aus zwei Kardinalitäten die Art der Beziehung.

    Raises:
        ValueError: bei einer fehlerhaften Notation.
    """
    left = read(first)["maximum"]
    right = read(second)["maximum"]
    many = {"left": left == "n" or left > 1, "right": right == "n"
            or right > 1}
    if many["left"] and many["right"]:
        return "n:m"
    if not many["left"] and not many["right"]:
        return "1:1"
    return "1:n"


def recursive(entity, name, first, second):
    """Beschreibt eine Beziehung eines Typs mit sich selbst.

    Dargestellt wird sie durch parallele Kanten: beide Enden der Raute
    führen auf dasselbe Rechteck. Zwei Formen kommen häufig vor. Bei einer
    Hierarchie hat jede Entität höchstens eine über sich und beliebig
    viele unter sich; bei einem Netz sind beide Seiten unbeschränkt.

    Raises:
        ValueError: bei einer fehlerhaften Notation.
    """
    upper = read(first)["maximum"]
    lower = read(second)["maximum"]
    unbounded = {upper == "n", lower == "n"}
    if unbounded == {True}:
        shape = "network"
    elif True in unbounded:
        shape = "hierarchy"
    else:
        shape = "pairing"
    return {"entity": entity, "relation": name, "parallel edges": True,
            "cardinalities": [first, second], "shape": shape}


def why_not_a_fixed_number():
    """Sagt, warum im Maximum meist n und keine Zahl steht.

    Eine Zahl im Maximum ist eine Geschäftsregel und keine Eigenschaft der
    Daten. Wer dort fünf einträgt, weil heute niemand mehr als fünf
    Vorlesungen belegt, muss das Modell ändern, sobald jemand sechs
    belegt.
    """
    return {"n means": "no fixed upper bound in the model",
            "a number means": "a rule that has to hold for ever",
            "advice": "only write a number when the rule is enforced"}
