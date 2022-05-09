"""Was das Aktormodell zusichert und was die Umsetzung zusichert."""

import itertools


def deliveries(order):
    """Bildet eine Zustellreihenfolge auf die empfangene Folge ab.

    Args:
        order: die Reihenfolge, in der die Nachrichten zugestellt werden.

    Returns:
        Die Folge, wie der Empfänger sie sieht.
    """
    return tuple(order)


def possible_orders(first, second):
    """Zählt die Reihenfolgen auf, in denen zwei Sender ankommen können.

    Args:
        first: die Nachrichten des ersten Senders, in Absendereihenfolge.
        second: die des zweiten.

    Returns:
        Abbildung mit allen Verschränkungen und denen, die die
        Absendereihenfolge je Sender erhalten.
    """
    marks = list(first) + list(second)
    everything = {tuple(order)
                  for order in itertools.permutations(marks)}
    keeps_order = set()
    for order in everything:
        left = [item for item in order if item in first]
        right = [item for item in order if item in second]
        if left == list(first) and right == list(second):
            keeps_order.add(order)
    return {"all orders": len(everything),
            "order preserving": len(keeps_order),
            "examples": sorted(keeps_order)[:4]}


def agha_against_implementations():
    """Vergleicht die Zusicherung der Theorie mit der der Praxis.

    Agha sichert zu, dass jede Nachricht irgendwann ankommt, und sagt
    nichts über die Reihenfolge, auch nicht zwischen denselben zwei
    Aktoren. Verbreitete Umsetzungen tauschen das: sie erhalten die
    Reihenfolge zwischen einem Paar von Aktoren und geben dafür die
    sichere Zustellung auf, weil eine Nachricht über das Netz verloren
    gehen kann.

    Beide Zusicherungen sind schwächer, als der erste Blick vermuten
    lässt. Bei der Theorie darf eine Nachricht beliebig lange
    unterwegs sein; bei der Praxis gilt die Reihenfolge nur je Paar, und
    schon bei drei Aktoren sagt sie nichts mehr darüber, was zuerst
    ankommt.

    Returns:
        Abbildung mit beiden Zusicherungen.
    """
    return {"theory": {"delivery": "irgendwann, sicher",
                       "order": "keine, auch nicht je Paar"},
            "implementation": {"delivery": "höchstens einmal, kann "
                                           "verlorengehen",
                               "order": "je Paar erhalten"},
            "both": "über drei Aktoren hinweg gibt es keine Reihenfolge",
            "consequence": "eine Rechnung, die von der Reihenfolge "
                           "zweier Absender abhängt, ist falsch"}


def three_actors_have_no_order():
    """Zeigt, dass die Reihenfolge je Paar bei drei Aktoren nichts sagt.

    Zwei Sender schicken je zwei Nachrichten an denselben Empfänger. Die
    Reihenfolge je Absender bleibt erhalten, und trotzdem bleiben sechs
    mögliche Folgen übrig: die Zusicherung schränkt von vierundzwanzig
    auf sechs ein und legt nichts fest.

    Returns:
        Abbildung mit beiden Zahlen.
    """
    report = possible_orders(("a1", "a2"), ("b1", "b2"))
    return {"all orders": report["all orders"],
            "with per sender order": report["order preserving"],
            "still ambiguous": report["order preserving"] > 1,
            "examples": report["examples"]}


def what_to_rely_on():
    """Nennt, worauf sich ein Programm stützen darf.

    Auf den eigenen Zustand, denn den sieht niemand sonst. Auf die
    Bearbeitung einer Nachricht als Ganzes. Und auf das, was im
    Protokoll erzwungen wird: wer eine Reihenfolge braucht, muss sie
    durch Quittungen herstellen, statt sie zu erwarten.
    """
    return ["der eigene Zustand ist privat",
            "eine Nachricht wird ganz oder gar nicht bearbeitet",
            "eine Reihenfolge entsteht nur durch Quittungen",
            "alles andere ist eine Annahme über die Umsetzung"]
