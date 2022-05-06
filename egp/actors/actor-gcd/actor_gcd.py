"""Der Algorithmus von Euklid mit Aktoren: Übungsblatt 3."""


def step(first, second):
    """Ein Schritt des Algorithmus.

    Ist der zweite Wert null, so ist der erste das Ergebnis. Sonst wird
    weitergerechnet mit dem zweiten Wert und dem Rest der Division.

    Raises:
        ValueError: bei einem negativen Wert.
    """
    if first < 0 or second < 0:
        raise ValueError("negativer Wert")
    if second == 0:
        return {"done": True, "result": first}
    return {"done": False, "next": (second, first % second)}


def run(first, second, limit=200):
    """Führt den Algorithmus als Folge von Nachrichten aus.

    Der Aktor schickt sich selbst eine Nachricht mit den nächsten
    Werten, bis der zweite null ist; dann schickt er das Ergebnis an die
    Adresse, die in der Nachricht stand. Genau das ist die Umsetzung mit
    Aktoren: keine Schleife, sondern eine Kette von Nachrichten.

    Args:
        first: der erste Wert.
        second: der zweite.
        limit: obere Schranke der Nachrichten.

    Returns:
        Abbildung mit dem Ergebnis und der Zahl der Nachrichten.

    Raises:
        ValueError: bei einem negativen Wert oder wenn die Schranke
            erreicht wird.
    """
    messages = []
    current = (first, second)
    for _ in range(limit):
        messages.append(current)
        report = step(*current)
        if report["done"]:
            return {"result": report["result"], "messages": len(messages),
                    "chain": messages}
        current = report["next"]
    raise ValueError("die Kette erreicht die Schranke")


def why_no_loop():
    """Sagt, warum die Rekursion hier eine Nachricht ist.

    Ein Aktor bearbeitet eine Nachricht und ist danach wieder
    empfangsbereit. Eine Schleife im Aktor würde ihn für die Dauer der
    Rechnung blockieren und alle anderen Nachrichten warten lassen. Die
    Kette von Nachrichten an sich selbst gibt dagegen zwischen je zwei
    Schritten die Gelegenheit, etwas anderes zu bearbeiten.

    Der Preis ist sichtbar: jede Zwischenstufe kostet eine Nachricht,
    und der Zustand der Rechnung muss in der Nachricht stehen, weil der
    Aktor sich zwischen zwei Nachrichten nichts merken soll, was nicht
    zu ihm gehört.
    """
    return {"loop": "blockiert den Aktor",
            "message chain": "lässt ihn zwischendurch andere bedienen",
            "cost": "eine Nachricht je Schritt",
            "state": "steht in der Nachricht, nicht im Aktor"}


def compare_with_subtraction(first, second, limit=2000):
    """Vergleicht die Version mit Rest und die mit Subtraktion.

    Die ursprüngliche Fassung von Euklid zieht ab, statt zu teilen. Beide
    liefern dasselbe Ergebnis, aber die Zahl der Nachrichten geht weit
    auseinander: für 1000 und 3 braucht die Subtraktion dreihundert
    Schritte und die Division zwei.

    Raises:
        ValueError: bei einem negativen Wert oder wenn die Schranke
            erreicht wird.
    """
    if first < 0 or second < 0:
        raise ValueError("negativer Wert")
    left, right = first, second
    steps = 0
    while left != right and left and right:
        if left > right:
            left -= right
        else:
            right -= left
        steps += 1
        if steps > limit:
            raise ValueError("die Kette erreicht die Schranke")
    by_division = run(first, second)
    return {"by subtraction": {"result": left or right,
                               "messages": steps + 1},
            "by division": {"result": by_division["result"],
                            "messages": by_division["messages"]},
            "agree": (left or right) == by_division["result"]}
