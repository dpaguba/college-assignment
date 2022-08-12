"""Das Lernverfahren L* von Angluin."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "observation-table"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "equivalence-queries"))

import equivalence_queries
import observation_table


def learn(alphabet, membership, equivalence=None, limit=8, rounds=50):
    """Lernt einen Automaten aus Zugehörigkeits- und Äquivalenzfragen.

    Die Tabelle wird abgeschlossen und widerspruchsfrei gemacht, daraus
    eine Hypothese gebaut und dem Äquivalenzorakel vorgelegt. Ein
    Gegenbeispiel wird samt allen seinen Präfixen in die Zeilen
    aufgenommen, und es geht von vorn los.

    Args:
        alphabet: die Buchstaben.
        membership: Orakel für die Zugehörigkeit eines Wortes.
        equivalence: Orakel, das ein Gegenbeispiel liefert oder None; ohne
            Angabe wird erschöpfend bis ``limit`` gesucht.
        limit: Wortlänge des voreingestellten Äquivalenzorakels.
        rounds: obere Schranke der Durchläufe.

    Returns:
        Der gelernte Automat, ergänzt um ``rounds`` und ``queries``.

    Raises:
        ValueError: wenn die Schranke der Durchläufe erreicht wird.
    """
    table = observation_table.Table(alphabet, membership)
    if equivalence is None:
        def equivalence(machine):
            """Sucht erschöpfend nach einem Gegenbeispiel."""
            return equivalence_queries.exhaustive(machine, membership,
                                                  alphabet, limit)
    for round_number in range(1, rounds + 1):
        table.make_closed_and_consistent()
        machine = table.hypothesis()
        counterexample = equivalence(machine)
        if counterexample is None:
            machine["rounds"] = round_number
            machine["queries"] = table.queries
            machine["table"] = table
            return machine
        for index in range(len(counterexample) + 1):
            table.add_prefix(counterexample[:index])
    raise ValueError("nach %d Durchlaeufen kein Ergebnis" % rounds)


def accepts(machine, word):
    """Lässt einen Automaten ein Wort lesen.

    Raises:
        KeyError: bei einem Buchstaben, den der Automat nicht kennt.
    """
    state = machine["start"]
    for letter in word:
        state = machine["transitions"][(state, letter)]
    return state in machine["accepting"]


def query_counts():
    """Vergleicht den Aufwand für zwei verschieden grosse Alphabete.

    Die Zahl der Fragen wächst mit der Zahl der Buchstaben, weil jede
    Zeile für jeden Buchstaben verlängert werden muss.

    Returns:
        Abbildung mit der Zahl der Fragen in beiden Fällen.
    """
    def parity(word):
        """Wahr, wenn die Zahl der a gerade ist."""
        return word.count("a") % 2 == 0

    two = learn(("a", "b"), parity)
    three = learn(("a", "b", "c"), parity)
    return {"two letters": two["queries"], "three letters": three["queries"],
            "states": len(two["states"])}


def weak_oracle_report():
    """Zeigt, was ein zu schwaches Äquivalenzorakel anrichtet.

    Wird nur bis zur Länge zwei nach Gegenbeispielen gesucht, so bleibt
    eine Sprache unentdeckt, die erst bei drei Buchstaben auffällt. Das
    Ergebnis sieht wie ein fertiges Modell aus und ist keines.

    Returns:
        Abbildung mit der Zahl der Zustände und dem Prüfergebnis bei
        grösserer Schranke.
    """
    def target(word):
        """Wahr, wenn das Wort auf aab endet."""
        return word.endswith("aab")

    weak = learn(("a", "b"), target, limit=2)
    strong = learn(("a", "b"), target, limit=8)
    return {"states with the weak oracle": len(weak["states"]),
            "states with the strong oracle": len(strong["states"]),
            "agrees at the larger limit": equivalence_queries.agree(
                weak, target, ("a", "b"), limit=6)}


def complexity():
    """Nennt die Schranken, die für das Verfahren bewiesen sind."""
    return {"membership queries": "O(k n^2 m), k letters, n states, "
                                  "m the longest counterexample",
            "equivalence queries": "at most n, one per new state",
            "why it terminates": "every counterexample adds a state, and "
                                 "there are only finitely many"}
