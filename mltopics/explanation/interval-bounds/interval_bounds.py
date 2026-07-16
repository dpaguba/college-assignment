"""Formale Schranken für ein kleines Netz."""

import numpy as np

CENTRE = np.array([0.3, -0.2])


def example_network(depth=2, width=4, seed=0):
    """Baut ein kleines Netz mit Gleichrichtern zwischen den Schichten.

    Raises:
        ValueError: bei einer nicht positiven Tiefe oder Breite.
    """
    if depth < 1 or width < 1:
        raise ValueError("Tiefe und Breite müssen positiv sein")
    rng = np.random.default_rng(seed)
    sizes = [2] + [width] * (depth - 1) + [1]
    return [{"weights": rng.normal(size=(one, two)) / np.sqrt(one),
             "bias": rng.normal(size=two) * 0.1}
            for one, two in zip(sizes, sizes[1:])]


def forward(network, point):
    """Rechnet das Netz für einen Punkt aus."""
    values = np.asarray(point, dtype=float)
    for index, layer in enumerate(network):
        values = values @ layer["weights"] + layer["bias"]
        if index < len(network) - 1:
            values = np.maximum(values, 0.0)
    return values


def propagate(network, radius=0.1, centre=None):
    """Schiebt ein Intervall durch das Netz.

    Für eine lineare Schicht ist die Schranke ausrechenbar: die untere
    Grenze entsteht, indem jedes positive Gewicht die untere und jedes
    negative die obere Eingangsgrenze nimmt. Der Gleichrichter schneidet
    beide Grenzen bei null ab.

    Das Ergebnis ist immer korrekt, also enthält es alle möglichen
    Ausgaben. Genau zu sein verspricht es nicht: sobald ein Wert in
    zwei Schichten auftaucht, behandelt die Rechnung ihn als zwei
    unabhängige Grössen, und der Bereich wird zu breit.

    Args:
        network: die Schichten.
        radius: die halbe Kantenlänge des Eingangswürfels.
        centre: der Mittelpunkt.

    Returns:
        Abbildung mit den Grenzen.

    Raises:
        ValueError: bei einem negativen Radius oder einem leeren Netz.
    """
    if not network:
        raise ValueError("leeres Netz")
    if radius < 0.0:
        raise ValueError("der Radius darf nicht negativ sein")
    middle = CENTRE if centre is None else np.asarray(centre, dtype=float)
    lower = middle - radius
    upper = middle + radius
    for index, layer in enumerate(network):
        weights = layer["weights"]
        positive = np.maximum(weights, 0.0)
        negative = np.minimum(weights, 0.0)
        new_lower = lower @ positive + upper @ negative + layer["bias"]
        new_upper = upper @ positive + lower @ negative + layer["bias"]
        lower, upper = new_lower, new_upper
        if index < len(network) - 1:
            lower = np.maximum(lower, 0.0)
            upper = np.maximum(upper, 0.0)
    return {"lower": lower, "upper": upper, "radius": radius,
            "width": float(np.max(upper - lower))}


def check_by_sampling(network=None, radius=0.1, draws=20000, seed=0):
    """Prüft die Schranke gegen viele Punkte aus dem Würfel.

    Gefunden werden kann damit nur eine falsche Schranke, nie eine
    bewiesen richtige. Für einen Fehler im Vorzeichen genügt es
    trotzdem: der wird sofort verletzt.

    Returns:
        Abbildung mit der Schranke, dem gemessenen Bereich und dem
        Urteil.

    Raises:
        ValueError: bei einem negativen Radius.
    """
    network = example_network() if network is None else network
    report = propagate(network, radius)
    rng = np.random.default_rng(seed)
    points = CENTRE + rng.uniform(-radius, radius, size=(draws, 2))
    values = np.array([float(forward(network, point)[0])
                       for point in points])
    return {"bound lower": float(report["lower"][0]),
            "bound upper": float(report["upper"][0]),
            "sampled lower": float(values.min()),
            "sampled upper": float(values.max()),
            "bound width": float(report["upper"][0] - report["lower"][0]),
            "sampled width": float(values.max() - values.min()),
            "sound": bool(values.min() >= report["lower"][0] - 1e-9
                          and values.max() <= report["upper"][0] + 1e-9),
            "draws": draws}


def one_layer_is_exact(radius=0.2, seed=1):
    """Zeigt, dass die Schranke bei einer Schicht scharf ist.

    Ohne Gleichrichter und ohne zweite Schicht taucht jeder Eingang
    genau einmal auf, und die Grenzen werden an den Ecken des Würfels
    angenommen. Die Schranke ist dann keine Näherung, sondern der
    Bereich selbst.

    Returns:
        Abbildung mit dem Abstand zwischen Schranke und Wirklichkeit.
    """
    rng = np.random.default_rng(seed)
    network = [{"weights": rng.normal(size=(2, 1)),
                "bias": rng.normal(size=1)}]
    report = propagate(network, radius)
    corners = [CENTRE + np.array([first, second]) * radius
               for first in (-1.0, 1.0) for second in (-1.0, 1.0)]
    values = [float(forward(network, corner)[0]) for corner in corners]
    return {"bound": (float(report["lower"][0]),
                      float(report["upper"][0])),
            "true": (min(values), max(values)),
            "gap": abs(float(report["upper"][0]) - max(values))
            + abs(float(report["lower"][0]) - min(values))}


def over_depth(depths=(1, 2, 3, 5, 8), radius=0.1, draws=6000, seed=2):
    """Misst, wie die Schranke mit der Tiefe schlechter wird.

    Jede Schicht bietet eine weitere Gelegenheit, denselben Wert zweimal
    unabhängig zu behandeln. Verglichen wird deshalb nicht der
    Unterschied der Breiten, sondern ihr Verhältnis: die Netze haben je
    Tiefe eine andere Grössenordnung, und ein Unterschied von einem
    Tausendstel bedeutet bei einer Breite von einem Zehntel etwas
    anderes als bei einer von einem Zehntausendstel.

    Die abgetastete Breite ist dabei selbst zu klein, denn eine
    Stichprobe trifft die Ecken des Würfels nur zufällig. Das Verhältnis
    ist damit eine Untergrenze für die Unschärfe.

    Returns:
        Liste mit einer Zeile je Tiefe.
    """
    found = []
    for depth in depths:
        network = example_network(depth=max(1, depth), seed=seed)
        report = check_by_sampling(network, radius, draws, seed)
        found.append({"depth": depth,
                      "bound width": report["bound width"],
                      "sampled width": report["sampled width"],
                      "looseness": report["bound width"]
                      / max(report["sampled width"], 1e-12)})
    return found


def sound_but_useless(radius=2.0, draws=6000, seed=3):
    """Zeigt eine Schranke, die richtig ist und nichts entscheidet.

    Bei einem grossen Eingangsbereich und mehreren Schichten enthält
    die Schranke sowohl positive als auch negative Werte. Sie ist damit
    korrekt und beantwortet die Frage, ob die Ausgabe immer positiv
    bleibt, mit einem Achselzucken.

    Das ist der Normalfall und der Grund, warum an schärferen Verfahren
    gearbeitet wird: die Korrektheit ist billig zu haben, die Schärfe
    nicht.

    Returns:
        Abbildung mit der Schranke und dem Urteil.
    """
    network = example_network(depth=4, width=6, seed=seed)
    report = check_by_sampling(network, radius, draws, seed)
    low, high = report["bound lower"], report["bound upper"]
    return {"bound": (low, high), "sound": report["sound"],
            "decides anything": bool(low > 0.0 or high < 0.0),
            "sampled": (report["sampled lower"],
                        report["sampled upper"]),
            "why": "die Korrektheit ist billig, die Schärfe nicht"}


def what_a_bound_is_worth():
    """Sagt, wofür eine korrekte Schranke steht.

    Sie ist eine Aussage über alle Eingaben im Würfel, nicht über die
    getesteten. Damit unterscheidet sie sich grundsätzlich von jeder
    Messung: ein Gegenbeispiel widerlegt sie, aber keine Zahl von
    Versuchen bestätigt sie.

    Der Preis ist, dass sie zu breit ausfällt, und die ganze Arbeit an
    solchen Verfahren besteht darin, sie schmaler zu machen, ohne die
    Korrektheit aufzugeben.
    """
    return {"what it covers": "alle Eingaben im Würfel",
            "how it differs from a test": "kein Versuch bestätigt sie, "
                                          "ein Gegenbeispiel widerlegt "
                                          "sie",
            "the price": "sie fällt zu breit aus",
            "the work": "sie schmaler machen, ohne die Korrektheit "
                        "aufzugeben"}
