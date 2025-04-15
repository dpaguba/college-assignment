"""Die Bewertungsfunktion der regelbasierten KI."""

FEATURES = ("expected yield", "variety", "points", "blocks")

PHASES = {
    "early": {"expected yield": 10.0, "variety": 3.0, "points": 1.0,
              "blocks": 0.5},
    "middle": {"expected yield": 5.0, "variety": 1.5, "points": 3.0,
               "blocks": 1.5},
    "late": {"expected yield": 1.0, "variety": 0.5, "points": 10.0,
             "blocks": 3.0},
}


def weights(phase="middle"):
    """Nennt die Gewichte einer Spielphase.

    Die Folie fragt, wie sich die Gewichtung über das Spiel verschiebt.
    Die Antwort steht in der Siegbedingung: gewonnen wird mit Punkten,
    nicht mit Karten. Am Anfang ist der Ertrag alles, weil er alle
    späteren Punkte bezahlt; am Ende zählt nur noch, ob ein Zug einen
    Punkt bringt, auch wenn er die Wirtschaft ruiniert.

    Raises:
        ValueError: bei einer unbekannten Phase.
    """
    if phase not in PHASES:
        raise ValueError("unbekannte Phase: %s" % phase)
    return dict(PHASES[phase])


def score(move, weight):
    """Bewertet einen Zug als gewichtete Summe seiner Merkmale.

    Raises:
        ValueError: bei einem unbekannten Merkmal oder einem fehlenden
            Gewicht.
    """
    total = 0.0
    for name, value in move.items():
        if name not in FEATURES:
            raise ValueError("unbekanntes Merkmal: %s" % name)
        if name not in weight:
            raise ValueError("kein Gewicht für: %s" % name)
        total += weight[name] * value
    return total


def best_move(moves, weight):
    """Wählt den bestbewerteten Zug.

    Bei Gleichstand entscheidet die Reihenfolge, in der die Züge
    angeboten werden. Das ist eine Setzung; wichtiger ist, dass sie
    festgelegt und nicht zufällig ist, damit dieselbe Stellung immer
    dieselbe Antwort bekommt.

    Raises:
        ValueError: bei einer leeren Zugliste oder einem fehlenden
            Gewicht.
    """
    if not moves:
        raise ValueError("keine Züge")
    return max(moves, key=lambda move: score(move, weight))


def scaling_changes_nothing(factor=7.5):
    """Zeigt, dass nur die Verhältnisse der Gewichte zählen.

    Alle Gewichte mit derselben positiven Zahl zu multiplizieren
    verändert jede Bewertung, aber keine Reihenfolge. Wer an den
    Gewichten dreht, muss deshalb ihr Verhältnis ändern, und eine
    Bewertung allein sagt nichts, solange die anderen fehlen.

    Returns:
        Abbildung mit beiden Reihenfolgen.
    """
    moves = [{"expected yield": 0.3, "points": 0},
             {"expected yield": 0.1, "points": 1},
             {"expected yield": 0.2, "points": 0}]
    weight = weights("middle")
    scaled = {name: value * factor for name, value in weight.items()}
    order = sorted(range(len(moves)),
                   key=lambda index: -score(moves[index], weight))
    after = sorted(range(len(moves)),
                   key=lambda index: -score(moves[index], scaled))
    return {"order": order, "order after scaling": after,
            "factor": factor,
            "what it means": "nur die Verhältnisse der Gewichte zählen"}


def the_balanced_move_problem(steps=64):
    """Zeigt eine Reihenfolge, die keine lineare Bewertung erzeugt.

    Drei Kreuzungen: eine mit viel Holz und keinem Lehm, eine mit viel
    Lehm und keinem Holz, eine mit der Hälfte von beidem. Gebaut wird
    aus beidem, also ist die dritte die beste. Eine lineare Bewertung
    kann das nicht sagen.

    Der Beweis ist eine Zeile: mit den Merkmalen (1,0), (0,1) und
    (0.5,0.5) verlangt «die dritte schlägt die erste», dass w2 grösser
    als w1 ist, und «die dritte schlägt die zweite», dass w1 grösser als
    w2 ist. Beides zusammen geht nicht, gleich wie die Gewichte gewählt
    werden.

    Nachgerechnet wird es trotzdem: über ein feines Gitter von
    Gewichtsvektoren findet sich keiner, der die gewünschte Reihenfolge
    liefert. Ein Produktterm der beiden Merkmale löst es sofort, und das
    ist der Grund, warum eine reine Summe von Merkmalen für Catan zu
    wenig ist.

    Returns:
        Abbildung mit dem Ergebnis der Suche.

    Raises:
        ValueError: bei einer zu groben Suche.
    """
    if steps < 2:
        raise ValueError("die Suche braucht mehrere Schritte")
    moves = [(1.0, 0.0), (0.0, 1.0), (0.5, 0.5)]
    works = 0
    tried = 0
    for one in range(steps + 1):
        for two in range(steps + 1):
            first = -1.0 + 2.0 * one / steps
            second = -1.0 + 2.0 * two / steps
            tried += 1
            scored = [first * wood + second * clay for wood, clay in moves]
            if scored[2] > scored[0] and scored[2] > scored[1]:
                works += 1
    product = [wood * clay for wood, clay in moves]
    return {"weight vectors tried": tried, "weight vectors that work": works,
            "with a product term": product[2] > product[0]
            and product[2] > product[1],
            "the algebra": "die dritte schlägt beide nur, wenn w2 > w1 "
                           "und w1 > w2",
            "what it means": "eine Summe von Merkmalen kann keine "
                             "Mischung bevorzugen"}


def what_the_rule_based_ai_is_for():
    """Nennt, wozu die erste KI dient, obwohl sie nichts lernt.

    Sie erzeugt die Trainingsdaten für die zweite, und die Folie sagt
    dazu den entscheidenden Satz: bessere Daten führen zu besserer KI.
    Eine schwache regelbasierte KI liefert Partien, in denen nie etwas
    Vernünftiges passiert, und daraus lässt sich vernünftiges Spiel auch
    nicht lernen.

    Zweitens legt sie fest, welche Merkmale überhaupt gemessen werden.
    Was hier nicht als Merkmal steht, sieht die zweite KI später auch
    nicht, wenn sie auf denselben Daten arbeitet.

    Und drittens ist ihre Geschwindigkeit die Menge der Daten: je
    schneller sie entscheidet, desto mehr Partien entstehen.
    """
    return {"first": "sie erzeugt die Trainingsdaten",
            "second": "sie legt fest, welche Merkmale gemessen werden",
            "third": "ihre Geschwindigkeit ist die Datenmenge",
            "the risk": "aus schwachen Partien lässt sich starkes Spiel "
                        "nicht lernen"}
