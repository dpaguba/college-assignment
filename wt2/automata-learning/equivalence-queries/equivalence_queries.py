"""Äquivalenzfragen: wie ein Modell gegen die Wirklichkeit geprüft wird."""

import itertools
import random


def run(machine, word):
    """Lässt einen Automaten ein Wort lesen und meldet die Antwort.

    Raises:
        KeyError: bei einem unbekannten Buchstaben.
    """
    state = machine["start"]
    for letter in word:
        state = machine["transitions"][(state, letter)]
    return state in machine["accepting"]


def words(alphabet, limit):
    """Zählt alle Wörter bis zur genannten Länge auf."""
    for length in range(limit + 1):
        for combination in itertools.product(alphabet, repeat=length):
            yield "".join(combination)


def word_count(letters, limit):
    """Zahl der Wörter bis zu einer Länge über einem Alphabet.

    Die Summe der Potenzen wächst geometrisch; das ist der Grund, aus dem
    die erschöpfende Suche nur für kurze Wörter taugt.

    Raises:
        ValueError: bei nicht positiven Werten.
    """
    if letters < 1 or limit < 0:
        raise ValueError("unbrauchbare Werte")
    return sum(letters ** length for length in range(limit + 1))


def exhaustive(machine, membership, alphabet, limit):
    """Sucht das kürzeste Gegenbeispiel bis zur Länge ``limit``.

    Returns:
        Das erste Wort, in dem sich beide unterscheiden, oder None.
    """
    for word in words(alphabet, limit):
        if run(machine, word) != bool(membership(word)):
            return word
    return None


def agree(machine, membership, alphabet, limit):
    """Sagt, ob Modell und Wirklichkeit bis zur Länge ``limit`` übereinstimmen."""
    return exhaustive(machine, membership, alphabet, limit) is None


def sampling(machine, membership, alphabet, count, length, seed=0):
    """Sucht ein Gegenbeispiel durch zufälliges Ziehen von Wörtern.

    Returns:
        Ein Gegenbeispiel oder None; None heisst hier nur, dass keines
        gezogen wurde.
    """
    generator = random.Random(seed)
    for _ in range(count):
        size = generator.randint(0, length)
        word = "".join(generator.choice(alphabet) for _ in range(size))
        if run(machine, word) != bool(membership(word)):
            return word
    return None


def break_one_transition(machine):
    """Verbiegt einen Übergang, damit ein Gegenbeispiel entsteht."""
    broken = dict(machine)
    transitions = dict(machine["transitions"])
    key = sorted(transitions)[0]
    states = machine["states"]
    transitions[key] = states[(states.index(transitions[key]) + 1)
                              % len(states)]
    broken["transitions"] = transitions
    return broken


def sampling_versus_search():
    """Zeigt einen Fall, in dem das Ziehen den Fehler nicht findet.

    Der Unterschied liegt in einem einzigen langen Wort; wer kurze Wörter
    zieht, trifft es fast nie, während die geordnete Suche es sicher
    findet.

    Returns:
        Abbildung mit dem Ergebnis beider Verfahren.
    """
    alphabet = ("a", "b")

    def membership(word):
        """Wahr für alle Wörter ausser einem einzigen langen."""
        return word != "aaaaa"

    machine = {"states": [0], "start": 0, "accepting": {0},
               "transitions": {(0, letter): 0 for letter in alphabet},
               "alphabet": alphabet}
    return {"found by search": exhaustive(machine, membership, alphabet, 6),
            "found by sampling": sampling(machine, membership, alphabet,
                                          count=200, length=3, seed=1)}


def w_method_size(states, alphabet, extra):
    """Schätzt den Umfang der Prüfmenge nach der W-Methode.

    Die Methode kombiniert eine Menge, die jeden Zustand erreicht, mit
    Wörtern bis zur angenommenen Zahl überzähliger Zustände und einer
    Menge, die je zwei Zustände unterscheidet. Der Umfang wächst
    polynomial statt geometrisch.

    Raises:
        ValueError: bei nicht positiven Werten.
    """
    if states < 1 or alphabet < 1 or extra < 0:
        raise ValueError("unbrauchbare Werte")
    middle = sum(alphabet ** length for length in range(extra + 1))
    return {"w method": states * middle * states,
            "exhaustive": word_count(alphabet, states + extra),
            "states": states}


def kinds():
    """Nennt die Wege, ein gelerntes Modell zu prüfen."""
    return {"exhaustive": "complete up to a length, exponential",
            "random sampling": "cheap, no guarantee",
            "w method": "complete under an assumption on the state count",
            "in practice": "the running system answers, and a bug in the "
                           "model is found only when it is used"}
