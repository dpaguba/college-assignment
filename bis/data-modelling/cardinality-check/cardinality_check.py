"""Die Prüfung einer Ausprägung gegen die (min,max)-Angaben."""


def _read(notation):
    """Liest ein (min,max)-Paar.

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
    return int(low), (None if high == "n" else int(high))


def example():
    """Studierende besuchen Vorlesungen, beide Seiten (0,n).

    Returns:
        Abbildung mit beiden Seiten und den vorhandenen Verbindungen.
    """
    return {
        "left": {"entity": "Studierende", "members": ["s1", "s2", "s3"],
                 "cardinality": "(0,n)"},
        "right": {"entity": "Vorlesung", "members": ["v1", "v2"],
                  "cardinality": "(0,n)"},
        "links": [("s1", "v1"), ("s1", "v2"), ("s2", "v1")],
    }


def check(model):
    """Prüft, ob die Verbindungen die Kardinalitäten einhalten.

    Gezählt wird je Entität, an wie vielen Beziehungen sie teilnimmt. Wer
    unter dem Minimum liegt, fehlt; wer über dem Maximum liegt, ist zu
    oft verbunden. Beides ist im Diagramm nicht zu sehen und erst an den
    Daten zu merken.

    Args:
        model: Abbildung mit ``left``, ``right`` und ``links``.

    Returns:
        Abbildung mit den Verstössen und den Zählungen beider Seiten.

    Raises:
        ValueError: bei einer Verbindung auf eine unbekannte Entität oder
            einer fehlerhaften Notation.
    """
    left, right = model["left"], model["right"]
    counts = {"left": {name: 0 for name in left["members"]},
              "right": {name: 0 for name in right["members"]}}
    for first, second in model["links"]:
        if first not in counts["left"]:
            raise ValueError("unbekannte Entität links: %s" % first)
        if second not in counts["right"]:
            raise ValueError("unbekannte Entität rechts: %s" % second)
        counts["left"][first] += 1
        counts["right"][second] += 1
    violations = []
    for side, other in (("left", left), ("right", right)):
        low, high = _read(other["cardinality"])
        for name in sorted(counts[side]):
            found = counts[side][name]
            if found < low:
                violations.append("%s hat %d Beziehungen, mindestens %d "
                                  "verlangt" % (name, found, low))
            if high is not None and found > high:
                violations.append("%s hat %d Beziehungen, höchstens %d "
                                  "erlaubt" % (name, found, high))
    return {"violations": violations, "left counts": counts["left"],
            "right counts": counts["right"],
            "links": len(model["links"])}


def what_the_diagram_cannot_say():
    """Nennt, was zwischen Modell und Daten offen bleibt.

    Ein Diagramm sagt, was erlaubt ist, und nicht, was der Fall ist. Eine
    Datenbank, die zu einem korrekten Modell gehört, kann trotzdem Zeilen
    enthalten, die es verletzen: entweder weil die Regel nicht als
    Fremdschlüssel oder Prüfung umgesetzt wurde, oder weil die Daten aus
    einem Vorsystem übernommen wurden, das die Regel nicht kannte.
    """
    return {"model says": "what is allowed",
            "data says": "what is there",
            "gap appears when": ["die Regel ist nicht umgesetzt",
                                 "die Daten kommen aus einem Vorsystem"],
            "minimum is the hard one": "ein Maximum lässt sich als "
                                       "Fremdschlüssel erzwingen, ein "
                                       "Minimum nicht ohne Weiteres"}
