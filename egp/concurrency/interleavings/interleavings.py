"""Verschränkungen: wie viele Abläufe eine Nebenläufigkeit erlaubt."""

import itertools
import math


def count(lengths):
    """Zählt die Verschränkungen mehrerer Folgen.

    Laufen k Prozesse mit n1, n2, ... Schritten nebeneinander, so ist die
    Zahl der möglichen Abläufe der Multinomialkoeffizient: die Fakultät
    der Gesamtzahl geteilt durch die Fakultäten der einzelnen Zahlen. Die
    Reihenfolge innerhalb eines Prozesses liegt fest, die zwischen ihnen
    nicht.

    Raises:
        ValueError: bei einer negativen Länge.
    """
    if any(length < 0 for length in lengths):
        raise ValueError("negative Länge")
    total = sum(lengths)
    result = math.factorial(total)
    for length in lengths:
        result //= math.factorial(length)
    return result


def enumerate_all(sequences):
    """Zählt die Verschränkungen tatsächlich auf.

    Das dient als Gegenrechnung zur Formel: bei kleinen Eingaben müssen
    beide dieselbe Zahl liefern.

    Raises:
        ValueError: ohne Folgen.
    """
    if not sequences:
        raise ValueError("keine Folgen")
    marks = []
    for index, sequence in enumerate(sequences):
        marks.extend([(index, step) for step in sequence])
    found = set()
    for order in itertools.permutations(marks):
        ok = True
        for index, sequence in enumerate(sequences):
            taken = [step for other, step in order if other == index]
            if taken != list(sequence):
                ok = False
                break
        if ok:
            found.add(tuple(step for _, step in order))
    return sorted(found)


def formula_agrees(sequences):
    """Vergleicht Formel und Aufzählung.

    Returns:
        Abbildung mit beiden Zahlen und dem Urteil.

    Raises:
        ValueError: ohne Folgen.
    """
    listed = enumerate_all(sequences)
    predicted = count([len(sequence) for sequence in sequences])
    return {"by formula": predicted, "by enumeration": len(listed),
            "agree": predicted == len(listed)}


def growth(processes=3, steps=(1, 2, 3, 4, 5)):
    """Zeigt, wie schnell die Zahl der Abläufe wächst.

    Drei Prozesse mit je fünf Schritten haben schon über
    siebenhunderttausend Abläufe. Daran hängt die ganze Schwierigkeit
    des Testens nebenläufiger Programme: einen Fehler, der nur in einem
    dieser Abläufe auftritt, findet kein Test durch Ausprobieren.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Prozessen.
    """
    if processes < 1:
        raise ValueError("mindestens ein Prozess")
    return {length: count([length] * processes) for length in steps}


def why_testing_does_not_find_it():
    """Nennt die Folge für die Praxis.

    Die Zahl der Abläufe wächst schneller als jede Testreihe. Ein Fehler,
    der nur in einer bestimmten Verschränkung auftritt, erscheint in der
    Erprobung nie und im Betrieb irgendwann. Deshalb wird in diesem
    Gebiet gerechnet und nicht ausprobiert: Modellprüfung,
    Bisimulation, Erreichbarkeitsgraphen.
    """
    return {"three processes of five steps": count([5, 5, 5]),
            "tests you would run": "vielleicht tausend",
            "conclusion": "Ausprobieren deckt einen verschwindenden "
                          "Anteil ab",
            "what is done instead": ["Erreichbarkeitsgraph",
                                     "Bisimulation",
                                     "Modellprüfung"]}
