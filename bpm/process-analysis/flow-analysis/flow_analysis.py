"""Durchlaufzeitanalyse: die Zykluszeit eines Prozessmodells."""

import random


def task(name, cycle, work=None):
    """Ein Block für eine einzelne Aktivität.

    Args:
        name: der Name der Aktivität.
        cycle: die Durchlaufzeit.
        work: die theoretische Bearbeitungszeit; ohne Angabe gleich der
            Durchlaufzeit.

    Raises:
        ValueError: bei einer negativen Zeit.
    """
    if cycle < 0 or (work is not None and work < 0):
        raise ValueError("negative Zeit")
    return {"type": "task", "name": name, "cycle": cycle,
            "work": cycle if work is None else work}


def sequence(parts):
    """Ein Block, dessen Teile nacheinander laufen.

    Raises:
        ValueError: bei einer leeren Folge.
    """
    if not parts:
        raise ValueError("leere Folge")
    return {"type": "sequence", "parts": list(parts)}


def parallel(parts):
    """Ein Block, dessen Teile gleichzeitig laufen.

    Raises:
        ValueError: bei weniger als zwei Zweigen.
    """
    if len(parts) < 2:
        raise ValueError("mindestens zwei Zweige")
    return {"type": "parallel", "parts": list(parts)}


def choice(branches):
    """Ein Block, von dem genau ein Zweig läuft.

    Args:
        branches: Paare aus Wahrscheinlichkeit und Block.

    Raises:
        ValueError: wenn die Wahrscheinlichkeiten nicht eins ergeben.
    """
    total = sum(probability for probability, _ in branches)
    if abs(total - 1.0) > 1e-9:
        raise ValueError("die Wahrscheinlichkeiten ergeben nicht eins")
    return {"type": "choice", "branches": [(float(probability), block)
                                           for probability, block in branches]}


def inclusive(parts, cases):
    """Ein Block, von dem eine nicht leere Auswahl der Zweige läuft.

    Args:
        parts: die Zweige.
        cases: Paare aus Wahrscheinlichkeit und den Nummern der Zweige,
            die in diesem Fall laufen.

    Raises:
        ValueError: bei einer leeren Auswahl, einer unbekannten Nummer
            oder wenn die Wahrscheinlichkeiten nicht eins ergeben.
    """
    total = sum(probability for probability, _ in cases)
    if abs(total - 1.0) > 1e-9:
        raise ValueError("die Wahrscheinlichkeiten ergeben nicht eins")
    for _, chosen in cases:
        if not chosen:
            raise ValueError("eine leere Auswahl ist nicht möglich")
        for index in chosen:
            if not 0 <= index < len(parts):
                raise ValueError("unbekannter Zweig")
    return {"type": "inclusive", "parts": list(parts),
            "cases": [(float(probability), tuple(chosen))
                      for probability, chosen in cases]}


def loop(body, repeat):
    """Ein Block, der sich mit einer Wahrscheinlichkeit wiederholt.

    Der Rumpf läuft mindestens einmal und danach mit der angegebenen
    Wahrscheinlichkeit erneut; im Mittel also 1/(1 − r) mal.

    Raises:
        ValueError: bei einer Wahrscheinlichkeit ausserhalb von null bis
            unter eins.
    """
    if not 0.0 <= repeat < 1.0:
        raise ValueError("die Wiederholung liegt ausserhalb von 0 bis unter 1")
    return {"type": "loop", "body": body, "repeat": float(repeat)}


def _measure(block, field):
    """Rechnet eine Zeit über die Blockstruktur aus.

    Raises:
        ValueError: bei einem unbekannten Block.
    """
    kind = block.get("type")
    if kind == "task":
        return block[field]
    if kind == "sequence":
        return sum(_measure(part, field) for part in block["parts"])
    if kind == "parallel":
        return max(_measure(part, field) for part in block["parts"])
    if kind == "choice":
        return sum(probability * _measure(part, field)
                   for probability, part in block["branches"])
    if kind == "inclusive":
        return sum(probability * max(_measure(block["parts"][index], field)
                                     for index in chosen)
                   for probability, chosen in block["cases"])
    if kind == "loop":
        return _measure(block["body"], field) / (1.0 - block["repeat"])
    raise ValueError("unbekannter Block")


def cycle_time(block):
    """Die mittlere Zykluszeit eines Blocks.

    Raises:
        ValueError: bei einem unbekannten Block.
    """
    return _measure(block, "cycle")


def work_time(block):
    """Die theoretische Bearbeitungszeit eines Blocks.

    Gerechnet wird über dieselbe Struktur wie die Zykluszeit, nur mit den
    Bearbeitungszeiten; der parallele Block nimmt also auch hier das
    Maximum und nicht die Summe.

    Raises:
        ValueError: bei einem unbekannten Block.
    """
    return _measure(block, "work")


def activities(block):
    """Nennt die Aktivitäten eines Blocks in der Reihenfolge des Modells.

    Raises:
        ValueError: bei einem unbekannten Block.
    """
    kind = block.get("type")
    if kind == "task":
        return [block["name"]]
    if kind in ("sequence", "parallel", "inclusive"):
        return [name for part in block["parts"] for name in activities(part)]
    if kind == "choice":
        return [name for _, part in block["branches"]
                for name in activities(part)]
    if kind == "loop":
        return activities(block["body"])
    raise ValueError("unbekannter Block")


def _draw(block, generator, field):
    """Zieht eine einzelne Ausprägung der Zeit eines Blocks."""
    kind = block["type"]
    if kind == "task":
        return block[field]
    if kind == "sequence":
        return sum(_draw(part, generator, field) for part in block["parts"])
    if kind == "parallel":
        return max(_draw(part, generator, field) for part in block["parts"])
    if kind == "choice":
        cut = generator.random()
        seen = 0.0
        for probability, part in block["branches"]:
            seen += probability
            if cut <= seen:
                return _draw(part, generator, field)
        return _draw(block["branches"][-1][1], generator, field)
    if kind == "inclusive":
        cut = generator.random()
        seen = 0.0
        chosen = block["cases"][-1][1]
        for probability, indices in block["cases"]:
            seen += probability
            if cut <= seen:
                chosen = indices
                break
        return max(_draw(block["parts"][index], generator, field)
                   for index in chosen)
    if kind == "loop":
        total = _draw(block["body"], generator, field)
        while generator.random() < block["repeat"]:
            total += _draw(block["body"], generator, field)
        return total
    raise ValueError("unbekannter Block")


def simulate(block, runs=20000, seed=0, field="cycle"):
    """Misst die mittlere Zykluszeit durch Nachspielen einzelner Fälle.

    Die Formeln setzen voraus, dass die Zweige unabhängig gewählt werden
    und die Zeiten fest sind. Die Simulation macht keine dieser Annahmen
    ausser der ersten und dient hier als unabhängige Gegenrechnung.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Durchläufen.
    """
    if runs < 1:
        raise ValueError("mindestens ein Durchlauf")
    generator = random.Random(seed)
    total = 0.0
    for _ in range(runs):
        total += _draw(block, generator, field)
    return total / runs


def loan_application(rework=0.0):
    """Der Darlehensantrag aus Übungsaufgabe 1, Zeiten in Tagen.

    Args:
        rework: Wahrscheinlichkeit, dass das Formular unvollständig ist
            und die Prüfung wiederholt werden muss.
    """
    check = task("Vollständigkeit d. Formulars überprüfen", 1, 2)
    return sequence([
        loop(check, rework) if rework else check,
        parallel([task("Kredithistorie überprüfen", 1, 0.5),
                  task("Einkommensquellen überprüfen", 3, 3)]),
        task("Zulässigkeit beurteilen", 3, 2),
        choice([(0.6, task("Darlehensangebot erstellen", 1, 2)),
                (0.4, task("Antrag ablehnen", 2, 0.5))]),
    ])


def app_release():
    """Der Versionsprozess aus Zettel 4, Zeiten in Stunden.

    In zehn Prozent der Fälle enthält die Version nur neue Funktionen, in
    dreissig Prozent nur behobene Fehler, sonst beides. Das ist ein
    inklusives Gateway: die Fälle sind die möglichen Auswahlen der Zweige.
    """
    return sequence([
        task("Neue Version der App planen", 4),
        inclusive([task("Bugs beheben", 6), task("Features entwickeln", 24)],
                  cases=[(0.1, (1,)), (0.3, (0,)), (0.6, (0, 1))]),
        task("Neue Version der App veröffentlichen", 2),
    ])


def application_form():
    """Die Bewerbung auf eine Abschlussarbeit, Zeiten in Minuten."""
    return sequence([
        task("Titel und Beschreibung der Arbeit angeben", 10),
        choice([(0.8, task("Bachelorarbeit auswählen", 1)),
                (0.2, task("Masterarbeit auswählen", 2))]),
        task("Starttermin, Namen und E-Mail eintragen", 15),
        task("Zustimmung bestätigen", 10),
        parallel([task("Lehrstuhl EC benachrichtigen", 2),
                  task("Im System abspeichern", 5)]),
    ])


def expose():
    """Der Exposé-Prozess aus Zettel 4, Durchlaufzeit in Tagen."""
    return sequence([
        task("Literaturen recherchieren", 2, 4.5),
        task("Exposé schreiben", 4, 14),
        loop(sequence([task("Fehler suchen", 1, 2),
                       task("Exposé überarbeiten", 1, 6)]), 0.2),
    ])
