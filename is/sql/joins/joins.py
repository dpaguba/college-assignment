"""Verbundarten in SQL und der Preis einer vergessenen Bedingung."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "basic-queries"))

import basic_queries


def run(query, parameters=()):
    """Führt eine Anfrage auf der Beispieldatenbank aus."""
    return basic_queries.run(query, parameters)


def forgotten_condition():
    """Misst, wie viele Zeilen ohne Verbundbedingung entstehen.

    Returns:
        Abbildung mit der Zeilenzahl mit und ohne Bedingung.
    """
    without = run("SELECT * FROM presidents, elections")
    with_condition = run("SELECT * FROM presidents p, elections e "
                         "WHERE e.president = p.name")
    return {"without condition": len(without),
            "with condition": len(with_condition)}


def outer_join_kinds():
    """Nennt die drei äußeren Verbunde und was sie erhalten."""
    return {"left": "all rows of the left table",
            "right": "all rows of the right table",
            "full": "all rows of both tables"}


def join_is_commutative():
    """Prüft, dass der innere Verbund von der Reihenfolge unabhängig ist."""
    first = run("SELECT p.name, e.year FROM presidents p "
                "JOIN elections e ON e.president = p.name")
    second = run("SELECT p.name, e.year FROM elections e "
                "JOIN presidents p ON e.president = p.name")
    return sorted(first) == sorted(second)
