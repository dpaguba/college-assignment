"""Synthesealgorithmus für die dritte Normalform."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "functional-dependencies"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "bcnf-decomposition"))

import bcnf_decomposition
import functional_dependencies as fds


def synthesise(attributes, dependencies):
    """Erzeugt Teilschemata in dritter Normalform.

    Der Algorithmus bildet eine minimale Überdeckung, fasst
    Abhängigkeiten mit gleicher linker Seite zusammen, ergänzt einen
    Schlüssel, falls keiner enthalten ist, und streicht Teilschemata, die
    in einem anderen aufgehen.

    Returns:
        Liste der Teilschemata als Mengen von Attributnamen.
    """
    attributes = set(attributes)
    cover = fds.minimal_cover(dependencies)
    grouped = {}
    for left, right in cover:
        grouped.setdefault(frozenset(left), set()).update(right)
    parts = [set(left) | right for left, right in grouped.items()]
    keys = fds.candidate_keys(attributes, dependencies)
    if keys and not any(keys[0] <= part for part in parts):
        parts.append(set(keys[0]))
    result = []
    for part in parts:
        if any(part < other for other in parts):
            continue
        if part not in result:
            result.append(part)
    return result


def compare():
    """Stellt Zerlegung und Synthese am Beispiel Student-Fach-Lehrkraft gegenüber.

    Returns:
        Abbildung mit den Eigenschaften beider Verfahren auf demselben
        Schema.
    """
    attributes = {"student", "subject", "teacher"}
    dependencies = [({"student", "subject"}, {"teacher"}),
                    ({"teacher"}, {"subject"})]
    by_decomposition = bcnf_decomposition.decompose(attributes, dependencies)
    by_synthesis = synthesise(attributes, dependencies)
    return {
        "bcnf loses a dependency": not bcnf_decomposition
        .preserves_dependencies(dependencies, by_decomposition),
        "synthesis keeps them": bcnf_decomposition.preserves_dependencies(
            dependencies, by_synthesis),
        "both lossless": (
            bcnf_decomposition.lossless(attributes, dependencies,
                                        by_decomposition)
            and bcnf_decomposition.lossless(attributes, dependencies,
                                            by_synthesis)),
    }
