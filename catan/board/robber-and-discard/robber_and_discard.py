"""Die Sieben: Abwerfen, Räuber und Diebstahl."""

PIPS = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}

LIMIT = 7


def discard_count(hand):
    """Nennt, wie viele Karten bei einer Sieben abzugeben sind.

    Über sieben Karten wird die Hälfte abgegeben, abgerundet. Die
    Grenze ist scharf: bei sieben Karten nichts, bei acht gleich vier.

    Raises:
        ValueError: bei einer negativen Handkartenzahl.
    """
    if hand < 0:
        raise ValueError("negative Handkartenzahl")
    return 0 if hand <= LIMIT else hand // 2


def the_threshold():
    """Zeigt, was die achte Karte kostet.

    Sie kostet nicht sich selbst, sondern vier Karten, denn mit ihr
    fällt die Hand unter die Regel. Das ist der Grund, warum erfahrene
    Spieler mit genau sieben Karten in den Wurf gehen und lieber
    ungünstig bauen, als die achte anzunehmen.

    Returns:
        Abbildung mit der Grenze und ihrem Preis.
    """
    return {"largest safe hand": LIMIT,
            "cost of the eighth card": discard_count(LIMIT + 1),
            "the eighth card is worth": -discard_count(LIMIT + 1) + 1,
            "what players do": "mit genau sieben Karten in den Wurf "
                               "gehen"}


def expected_loss(hand, players=4):
    """Schätzt den Verlust je eigenem Zug durch die Sieben.

    Raises:
        ValueError: bei einer negativen Hand oder Spielerzahl.
    """
    if hand < 0 or players <= 0:
        raise ValueError("unzulässige Angaben")
    chance = 6.0 / 36.0
    return {"chance of a seven": chance,
            "cards discarded if it falls": discard_count(hand),
            "expected cards lost": chance * discard_count(hand),
            "per round": players * chance * discard_count(hand)}


def steal_chance(hand):
    """Nennt, welche Karte der Räuber mit welcher Chance nimmt.

    Raises:
        ValueError: bei einer leeren Hand.
    """
    total = sum(hand.values())
    if total <= 0:
        raise ValueError("eine leere Hand kann nicht bestohlen werden")
    return {name: count / total for name, count in hand.items()}


def blocked_yield(token):
    """Nennt, was ein blockiertes Feld je Zug kostet.

    Der Räuber nimmt dem Feld den ganzen Ertrag, nicht einen Teil.
    Deshalb kostet er auf einer Acht fünf Sechsunddreissigstel je
    angrenzender Siedlung und auf einer Zwei nur ein
    Sechsunddreissigstel.

    Raises:
        ValueError: bei einer unmöglichen Zahl.
    """
    if token not in PIPS:
        raise ValueError("kein gültiges Zahlenplättchen")
    return {"token": token, "lost per turn": PIPS[token] / 36.0,
            "compared with a two": PIPS[token] / PIPS[2],
            "why he goes on the eight": "er nimmt den ganzen Ertrag, "
                                        "nicht einen Teil"}


def why_the_seven_is_two_rules():
    """Trennt die beiden Wirkungen der Sieben.

    Die eine trifft alle mit vollen Händen und ist rein zufällig; die
    andere wird von einem Spieler gesetzt und trifft gezielt. Die erste
    bestraft das Sammeln, die zweite bestraft den Führenden. Zusammen
    sorgen sie dafür, dass ein Vorsprung teurer wird, je grösser er ist,
    und das hält die Partie offen.
    """
    return {"random half": "wer über sieben Karten hält, verliert die "
                           "Hälfte",
            "chosen half": "der Räuber wird gesetzt und trifft gezielt",
            "what both do": "ein Vorsprung wird teurer, je grösser er "
                            "ist",
            "effect on the game": "die Partie bleibt offen"}
