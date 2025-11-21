"""Lloyds Algorithmus für das visuelle Vokabular."""

import numpy as np


def _data(points):
    """Prüft eine Punktmenge.

    Raises:
        ValueError: bei einer leeren oder falsch geformten Menge.
    """
    field = np.asarray(points, dtype=float)
    if field.ndim != 2 or field.shape[0] == 0:
        raise ValueError("leere oder falsch geformte Punktmenge")
    return field


def assign(points, centroids):
    """Ordnet jeden Punkt seinem nächsten Zentroiden zu.

    Das ist die Nächster-Nachbar-Bedingung von der Folie: bei festen
    Zentroiden lässt sich der Quantisierungsfehler nicht kleiner machen
    als durch diese Zuordnung.

    Raises:
        ValueError: bei einer leeren Menge von Zentroiden.
    """
    field = _data(points)
    centres = _data(centroids)
    if centres.shape[1] != field.shape[1]:
        raise ValueError("Punkte und Zentroide haben verschiedene Längen")
    measured = ((field[:, None, :] - centres[None, :, :]) ** 2).sum(axis=2)
    return np.argmin(measured, axis=1), measured


def quantisation_error(points, centroids, assignment=None):
    """Misst den mittleren quadratischen Abstand zum Zentroiden.

    Raises:
        ValueError: bei einer leeren Menge.
    """
    field = _data(points)
    centres = _data(centroids)
    if assignment is None:
        assignment, _ = assign(field, centres)
    taken = centres[np.asarray(assignment)]
    return float(np.mean(np.sum((field - taken) ** 2, axis=1)))


def cluster(points, k=8, seed=0, iterations=100):
    """Führt Lloyds Algorithmus aus.

    Die beiden Schritte wechseln sich ab: zuerst wird jeder Punkt seinem
    nächsten Zentroiden zugeordnet, dann wird jeder Zentroid auf den
    Mittelwert seiner Punkte gesetzt. Keiner der beiden Schritte kann den
    Fehler vergrössern, deshalb fällt er monoton und das Verfahren hält
    an. Dass es dabei im besten Punkt landet, folgt daraus nicht.

    Args:
        points: die Deskriptoren.
        k: die Grösse des Vokabulars.
        seed: der Startwert für die Auswahl der ersten Zentroide.
        iterations: die Obergrenze der Durchläufe.

    Returns:
        Abbildung mit den Zentroiden, der Zuordnung und dem Verlauf des
        Fehlers.

    Raises:
        ValueError: bei einem nicht positiven k oder mehr Zentroiden als
            Punkten.
    """
    field = _data(points)
    if k <= 0:
        raise ValueError("k muss positiv sein")
    if k > field.shape[0]:
        raise ValueError("mehr Zentroide als Punkte")
    rng = np.random.default_rng(seed)
    chosen = rng.choice(field.shape[0], size=k, replace=False)
    centres = field[chosen].copy()
    errors = []
    assignment = None
    converged = False
    for _ in range(iterations):
        new_assignment, _ = assign(field, centres)
        errors.append(quantisation_error(field, centres, new_assignment))
        if assignment is not None and np.array_equal(assignment,
                                                     new_assignment):
            converged = True
            break
        assignment = new_assignment
        for index in range(k):
            inside = field[assignment == index]
            if len(inside):
                centres[index] = inside.mean(axis=0)
    return {"centroids": centres, "assignment": list(assignment),
            "error": errors[-1], "error per iteration": errors,
            "converged": converged, "iterations": len(errors)}


def best_of(points, k=8, restarts=10, iterations=100):
    """Startet mehrfach und behält den besten Durchlauf.

    Raises:
        ValueError: wie bei ``cluster``.
    """
    if restarts < 1:
        raise ValueError("mindestens ein Durchlauf")
    best = None
    for seed in range(restarts):
        report = cluster(points, k, seed, iterations)
        if best is None or report["error"] < best["error"]:
            best = report
    best["restarts"] = restarts
    return best


def the_local_optimum(seed=21):
    """Zeigt, dass der Startpunkt das Ergebnis bestimmt.

    Vier Häufungen, drei gesuchte Zentroide: je nachdem, wo die
    Zentroide beginnen, werden zwei Häufungen zusammengefasst oder eine
    Häufung geteilt, und die Fehler unterscheiden sich deutlich. Das
    Verfahren hat in beiden Fällen einen Punkt erreicht, an dem sich
    nichts mehr bewegt.

    Returns:
        Abbildung mit den Fehlern aller Startpunkte.
    """
    rng = np.random.default_rng(seed)
    data = np.vstack([rng.normal(size=(30, 2)) * 0.4 + centre
                      for centre in ([0.0, 0.0], [6.0, 0.0], [0.0, 6.0],
                                     [6.0, 6.0])])
    errors = [round(cluster(data, k=3, seed=start)["error"], 6)
              for start in range(12)]
    return {"errors": errors, "best": min(errors), "worst": max(errors),
            "spread": max(errors) - min(errors),
            "why": "beide Ergebnisse sind Punkte, an denen sich nichts "
                   "mehr bewegt",
            "the remedy": "mehrfach starten und den besten behalten"}


def what_the_vocabulary_size_decides():
    """Sagt, was an k hängt.

    Wenige Zentroide fassen verschiedene Formen zusammen und machen
    Bilder ähnlicher, als sie sind. Viele Zentroide trennen fein, aber
    zwei Abbilder desselben Worts landen dann leicht in verschiedenen
    Klassen, und das Histogramm wird dünn besetzt. Die Grösse ist damit
    dasselbe Problem wie k bei den Nachbarn: sie lässt sich nur an der
    eigentlichen Aufgabe messen.
    """
    return {"small": "verschiedene Formen fallen zusammen",
            "large": "dasselbe Wort landet in verschiedenen Klassen",
            "the histogram": "wird bei grossem k dünn besetzt",
            "how to choose": "an der eigentlichen Aufgabe messen"}
