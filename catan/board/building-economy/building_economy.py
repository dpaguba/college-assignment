"""Baukosten, Vorräte und was sie an Zeit bedeuten."""

import random

COSTS = {"Straße": {"Lehm": 1, "Holz": 1},
         "Siedlung": {"Lehm": 1, "Holz": 1, "Wolle": 1, "Getreide": 1},
         "Stadt": {"Getreide": 2, "Erz": 3},
         "Entwicklungskarte": {"Wolle": 1, "Getreide": 1, "Erz": 1}}

PIECES = {"Straße": 15, "Siedlung": 5, "Stadt": 4}

POINTS = {"Siedlung": 1, "Stadt": 2}

PIPS = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}


def cost(building):
    """Nennt die Kosten eines Bauwerks.

    Raises:
        ValueError: bei einem unbekannten Bauwerk.
    """
    if building not in COSTS:
        raise ValueError("unbekanntes Bauwerk: %s" % building)
    return dict(COSTS[building])


def victory_points(built, longest_road=False, largest_army=False,
                   cards=0):
    """Zählt die Siegpunkte eines Spielers.

    Raises:
        ValueError: bei mehr Bauwerken, als die Schachtel hergibt, oder
            einer negativen Kartenzahl.
    """
    if cards < 0:
        raise ValueError("negative Kartenzahl")
    for name, count in built.items():
        if name not in PIECES:
            raise ValueError("unbekanntes Bauwerk: %s" % name)
        if count > PIECES[name] or count < 0:
            raise ValueError("mehr %s als vorhanden" % name)
    points = sum(POINTS.get(name, 0) * count
                 for name, count in built.items())
    points += 2 if longest_road else 0
    points += 2 if largest_army else 0
    points += cards
    return {"points": points, "wins": points >= 10,
            "from buildings": sum(POINTS.get(name, 0) * count
                                  for name, count in built.items()),
            "from bonuses": (2 if longest_road else 0)
            + (2 if largest_army else 0)}


def city_or_settlement():
    """Vergleicht den Ausbau mit dem Neubau.

    Eine Stadt kostet fünf Karten und bringt einen Punkt und den
    doppelten Ertrag einer schon vorhandenen Kreuzung. Eine Siedlung
    kostet vier Karten, bringt ebenfalls einen Punkt, braucht aber eine
    freie Kreuzung, meist eine Strasse dorthin und liefert von einer
    Kreuzung, die schwächer ist als die erste, denn die beste war zuerst
    dran.

    Deshalb dreht sich das Verhältnis im Verlauf: früh ist die Siedlung
    besser, weil noch gute Kreuzungen frei sind, später die Stadt.
    """
    return {"city": {"cards": 5, "points": 1,
                     "needs": "eine eigene Siedlung"},
            "settlement": {"cards": 4, "points": 1,
                           "needs": "eine freie Kreuzung und meist eine "
                                    "Strasse"},
            "why the city wins later": "die freien Kreuzungen sind dann "
                                       "die schwachen",
            "why the settlement wins early": "die guten Kreuzungen sind "
                                             "noch frei"}


def turns_to_afford(building, tokens, resources, trials=10000, seed=0):
    """Schätzt, wie viele Züge das Sparen für ein Bauwerk dauert.

    Gewürfelt wird für eine einzelne Siedlung an den gegebenen Feldern,
    ohne Handel und ohne Räuber. Das ist die Untergrenze der Wartezeit
    und zeigt, warum eine Kreuzung ohne den passenden Rohstoff das
    Bauwerk nie erreicht.

    Args:
        building: das Bauwerk.
        tokens: die Zahlen der angrenzenden Felder.
        resources: die Rohstoffe derselben Felder.
        trials: die Anzahl der Durchläufe.
        seed: der Startwert.

    Returns:
        Abbildung mit dem Mittel aus Simulation und Rechnung.

    Raises:
        ValueError: bei einem unbekannten Bauwerk, unpassend vielen
            Angaben oder einem Rohstoff, den die Kreuzung nie liefert.
    """
    needed = cost(building)
    if len(tokens) != len(resources):
        raise ValueError("zu jeder Zahl gehört ein Rohstoff")
    missing = [name for name in needed
               if name not in [row for row in resources if row]]
    if missing:
        raise ValueError("die Kreuzung liefert nie: %s"
                         % ", ".join(sorted(missing)))
    rng = random.Random(seed)
    total = 0
    for _ in range(trials):
        hand = {name: 0 for name in needed}
        turns = 0
        while any(hand[name] < needed[name] for name in needed):
            turns += 1
            rolled = rng.randint(1, 6) + rng.randint(1, 6)
            for token, resource in zip(tokens, resources):
                if token == rolled and resource in hand:
                    hand[resource] += 1
        total += turns
    rates = {}
    for name in needed:
        rates[name] = sum(PIPS.get(token, 0) / 36.0
                          for token, resource in zip(tokens, resources)
                          if resource == name)
    slowest = max(needed[name] / rates[name] for name in needed)
    return {"by simulation": total / trials,
            "mean turns": exact_turns(building, tokens, resources),
            "slowest resource alone": slowest,
            "rates": rates, "needed": needed,
            "why waiting is longer than the slowest": "gewartet wird auf "
                                                      "den letzten der "
                                                      "Rohstoffe"}


def exact_turns(building, tokens, resources, tolerance=1e-12):
    """Rechnet die erwartete Wartezeit exakt aus.

    Der Zustand ist der Vorrat, bei den benötigten Mengen abgeschnitten.
    Ein Wurf führt von einem Zustand in einen anderen, mit den bekannten
    Wahrscheinlichkeiten der elf Summen. Damit ist die Wartezeit die
    erwartete Schrittzahl bis zum Zielzustand einer endlichen Markowkette,
    und die lässt sich ausrechnen statt auswürfeln.

    Die Rohstoffe kommen nicht unabhängig: ein Wurf bedient alle
    angrenzenden Felder mit dieser Zahl auf einmal. Eine Formel, die die
    Rohstoffe getrennt behandelt, wäre deshalb falsch, und die Kette
    umgeht die Frage.

    Raises:
        ValueError: wie bei ``turns_to_afford``.
    """
    needed = cost(building)
    if len(tokens) != len(resources):
        raise ValueError("zu jeder Zahl gehört ein Rohstoff")
    names = sorted(needed)
    gains = {}
    for roll in range(2, 13):
        gain = tuple(sum(1 for token, resource in zip(tokens, resources)
                         if token == roll and resource == name)
                     for name in names)
        if any(gain):
            gains[roll] = gain
    if not gains:
        raise ValueError("die Kreuzung liefert keinen der Rohstoffe")
    target = tuple(needed[name] for name in names)
    states = [(0,)]
    for limit in target:
        states = [row + (value,) for row in states
                  for value in range(limit + 1)]
    states = [row[1:] for row in states]
    values = {state: 0.0 for state in states}
    for _ in range(10000):
        moved = 0.0
        for state in states:
            if state == target:
                continue
            weight = 0.0
            total = 1.0
            for roll, gain in gains.items():
                after = tuple(min(target[index], state[index]
                                  + gain[index])
                              for index in range(len(target)))
                if after == state:
                    continue
                chance = PIPS.get(roll, 0) / 36.0
                weight += chance
                total += chance * values[after]
            if weight <= 0.0:
                raise ValueError("aus diesem Vorrat führt kein Wurf "
                                 "weiter")
            total /= weight
            moved = max(moved, abs(total - values[state]))
            values[state] = total
        if moved < tolerance:
            break
    return values[tuple(0 for _ in target)]


def what_the_costs_encode():
    """Sagt, was die Kostentabelle über das Spiel verrät.

    Lehm und Holz bauen aus, Getreide und Erz bauen auf. Wer am Anfang
    keinen Lehm hat, kommt nicht in die Fläche; wer später kein Erz hat,
    kommt nicht in die Höhe. Die Wolle steht in beiden Sätzen einmal und
    ist deshalb der Rohstoff, den man am ehesten hergeben kann.
    """
    return {"Lehm und Holz": "in die Fläche, Strassen und Siedlungen",
            "Getreide und Erz": "in die Höhe, Städte und Karten",
            "Wolle": "in beiden Sätzen einmal, also am ehesten "
                     "verhandelbar",
            "what it means for the opening": "ohne Lehm keine Fläche, "
                                             "ohne Erz keine Höhe"}
