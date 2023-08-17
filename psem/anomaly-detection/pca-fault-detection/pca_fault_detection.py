"""Fehlerhafte Sensoren über die Hauptkomponenten finden."""

import math
import random


def covariance(rows):
    """Die Kovarianzmatrix einer Datenmatrix.

    Raises:
        ValueError: bei weniger als zwei Zeilen oder ungleichen Längen.
    """
    if len(rows) < 2:
        raise ValueError("mindestens zwei Zeilen")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("die Zeilen sind verschieden lang")
    means = [sum(row[index] for row in rows) / len(rows)
             for index in range(width)]
    matrix = [[0.0] * width for _ in range(width)]
    for row in rows:
        for first in range(width):
            for second in range(width):
                matrix[first][second] += ((row[first] - means[first])
                                          * (row[second] - means[second]))
    count = len(rows) - 1
    return [[value / count for value in line] for line in matrix]


def eigen(matrix, sweeps=100):
    """Zerlegt eine symmetrische Matrix mit dem Verfahren von Jacobi.

    Gedreht wird jeweils um das grösste Element ausserhalb der
    Diagonale, bis nichts mehr übrig ist. Für kleine Matrizen ist das
    genau genug und braucht nichts ausser der Standardbibliothek.

    Args:
        matrix: eine symmetrische Matrix.
        sweeps: obere Schranke der Durchgänge.

    Returns:
        Paar aus den Eigenwerten und den Eigenvektoren als Spalten,
        absteigend nach Eigenwert sortiert.

    Raises:
        ValueError: bei einer nicht quadratischen Matrix.
    """
    size = len(matrix)
    if any(len(line) != size for line in matrix):
        raise ValueError("die Matrix ist nicht quadratisch")
    values = [list(line) for line in matrix]
    vectors = [[1.0 if first == second else 0.0 for second in range(size)]
               for first in range(size)]
    for _ in range(sweeps):
        first, second, largest = 0, 1, 0.0
        for row in range(size):
            for column in range(row + 1, size):
                if abs(values[row][column]) > largest:
                    first, second = row, column
                    largest = abs(values[row][column])
        if largest < 1e-12:
            break
        difference = values[second][second] - values[first][first]
        if abs(difference) < 1e-18:
            angle = math.pi / 4
        else:
            angle = 0.5 * math.atan2(2 * values[first][second], difference)
        cosine, sine = math.cos(angle), math.sin(angle)
        for index in range(size):
            left = values[index][first]
            right = values[index][second]
            values[index][first] = cosine * left - sine * right
            values[index][second] = sine * left + cosine * right
        for index in range(size):
            left = values[first][index]
            right = values[second][index]
            values[first][index] = cosine * left - sine * right
            values[second][index] = sine * left + cosine * right
        for index in range(size):
            left = vectors[index][first]
            right = vectors[index][second]
            vectors[index][first] = cosine * left - sine * right
            vectors[index][second] = sine * left + cosine * right
    pairs = sorted(((values[index][index],
                     [vectors[row][index] for row in range(size)])
                    for index in range(size)), key=lambda pair: -pair[0])
    return [value for value, _ in pairs], [vector for _, vector in pairs]


def model(rows, components):
    """Baut das Hauptkomponentenmodell einer Datenmatrix.

    Raises:
        ValueError: bei einer unzulässigen Zahl von Komponenten.
    """
    width = len(rows[0])
    if not 1 <= components < width:
        raise ValueError("die Zahl der Komponenten liegt zwischen eins "
                         "und der Zahl der Sensoren minus eins")
    means = [sum(row[index] for row in rows) / len(rows)
             for index in range(width)]
    eigenvalues, eigenvectors = eigen(covariance(rows))
    return {"means": means, "loadings": eigenvectors[:components],
            "eigenvalues": eigenvalues, "components": components,
            "sensors": width}


def reconstruct(built, row):
    """Bildet eine Messung auf den Hauptunterraum ab und zurück.

    Raises:
        ValueError: bei einer Zeile falscher Länge.
    """
    if len(row) != built["sensors"]:
        raise ValueError("die Zeile hat die falsche Länge")
    centred = [value - mean for value, mean in zip(row, built["means"])]
    rebuilt = [0.0] * built["sensors"]
    for vector in built["loadings"]:
        score = sum(centred[index] * vector[index]
                    for index in range(built["sensors"]))
        for index in range(built["sensors"]):
            rebuilt[index] += score * vector[index]
    return [value + mean for value, mean in zip(rebuilt, built["means"])]


def squared_error(built, row):
    """Der quadratische Rest zwischen Messung und Rekonstruktion.

    Das ist die Grösse, die der Aufsatz Q oder SPE nennt. Im Normalfall
    liegen die Messungen fast im Hauptunterraum und der Rest ist klein;
    ein Sensorfehler bricht die Korrelation, die Messung verlässt den
    Unterraum, und der Rest wächst.

    Raises:
        ValueError: bei einer Zeile falscher Länge.
    """
    rebuilt = reconstruct(built, row)
    return sum((value - other) ** 2 for value, other in zip(row, rebuilt))


def correlated_data(count=200, seed=0, noise=0.05):
    """Zieht Messungen von vier Sensoren mit zwei Ursachen.

    Zwei verborgene Grössen erzeugen vier Messwerte; die Sensoren sind
    deshalb stark korreliert, und zwei Hauptkomponenten genügen. Genau
    diese Redundanz macht die Fehlererkennung möglich: ein einzelner
    Sensor kann von den anderen aus vorhergesagt werden.

    Raises:
        ValueError: bei einer zu kleinen Zahl.
    """
    if count < 10:
        raise ValueError("zu wenige Messungen")
    generator = random.Random(seed)
    rows = []
    for _ in range(count):
        first = generator.gauss(0.0, 1.0)
        second = generator.gauss(0.0, 1.0)
        rows.append((first + generator.gauss(0.0, noise),
                     2 * first + generator.gauss(0.0, noise),
                     second + generator.gauss(0.0, noise),
                     first - second + generator.gauss(0.0, noise)))
    return rows


def detect_fault(sensor=1, offset=1.0, count=200, seed=0):
    """Legt einen Sensorfehler auf und misst, ob er auffällt.

    Der Fehler ist ein fester Versatz auf einem Sensor. Bei einem
    Versatz von eins bleibt der Wert im normalen Bereich des Sensors und
    passt trotzdem nicht mehr zu den anderen; genau diesen Fall nennt
    der Aufsatz als den, den Grenzwerte je Sensor nicht finden.

    Gemessen wird: im gesunden Betrieb liegt der grösste Rest bei 0.035,
    bei einem Versatz von 0.5 schon bei 0.096 und bei einem von eins bei
    0.33. Der Fehler wird also weit unterhalb der Grenzwerte sichtbar.

    Returns:
        Abbildung mit dem Rest vor und nach dem Fehler.

    Raises:
        ValueError: bei einem unbekannten Sensor.
    """
    rows = correlated_data(count, seed)
    built = model(rows, components=2)
    if not 0 <= sensor < built["sensors"]:
        raise ValueError("unbekannter Sensor")
    healthy = [squared_error(built, row) for row in rows]
    limit = max(healthy)
    faulty = list(rows[0])
    faulty[sensor] += offset
    low = min(row[sensor] for row in rows)
    high = max(row[sensor] for row in rows)
    return {"mean error when healthy": sum(healthy) / len(healthy),
            "largest error when healthy": limit,
            "error with the fault": squared_error(built, faulty),
            "detected": squared_error(built, faulty) > limit,
            "value stays in the normal range": low <= faulty[sensor] <= high,
            "why": "der Wert ist für sich normal und passt nicht zu den "
                   "anderen"}


def blame(built, row):
    """Nennt den Sensor, dessen Rekonstruktion den Rest am meisten senkt.

    Der Aufsatz rekonstruiert jeden Sensor der Reihe nach aus den
    anderen und sieht nach, bei welchem der Rest dadurch am stärksten
    fällt.

    Raises:
        ValueError: bei einer Zeile falscher Länge.
    """
    base = squared_error(built, row)
    drops = {}
    for candidate in range(built["sensors"]):
        repaired = list(row)
        repaired[candidate] = reconstruct(built, row)[candidate]
        drops[candidate] = base - squared_error(built, repaired)
    return max(drops, key=lambda index: drops[index]), drops


def identify_fault(offset=1.0, count=200, seed=0):
    """Prüft für jeden Sensor, ob der Fehler ihm zugeordnet wird.

    Hier hört die Sache auf, glatt zu sein. Erkannt wird jeder Fehler,
    zugeordnet nicht: von den vier Sensoren werden zwei richtig
    benannt und zwei ihrem Partner zugeschrieben. Der Grund liegt in
    den Daten. Sensor eins misst das Doppelte von Sensor null, also
    zeigt ein Versatz auf dem einen in dieselbe Richtung des
    Restraums wie ein Versatz auf dem anderen, nur anders skaliert.
    Dasselbe gilt für die Sensoren zwei und drei, weil der vierte
    Messwert die Differenz der beiden verborgenen Grössen ist.

    Das ist keine Schwäche der Rechnung, sondern die
    Identifizierbarkeitsbedingung des Aufsatzes: unterscheidbar sind
    zwei Fehler nur, wenn ihre Richtungen im Restraum verschieden sind.
    Bei vier Sensoren und zwei Komponenten ist der Restraum
    zweidimensional, und vier Richtungen passen nicht unterscheidbar
    hinein.

    Returns:
        Abbildung vom eingelegten Sensor auf den benannten.
    """
    rows = correlated_data(count, seed)
    built = model(rows, components=2)
    found = {}
    for sensor in range(built["sensors"]):
        faulty = list(rows[0])
        faulty[sensor] += offset
        named, _ = blame(built, faulty)
        found[sensor] = named
    return {"identified": found,
            "correct": sorted(sensor for sensor, named in found.items()
                              if sensor == named),
            "confused": sorted(sensor for sensor, named in found.items()
                               if sensor != named),
            "why": "zwei Fehlerrichtungen fallen im zweidimensionalen "
                   "Restraum zusammen",
            "condition": "unterscheidbar nur bei verschiedenen Richtungen "
                         "im Restraum"}


def detection_against_identification():
    """Trennt die beiden Aufgaben, die leicht verwechselt werden.

    Erkennen heisst festzustellen, dass etwas nicht stimmt, und dafür
    genügt ein Rest über der Schranke. Zuordnen heisst zu sagen, welcher
    Sensor es ist, und das verlangt mehr: die Fehlerrichtungen müssen im
    Restraum auseinanderliegen. Ein System kann jeden Fehler zuverlässig
    erkennen und keinen zuverlässig zuordnen, und dieses hier tut genau
    das.

    Returns:
        Abbildung mit beiden Befunden.
    """
    detected = all(detect_fault(sensor=sensor)["detected"]
                   for sensor in range(4))
    report = identify_fault()
    return {"every fault detected": detected,
            "correctly identified": len(report["correct"]),
            "of": len(report["identified"]),
            "lesson": "Erkennung braucht Redundanz, Zuordnung braucht "
                      "unterscheidbare Richtungen"}
