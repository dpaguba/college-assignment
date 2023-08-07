"""Lernende Klassifikatorsysteme: Regeln, die sich selbst bewerten."""

import random


def rule(condition, action, fitness=1.0):
    """Baut eine Regel.

    Die Bedingung ist eine Folge aus null, eins und dem Platzhalter
    ``#``, der auf beides passt. Der Platzhalter ist der ganze Trick:
    er macht eine Regel allgemeiner, und wie allgemein sie sein darf,
    entscheidet sich daran, ob sie damit noch recht behält.

    Raises:
        ValueError: bei einem unzulässigen Zeichen oder einer negativen
            Güte.
    """
    if any(character not in "01#" for character in condition):
        raise ValueError("die Bedingung besteht aus 0, 1 und #")
    if fitness < 0:
        raise ValueError("negative Güte")
    return {"condition": condition, "action": action, "fitness": fitness,
            "matched": 0, "correct": 0}


def matches(built, message):
    """Sagt, ob eine Regel auf eine Eingabe passt.

    Raises:
        ValueError: bei einer Eingabe falscher Länge.
    """
    if len(message) != len(built["condition"]):
        raise ValueError("die Eingabe hat die falsche Länge")
    return all(expected in ("#", actual)
               for expected, actual in zip(built["condition"], message))


def match_set(rules, message):
    """Nennt die Regeln, die auf eine Eingabe passen.

    Raises:
        ValueError: bei einer Eingabe falscher Länge.
    """
    return [built for built in rules if matches(built, message)]


def decide(rules, message):
    """Entscheidet über die gewichtete Mehrheit der passenden Regeln.

    Jede passende Regel stimmt mit ihrer Güte für ihre Aktion ab. Das
    ist der Unterschied zu einem Entscheidungsbaum: es entscheidet nicht
    ein Pfad, sondern eine Menge von Regeln, die einander widersprechen
    dürfen.

    Raises:
        ValueError: wenn keine Regel passt.
    """
    found = match_set(rules, message)
    if not found:
        raise ValueError("keine Regel passt")
    votes = {}
    for built in found:
        votes[built["action"]] = (votes.get(built["action"], 0.0)
                                  + built["fitness"])
    return max(votes, key=lambda action: votes[action])


def reward(rules, message, truth, learning=0.2):
    """Bewertet die passenden Regeln nach dem Ergebnis.

    Wer recht hatte, gewinnt an Güte, wer nicht, verliert. Über viele
    Beispiele setzen sich die Regeln durch, die oft passen und dabei oft
    recht haben; zu allgemeine Regeln passen oft und irren oft, zu enge
    passen selten.

    Raises:
        ValueError: bei einer Lernrate ausserhalb von null bis eins.
    """
    if not 0 < learning <= 1:
        raise ValueError("die Lernrate liegt zwischen null und eins")
    for built in match_set(rules, message):
        built["matched"] += 1
        hit = built["action"] == truth
        built["correct"] += 1 if hit else 0
        built["fitness"] += learning * ((1.0 if hit else 0.0)
                                        - built["fitness"])
    return rules


def learn(bits=4, rounds=600, seed=0):
    """Lässt ein kleines System die Parität lernen.

    Die Zielgrösse ist, ob die Zahl der Einsen gerade ist. Für diese
    Aufgabe gibt es keine kurze Regel: jeder Platzhalter zerstört die
    Aussage, weil jedes Bit zählt. Das System muss deshalb die
    vollständigen Bedingungen finden, und daran lässt sich sehen, wie
    die Güte die allgemeinen Regeln aussortiert.

    Returns:
        Abbildung mit der Trefferquote und den besten Regeln.

    Raises:
        ValueError: bei einer zu kleinen Bitzahl oder Rundenzahl.
    """
    if bits < 2 or rounds < 10:
        raise ValueError("zu kleine Aufgabe")
    generator = random.Random(seed)
    rules = []
    for _ in range(60):
        condition = "".join(generator.choice("01#") for _ in range(bits))
        rules.append(rule(condition, generator.choice([0, 1]), 0.5))
    for _ in range(rounds):
        message = "".join(generator.choice("01") for _ in range(bits))
        truth = 1 if message.count("1") % 2 == 0 else 0
        reward(rules, message, truth)
    correct = 0
    checked = 0
    for _ in range(200):
        message = "".join(generator.choice("01") for _ in range(bits))
        truth = 1 if message.count("1") % 2 == 0 else 0
        try:
            correct += 1 if decide(rules, message) == truth else 0
            checked += 1
        except ValueError:
            pass
    best = sorted(rules, key=lambda built: -built["fitness"])[:5]
    return {"accuracy": correct / checked if checked else 0.0,
            "covered": checked / 200,
            "best rules": [(built["condition"], built["action"],
                            round(built["fitness"], 3))
                           for built in best],
            "wildcards in the best": [built["condition"].count("#")
                                      for built in best]}


def why_wildcards_are_the_whole_question():
    """Sagt, worum es beim Lernen von Regeln geht.

    Eine Regel ohne Platzhalter ist ein auswendig gelernter Fall und
    hilft bei keinem anderen. Eine Regel mit lauter Platzhaltern passt
    auf alles und sagt nichts. Dazwischen liegt die Verallgemeinerung,
    und die Güte ist das Mass, das die Balance findet, ohne dass jemand
    sie vorgibt.

    Bei der Parität gibt es keine solche Balance: jedes Bit zählt, also
    ist jede Verallgemeinerung falsch. Das ist der Fall, an dem ein
    regelbasiertes System an seine Grenze kommt, und er ist derselbe,
    an dem ein flacher Entscheidungsbaum scheitert.
    """
    return {"no wildcards": "auswendig gelernt, hilft nur beim selben Fall",
            "all wildcards": "passt immer, sagt nichts",
            "fitness finds": "die Balance dazwischen",
            "parity has none": "jedes Bit zählt, jede Verallgemeinerung "
                               "ist falsch",
            "same limit as": "der flache Entscheidungsbaum"}
