"""Verbrauchsfolgeverfahren: FIFO, LIFO und der gewogene Durchschnitt."""

PURCHASES = ((100, 10.0), (100, 12.0), (100, 15.0))
SOLD = 150


def available(purchases=PURCHASES):
    """Nennt Menge und Wert der zur Verfügung stehenden Ware.

    Raises:
        ValueError: bei einer leeren Liste oder negativen Angaben.
    """
    if not purchases:
        raise ValueError("keine Zugänge")
    for amount, price in purchases:
        if amount < 0 or price < 0:
            raise ValueError("negative Menge oder negativer Preis")
    return {"quantity": sum(amount for amount, _ in purchases),
            "value": sum(amount * price for amount, price in purchases)}


def fifo(purchases=PURCHASES, sold=SOLD):
    """Zuerst gekauft, zuerst verbraucht.

    Bei steigenden Preisen verbraucht das Verfahren die alten billigen
    Posten und lässt die teuren im Bestand: der Aufwand ist niedrig, der
    Gewinn hoch, und der Bestand steht nahe am aktuellen Wert.

    Raises:
        ValueError: bei einer negativen Menge oder mehr Verbrauch als
            Bestand.
    """
    report = available(purchases)
    if sold < 0 or sold > report["quantity"]:
        raise ValueError("unzulässige Verbrauchsmenge")
    left = sold
    cost = 0.0
    for amount, price in purchases:
        taken = min(left, amount)
        cost += taken * price
        left -= taken
    return {"cost of goods sold": cost,
            "ending inventory": report["value"] - cost,
            "sold": sold}


def lifo(purchases=PURCHASES, sold=SOLD):
    """Zuletzt gekauft, zuerst verbraucht.

    Bei steigenden Preisen genau umgekehrt: der Aufwand ist hoch, der
    Gewinn niedrig, und der Bestand bleibt zu alten Preisen stehen. Das
    Verfahren ist handelsrechtlich zulässig und international nicht,
    weil der Bestand mit der Zeit beliebig weit vom Marktwert abweicht.

    Raises:
        ValueError: bei einer negativen Menge oder mehr Verbrauch als
            Bestand.
    """
    report = available(purchases)
    if sold < 0 or sold > report["quantity"]:
        raise ValueError("unzulässige Verbrauchsmenge")
    left = sold
    cost = 0.0
    for amount, price in reversed(list(purchases)):
        taken = min(left, amount)
        cost += taken * price
        left -= taken
    return {"cost of goods sold": cost,
            "ending inventory": report["value"] - cost,
            "sold": sold}


def average(purchases=PURCHASES, sold=SOLD):
    """Der gewogene Durchschnitt über alle Zugänge.

    Raises:
        ValueError: bei einer negativen Menge oder mehr Verbrauch als
            Bestand.
    """
    report = available(purchases)
    if sold < 0 or sold > report["quantity"]:
        raise ValueError("unzulässige Verbrauchsmenge")
    unit = report["value"] / report["quantity"]
    return {"unit cost": unit, "cost of goods sold": sold * unit,
            "ending inventory": report["value"] - sold * unit,
            "sold": sold}


def compare(purchases=PURCHASES, sold=SOLD):
    """Stellt die drei Verfahren nebeneinander.

    Die Probe: Aufwand plus Endbestand ist bei allen drei Verfahren
    gleich und gleich dem Wert der verfügbaren Ware. Verteilt wird nur,
    was schon da ist; kein Verfahren erzeugt oder vernichtet Wert. Was
    sich unterscheidet, ist allein, wie viel davon jetzt in den Erfolg
    geht und wie viel später.

    Returns:
        Abbildung mit den drei Ergebnissen und der Probe.
    """
    report = available(purchases)
    results = {"fifo": fifo(purchases, sold), "lifo": lifo(purchases, sold),
               "average": average(purchases, sold)}
    return {"available": report["value"],
            "results": {name: {"cost": round(row["cost of goods sold"], 2),
                               "inventory": round(row["ending inventory"],
                                                  2)}
                        for name, row in results.items()},
            "all add up": all(abs(row["cost of goods sold"]
                                  + row["ending inventory"]
                                  - report["value"]) < 1e-9
                              for row in results.values()),
            "highest profit": min(results,
                                  key=lambda name:
                                  results[name]["cost of goods sold"]),
            "lowest profit": max(results,
                                 key=lambda name:
                                 results[name]["cost of goods sold"])}


def with_falling_prices():
    """Dreht die Preisentwicklung um und zeigt, dass sich alles umkehrt.

    Bei fallenden Preisen liefert FIFO den hohen Aufwand und LIFO den
    niedrigen. Die verbreitete Merkregel «LIFO senkt den Gewinn» gilt
    also nur bei steigenden Preisen, und sie wird trotzdem meist ohne
    diese Bedingung zitiert.

    Returns:
        Abbildung mit beiden Fällen.
    """
    rising = compare(PURCHASES, SOLD)
    falling = compare(((100, 15.0), (100, 12.0), (100, 10.0)), SOLD)
    return {"rising prices": {"lowest profit": rising["lowest profit"]},
            "falling prices": {"lowest profit": falling["lowest profit"]},
            "the rule holds only": "bei steigenden Preisen"}
