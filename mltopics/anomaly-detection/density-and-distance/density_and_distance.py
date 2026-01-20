"""Abstand und lokale Dichte als Mass für Auffälligkeit."""

import numpy as np


def _points(data):
    """Prüft eine Punktmenge.

    Raises:
        ValueError: bei einer leeren oder falsch geformten Menge.
    """
    field = np.asarray(data, dtype=float)
    if field.ndim != 2 or field.shape[0] == 0:
        raise ValueError("leere oder falsch geformte Punktmenge")
    return field


def _distances(field):
    """Rechnet alle paarweisen Abstände aus."""
    difference = field[:, None, :] - field[None, :, :]
    return np.sqrt((difference ** 2).sum(axis=2))


def knn_distance(data, k=5):
    """Der Abstand zum k-nächsten Nachbarn.

    Das einfachste brauchbare Mass: wer weit von seinen Nachbarn
    entfernt liegt, ist auffällig. Es misst die Dichte global, also mit
    demselben Massstab überall im Raum, und genau daran scheitert es,
    sobald der Datensatz Gebiete verschiedener Dichte enthält.

    Raises:
        ValueError: bei einem k ausserhalb des Zulässigen.
    """
    field = _points(data)
    if not 1 <= k < field.shape[0]:
        raise ValueError("k liegt zwischen eins und der Anzahl der Punkte")
    measured = np.sort(_distances(field), axis=1)
    return measured[:, k]


def local_outlier_factor(data, k=20):
    """Der lokale Ausreisserfaktor.

    Verglichen wird nicht der Abstand selbst, sondern die eigene
    erreichbare Dichte mit der der Nachbarn. Ein Wert um eins heisst,
    dass der Punkt so dicht liegt wie seine Umgebung; ein Wert deutlich
    darüber heisst, dass die Umgebung dichter ist als er selbst.

    Damit misst das Verfahren örtlich und findet einen Punkt, der nur im
    Vergleich zu seiner eigenen Nachbarschaft auffällt, obwohl er global
    mitten im Datensatz liegt.

    Raises:
        ValueError: bei einem k ausserhalb des Zulässigen.
    """
    field = _points(data)
    if not 1 <= k < field.shape[0]:
        raise ValueError("k liegt zwischen eins und der Anzahl der Punkte")
    measured = _distances(field)
    order = np.argsort(measured, axis=1)
    neighbours = order[:, 1:k + 1]
    kth = measured[np.arange(len(field)), order[:, k]]
    reach = np.maximum(measured[np.arange(len(field))[:, None],
                                neighbours], kth[neighbours])
    density = 1.0 / np.maximum(reach.mean(axis=1), 1e-12)
    return density[neighbours].mean(axis=1) / density


def two_clouds_of_different_density(seed=0):
    """Zeigt den Fall, für den der lokale Faktor gebaut wurde.

    Zwei Häufungen, eine dicht und eine weit gestreut, und ein Punkt am
    Rand der dichten. Global gemessen ist sein Abstand zu den Nachbarn
    kleiner als der vieler ganz normaler Punkte der weiten Häufung, also
    fällt er dort nicht auf. Im Vergleich zu seiner eigenen Umgebung
    fällt er sofort auf.

    Returns:
        Abbildung mit beiden Urteilen.
    """
    rng = np.random.default_rng(seed)
    tight = rng.normal(size=(200, 2)) * 0.25
    loose = rng.normal(size=(200, 2)) * 3.0 + np.array([14.0, 0.0])
    planted = np.array([[1.6, 0.0]])
    cloud = np.vstack([tight, loose, planted])
    index = len(cloud) - 1
    plain = knn_distance(cloud, k=20)
    local = local_outlier_factor(cloud, k=20)
    plain_rank = int(np.sum(plain > plain[index]))
    local_rank = int(np.sum(local > local[index]))
    return {"plain distance rank": plain_rank,
            "local factor rank": local_rank,
            "plain distance finds it": plain_rank < 5,
            "lof finds it": local_rank < 5,
            "why": "der Punkt ist nur im Vergleich zu seiner eigenen "
                   "Umgebung auffällig"}


def what_both_assume():
    """Nennt die Annahme hinter jedem abstandsbasierten Verfahren.

    Dass Nähe im gewählten Abstand etwas mit Zugehörigkeit zu tun hat.
    In vielen Dimensionen trifft das immer weniger zu, weil alle
    Abstände zusammenrücken; auf Zeitreihen trifft es nur zu, wenn der
    Abstand die Zeitverschiebung verträgt; und auf gemischten Merkmalen
    trifft es nur zu, wenn die Skalen vorher angeglichen wurden.

    Das Verfahren selbst prüft diese Annahme nie und liefert immer eine
    Rangliste.
    """
    return {"the assumption": "Nähe im gewählten Abstand heisst "
                              "Zugehörigkeit",
            "where it fails": ["in vielen Dimensionen",
                               "auf Zeitreihen ohne passenden Abstand",
                               "bei ungleich skalierten Merkmalen"],
            "what the method does anyway": "es liefert immer eine "
                                           "Rangliste"}
