"""Künstliche neuronale Netze: vom einzelnen Neuron zur verdeckten Schicht."""

import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "support-vector-machines"))

import support_vector_machines

AND = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1}
OR = {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 1}
NAND = {(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 0}
NOR = {(0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 0}
XOR = {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0}
XNOR = {(0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 1}


def neuron(weights, threshold):
    """Baut ein Neuron mit Schwellenwertfunktion."""
    return {"weights": list(weights), "threshold": float(threshold)}


def fire(cell, inputs):
    """Wertet ein Neuron aus: eins, sobald die Summe die Schwelle erreicht.

    Raises:
        ValueError: wenn die Zahl der Eingänge nicht zu den Gewichten passt.
    """
    if len(inputs) != len(cell["weights"]):
        raise ValueError("Eingaenge passen nicht zu den Gewichten")
    total = sum(weight * value
                for weight, value in zip(cell["weights"], inputs))
    return 1 if total >= cell["threshold"] else 0


def and_neuron():
    """Liefert ein Neuron, das die Konjunktion berechnet.

    Beide Gewichte sind eins, die Schwelle liegt bei 1.5: nur wenn beide
    Eingänge brennen, wird die Schwelle erreicht. Die Trennlinie ist
    x₁ + x₂ = 1.5.
    """
    return neuron((1.0, 1.0), 1.5)


def or_neuron():
    """Liefert ein Neuron für die Disjunktion, mit der Schwelle 0.5."""
    return neuron((1.0, 1.0), 0.5)


def nor_neuron():
    """Liefert ein Neuron, das brennt, wenn kein Eingang brennt."""
    return neuron((-1.0, -1.0), -0.5)


def is_half_plane(cell):
    """Sagt, ob die Entscheidungsgrenze eine Gerade ist.

    Ein Neuron mit gewichteter Summe und Schwelle teilt den Eingaberaum
    immer in zwei Halbräume; etwas anderes kann es nicht.
    """
    return len(cell["weights"]) >= 1


def linearly_separable(table):
    """Prüft, ob eine Wahrheitstafel von einem Neuron berechnet werden kann.

    Geprüft wird der Abstand der konvexen Hüllen der beiden Klassen; das
    ist die Frage, ob eine Gerade die Einsen von den Nullen trennt.
    """
    samples = [(inputs, 1 if value else -1)
               for inputs, value in table.items()]
    return support_vector_machines.linearly_separable(samples)


def xnor_network():
    """Baut ein Netz für die Äquivalenz aus drei Neuronen.

    Die verdeckte Schicht bildet die Konjunktion und die Nor-Verknüpfung;
    beide Fälle, in denen die Eingänge gleich sind, werden dadurch
    getrennt sichtbar, und die Ausgabeschicht verodert sie.
    """
    return {"hidden": [and_neuron(), nor_neuron()], "output": or_neuron()}


def run(network, inputs):
    """Wertet ein zweischichtiges Netz aus."""
    hidden = tuple(fire(cell, inputs) for cell in network["hidden"])
    return fire(network["output"], hidden)


def hidden_layer_report():
    """Vergleicht die Trennbarkeit vor und hinter der verdeckten Schicht.

    Returns:
        Abbildung mit beiden Antworten und den Bildern der vier Eingaben.
    """
    network = xnor_network()
    mapped = {}
    for inputs, value in XNOR.items():
        hidden = tuple(fire(cell, inputs) for cell in network["hidden"])
        mapped[hidden] = value
    return {"input space separable": linearly_separable(XNOR),
            "hidden space separable": linearly_separable(mapped),
            "images": mapped}


def _sigmoid(value):
    """Logistische Funktion als glatter Ersatz der Schwelle."""
    if value < -60:
        return 0.0
    if value > 60:
        return 1.0
    return 1.0 / (1.0 + math.exp(-value))


def train(table, hidden=2, rounds=20000, rate=0.5, seed=0):
    """Lernt eine Wahrheitstafel mit Rückwärtsausbreitung des Fehlers.

    Returns:
        Abbildung mit den Gewichten beider Schichten.
    """
    generator = random.Random(seed)
    inputs = list(table)
    first = [[generator.uniform(-1, 1) for _ in range(3)]
             for _ in range(hidden)]
    second = [generator.uniform(-1, 1) for _ in range(hidden + 1)]
    for _ in range(rounds):
        for values in inputs:
            target = table[values]
            layer = [_sigmoid(row[0] * values[0] + row[1] * values[1] + row[2])
                     for row in first]
            output = _sigmoid(sum(second[index] * layer[index]
                                  for index in range(hidden)) + second[hidden])
            error = (output - target) * output * (1 - output)
            gradients = []
            for index in range(hidden):
                gradients.append(error * second[index] * layer[index]
                                 * (1 - layer[index]))
            for index in range(hidden):
                second[index] -= rate * error * layer[index]
            second[hidden] -= rate * error
            for index in range(hidden):
                first[index][0] -= rate * gradients[index] * values[0]
                first[index][1] -= rate * gradients[index] * values[1]
                first[index][2] -= rate * gradients[index]
    return {"first": first, "second": second, "hidden": hidden}


def evaluate(model, values):
    """Wertet ein gelerntes Netz aus und gibt die Ausgabe zwischen 0 und 1."""
    layer = [_sigmoid(row[0] * values[0] + row[1] * values[1] + row[2])
             for row in model["first"]]
    return _sigmoid(sum(model["second"][index] * layer[index]
                        for index in range(model["hidden"]))
                    + model["second"][model["hidden"]])


def squared_error(model, table):
    """Summe der quadrierten Abweichungen über die Wahrheitstafel."""
    return sum((evaluate(model, values) - target) ** 2
               for values, target in table.items())


def training_reduces_error():
    """Misst den Fehler vor und nach dem Lernen der Äquivalenz.

    Returns:
        Abbildung mit beiden Fehlern.
    """
    before = train(XNOR, rounds=0, seed=3)
    after = train(XNOR, rounds=20000, seed=3)
    return {"before": squared_error(before, XNOR),
            "after": squared_error(after, XNOR)}


def why_one_neuron_fails():
    """Begründet, warum ein einzelnes Neuron die Äquivalenz nicht schafft.

    Die Eingaben mit der Ausgabe eins liegen sich diagonal gegenüber, und
    ebenso die mit der Ausgabe null. Die Verbindungsstrecken kreuzen sich,
    die konvexen Hüllen überschneiden sich also, und keine Gerade kann
    dazwischen liegen.
    """
    positive = [inputs for inputs, value in XNOR.items() if value]
    negative = [inputs for inputs, value in XNOR.items() if not value]
    distance = support_vector_machines.hull_distance(
        [tuple(float(v) for v in point) for point in positive],
        [tuple(float(v) for v in point) for point in negative])
    return {"positive": positive, "negative": negative,
            "hull distance": distance, "separable": distance > 1e-6}
