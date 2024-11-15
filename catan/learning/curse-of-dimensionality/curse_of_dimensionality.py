"""Was in vielen Dimensionen mit den Abständen geschieht."""

import math

import numpy as np


def distance_spread(dimensions=(1, 2, 5, 10, 50, 100), points=500,
                    seed=0):
    """Misst, wie sich der nächste und der fernste Punkt annähern.

    Gezogen werden Punkte gleichverteilt im Würfel, gemessen wird vom
    Ursprung aus der kleinste und der grösste Abstand. In einer
    Dimension liegen sie weit auseinander; in hundert Dimensionen ist
    ihr Verhältnis fast eins.

    Damit verliert der Begriff des nächsten Nachbarn seinen Sinn: wenn
    alle Punkte gleich weit weg sind, ist der nächste keine Auszeichnung
    mehr.

    Returns:
        Liste mit einer Zeile je Dimension.

    Raises:
        ValueError: bei zu wenigen Punkten.
    """
    if points < 2:
        raise ValueError("es braucht mindestens zwei Punkte")
    rng = np.random.default_rng(seed)
    found = []
    for dimension in dimensions:
        cloud = rng.uniform(0.0, 1.0, size=(points, dimension))
        measured = np.sqrt((cloud ** 2).sum(axis=1))
        near = float(measured.min())
        far = float(measured.max())
        found.append({"dimension": dimension, "nearest": near,
                      "farthest": far,
                      "relative spread": (far - near) / near})
    return found


def ball_volume(dimension):
    """Rechnet das Volumen der Einheitskugel über die Rekursion aus.

    Aus dem Volumen in d minus zwei Dimensionen folgt das in d durch
    Multiplikation mit zwei Pi durch d. Die Rekursion beginnt bei zwei
    für die Strecke und bei Pi für den Kreis und kommt ohne die
    Gammafunktion aus. Dass sie mit der geschlossenen Form
    übereinstimmt, ist die Probe.

    Raises:
        ValueError: bei einer nicht positiven Dimension.
    """
    if dimension <= 0:
        raise ValueError("die Dimension muss positiv sein")
    if dimension == 1:
        return 2.0
    if dimension == 2:
        return math.pi
    return 2.0 * math.pi / dimension * ball_volume(dimension - 2)


def ball_volume_by_sampling(dimension, samples=200000, seed=0):
    """Schätzt dasselbe Volumen durch Zählen im Würfel.

    Der Anteil der Punkte, die in die Kugel fallen, mal dem Volumen des
    Würfels. Ab etwa zehn Dimensionen trifft kaum ein Punkt mehr, und
    die Schätzung wird unbrauchbar. Genau das ist der Fluch, hier von
    der praktischen Seite: eine Stichprobe reicht nicht mehr aus, um den
    Raum zu füllen.

    Raises:
        ValueError: bei einer nicht positiven Dimension oder Stichprobe.
    """
    if dimension <= 0 or samples <= 0:
        raise ValueError("Dimension und Stichprobe müssen positiv sein")
    rng = np.random.default_rng(seed)
    cloud = rng.uniform(-1.0, 1.0, size=(samples, dimension))
    inside = float(np.mean((cloud ** 2).sum(axis=1) <= 1.0))
    return {"estimate": inside * 2.0 ** dimension,
            "exact": ball_volume(dimension), "hits": inside * samples,
            "usable": inside * samples > 100}


def ball_volume_by_formula(dimension):
    """Rechnet das Volumen der Einheitskugel mit der Gammafunktion aus.

    Raises:
        ValueError: bei einer nicht positiven Dimension.
    """
    if dimension <= 0:
        raise ValueError("die Dimension muss positiv sein")
    return math.pi ** (dimension / 2.0) / math.gamma(dimension / 2.0
                                                     + 1.0)


def ball_share(dimension):
    """Nennt den Anteil des Würfels, den die einbeschriebene Kugel füllt.

    In zwei Dimensionen sind es rund achtundsiebzig Prozent, in zehn
    noch zweieinhalb Promille, in zwanzig weniger als ein Millionstel.
    Das Volumen sitzt in den Ecken, und ein Würfel hat in d Dimensionen
    zwei hoch d davon.

    Raises:
        ValueError: bei einer nicht positiven Dimension.
    """
    if dimension <= 0:
        raise ValueError("die Dimension muss positiv sein")
    return ball_volume_by_formula(dimension) / 2.0 ** dimension


def shell(inner=0.9, dimensions=(1, 2, 3, 5, 10, 20, 50, 100, 200)):
    """Misst, wie viel des Kugelvolumens in der äusseren Schale liegt.

    Raises:
        ValueError: bei einem Radius ausserhalb von null bis eins.
    """
    if not 0.0 < inner < 1.0:
        raise ValueError("der innere Radius liegt zwischen null und eins")
    return [{"dimension": dimension,
             "share in the shell": 1.0 - inner ** dimension,
             "inner radius": inner}
            for dimension in dimensions]


def intrinsic_dimension(points=400, seed=1):
    """Zeigt, dass die Darstellung mehr Dimensionen haben kann als die Daten.

    Eine Kurve im hundertdimensionalen Raum bleibt eine Kurve: die Daten
    liegen auf einer eindimensionalen Menge, auch wenn jeder Punkt durch
    hundert Zahlen beschrieben wird. Die Eigenwerte der Kovarianzmatrix
    zeigen das sofort, und darauf beruht jede Reduktion.

    Returns:
        Abbildung mit beiden Zahlen.
    """
    rng = np.random.default_rng(seed)
    line = rng.uniform(-1.0, 1.0, size=(points, 1))
    mix = rng.normal(size=(1, 100))
    cloud = line @ mix + rng.normal(size=(points, 100)) * 1e-6
    centred = cloud - cloud.mean(axis=0)
    values = np.linalg.eigvalsh((centred.T @ centred) / points)[::-1]
    kept = float(values[0] / values.sum())
    return {"representation": cloud.shape[1],
            "intrinsic": int(np.sum(values > values[0] * 1e-6)),
            "share on the first axis": kept,
            "why it matters": "der Fluch trifft die Darstellung, nicht "
                              "die Daten"}


def what_the_curse_actually_breaks():
    """Nennt, was in vielen Dimensionen nicht mehr funktioniert.

    Der nächste Nachbar verliert seine Bedeutung, weil alle Abstände
    zusammenrücken. Indexstrukturen verlieren ihren Nutzen, weil eine
    kleine Änderung des Suchradius plötzlich fast alle Punkte umfasst.
    Und der Raum wird so leer, dass jede Stichprobe dünn ist: um die
    Dichte einer Stichprobe zu halten, müsste ihre Grösse mit der
    Dimension exponentiell wachsen.

    Was nicht bricht: Verfahren, die auf der wirklichen, meist viel
    kleineren Dimension der Daten arbeiten.
    """
    return {"breaks": ["der nächste Nachbar", "die Indexstrukturen",
                       "die Dichte jeder Stichprobe"],
            "survives": "was auf der wirklichen Dimension arbeitet",
            "why the radius matters": "ein kleiner Unterschied im "
                                      "Suchradius ändert die Laufzeit "
                                      "gewaltig"}
