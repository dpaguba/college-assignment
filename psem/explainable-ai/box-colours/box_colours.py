"""Weisse, graue und schwarze Kästen und was die Farbe kostet."""

import random

COLOURS = {
    "white": "das Modell ist als Ganzes lesbar: eine Regel, eine "
             "Gerade, ein flacher Baum",
    "grey": "der Aufbau ist bekannt, das Verhalten nicht mehr im Ganzen "
            "nachvollziehbar",
    "black": "nur Eingabe und Ausgabe sind zugänglich",
}


def colours():
    """Nennt die drei Farben mit ihrer Bedeutung."""
    return dict(COLOURS)


def _data(count, seed=0):
    """Zieht Punkte mit einer nichtlinearen Zielgrösse."""
    generator = random.Random(seed)
    points = []
    for _ in range(count):
        first = generator.uniform(-3.0, 3.0)
        second = generator.uniform(-3.0, 3.0)
        label = 1 if first * second > 0 else 0
        points.append(((first, second), label))
    return points


def stump(points):
    """Baut einen Entscheidungsstumpf: eine Schwelle auf einem Merkmal.

    Das ist der weisseste Kasten, den es gibt: eine Zeile Text erklärt
    ihn vollständig.

    Raises:
        ValueError: bei einer leeren Menge.
    """
    if not points:
        raise ValueError("keine Daten")
    best = None
    for index in (0, 1):
        values = sorted({point[index] for point, _ in points})
        for threshold in values:
            for direction in (True, False):
                correct = sum(1 for point, label in points
                              if ((point[index] > threshold) == direction)
                              == bool(label))
                if best is None or correct > best[0]:
                    best = (correct, index, threshold, direction)
    correct, index, threshold, direction = best
    return {"feature": index, "threshold": threshold,
            "above means one": direction,
            "accuracy": correct / len(points)}


def nearest_neighbour(points, other, neighbours=5):
    """Sagt die Klasse eines Punktes über seine Nachbarn vorher.

    Das ist der schwärzeste Kasten: er hat kein Modell, das sich
    hinschreiben liesse, sondern nur die Daten selbst.

    Raises:
        ValueError: bei einer leeren Menge oder einer nicht positiven
            Nachbarzahl.
    """
    if not points:
        raise ValueError("keine Daten")
    if neighbours < 1:
        raise ValueError("mindestens ein Nachbar")
    ranked = sorted(points,
                    key=lambda row: sum((a - b) ** 2 for a, b
                                        in zip(row[0], other)))
    labels = [label for _, label in ranked[:neighbours]]
    return 1 if sum(labels) * 2 > len(labels) else 0


def compare(count=400, seed=1):
    """Misst, was der weisse Kasten hier kostet.

    Die Zielgrösse ist das Vorzeichen des Produkts zweier Merkmale. Ein
    Stumpf kann das nicht: jede einzelne Schwelle trennt die Ebene in
    zwei Halbebenen, und die gesuchte Menge sind zwei gegenüberliegende
    Quadranten. Er landet deshalb bei der Hälfte. Die Nachbarn schaffen
    es fast vollständig und lassen sich nicht hinschreiben.

    Returns:
        Abbildung mit beiden Trefferquoten.
    """
    training = _data(count, seed)
    testing = _data(count, seed + 1000)
    simple = stump(training)
    index, threshold = simple["feature"], simple["threshold"]
    direction = simple["above means one"]
    stump_correct = sum(
        1 for point, label in testing
        if (((point[index] > threshold) == direction) == bool(label)))
    neighbour_correct = sum(
        1 for point, label in testing
        if nearest_neighbour(training, point) == label)
    return {"stump": stump_correct / len(testing),
            "neighbours": neighbour_correct / len(testing),
            "cost of the white box": (neighbour_correct - stump_correct)
            / len(testing),
            "why": "eine Schwelle trennt Halbebenen, gesucht sind zwei "
                   "gegenüberliegende Quadranten"}


def when_the_white_box_costs_nothing(count=400, seed=1):
    """Zeigt die andere Seite: eine Aufgabe, die der Stumpf löst.

    Ist die Zielgrösse das Vorzeichen eines einzigen Merkmals, so ist
    der Stumpf genau richtig und die Nachbarn haben keinen Vorteil. Die
    Frage ist also nie, ob Erklärbarkeit etwas kostet, sondern ob sie
    bei dieser Aufgabe etwas kostet.

    Returns:
        Abbildung mit beiden Trefferquoten.
    """
    generator = random.Random(seed)
    points = [((generator.uniform(-3, 3), generator.uniform(-3, 3)), None)
              for _ in range(count)]
    training = [(point, 1 if point[0] > 0 else 0) for point, _ in points]
    checking = [((generator.uniform(-3, 3), generator.uniform(-3, 3)), 0)
                for _ in range(count)]
    checking = [(point, 1 if point[0] > 0 else 0) for point, _ in checking]
    simple = stump(training)
    index, threshold = simple["feature"], simple["threshold"]
    direction = simple["above means one"]
    stump_correct = sum(
        1 for point, label in checking
        if (((point[index] > threshold) == direction) == bool(label)))
    neighbour_correct = sum(1 for point, label in checking
                            if nearest_neighbour(training, point) == label)
    return {"stump": stump_correct / len(checking),
            "neighbours": neighbour_correct / len(checking),
            "cost of the white box": (neighbour_correct - stump_correct)
            / len(checking)}


def the_real_question():
    """Nennt, was die Wahl der Farbe entscheidet.

    Nicht die Genauigkeit allein, sondern wer die Entscheidung tragen
    muss. Wo jemand widersprechen können soll, muss die Begründung
    prüfbar sein, und eine nachträgliche Erklärung eines schwarzen
    Kastens ist keine Begründung, sondern eine Vermutung über eine.
    """
    return {"question": "muss jemand der Entscheidung widersprechen "
                        "können",
            "if yes": "die Begründung muss prüfbar sein, nicht nur "
                      "plausibel",
            "post hoc explanation": "eine Vermutung über die Begründung",
            "not the same as": "die Begründung selbst"}
