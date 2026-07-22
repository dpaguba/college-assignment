"""Die Zerlegung der Unsicherheit in ihre zwei Arten."""

import numpy as np


def entropy(distribution):
    """Die Entropie einer Verteilung, in Bit.

    Raises:
        ValueError: bei einer Verteilung, die nicht auf eins summiert.
    """
    values = np.asarray(distribution, dtype=float)
    if abs(float(values.sum()) - 1.0) > 1e-9 or np.any(values < -1e-12):
        raise ValueError("keine Wahrscheinlichkeitsverteilung")
    safe = np.clip(values, 1e-300, 1.0)
    return float(-np.sum(values * np.log2(safe)))


def decompose(members):
    """Zerlegt die Unsicherheit eines Ensembles in zwei Teile.

    Die Entropie der gemittelten Vorhersage ist die gesamte
    Unsicherheit. Der Durchschnitt der einzelnen Entropien ist der Teil,
    den auch ein perfekt informiertes Modell nicht loswürde, also das
    Rauschen der Aufgabe. Die Differenz ist die wechselseitige
    Information zwischen Vorhersage und Modellwahl, also die
    Uneinigkeit der Mitglieder.

    Die Gleichung gesamt gleich Rauschen plus Uneinigkeit ist eine
    Identität. Sie ist zugleich der Grund, warum ein einzelnes Modell
    die beiden Arten nicht trennen kann: ohne Mitglieder gibt es keine
    Uneinigkeit, und der zweite Teil ist null.

    Args:
        members: die Vorhersagen der Ensemblemitglieder.

    Returns:
        Abbildung mit den drei Grössen.

    Raises:
        ValueError: bei einem leeren Ensemble oder Verteilungen, die
            nicht auf eins summieren.
    """
    field = np.asarray(members, dtype=float)
    if field.ndim != 2 or field.shape[0] == 0:
        raise ValueError("leeres oder falsch geformtes Ensemble")
    for row in field:
        if abs(float(row.sum()) - 1.0) > 1e-9:
            raise ValueError("keine Wahrscheinlichkeitsverteilung")
    mean = field.mean(axis=0)
    total = entropy(mean)
    aleatoric = float(np.mean([entropy(row) for row in field]))
    return {"total": total, "aleatoric": aleatoric,
            "epistemic": total - aleatoric, "members": len(field)}


def _ensemble(size, seed, members=12):
    """Zieht ein Ensemble aus einer Stichprobe der gegebenen Grösse.

    Jedes Mitglied sieht eine eigene gezogene Stichprobe und schätzt
    daraus die Wahrscheinlichkeit einer Münze. Mit wachsender Stichprobe
    rücken die Schätzungen zusammen.
    """
    rng = np.random.default_rng(seed)
    truth = 0.7
    found = []
    for _ in range(members):
        flips = rng.uniform(size=size) < truth
        estimate = float((flips.sum() + 1.0) / (size + 2.0))
        found.append([estimate, 1.0 - estimate])
    return np.array(found)


def more_data_removes_one_kind(sizes=(5, 20, 100, 1000), seed=0):
    """Zeigt, welcher Teil mit mehr Daten verschwindet.

    Die Uneinigkeit der Mitglieder fällt, denn mit genügend Daten
    schätzen alle dasselbe. Das Rauschen der Münze bleibt, denn kein
    Datensatz macht aus einer Münze mit siebzig Prozent eine sichere
    Sache.

    Returns:
        Liste mit einer Zeile je Stichprobengrösse.
    """
    found = []
    for size in sizes:
        report = decompose(_ensemble(size, seed))
        report["size"] = size
        found.append(report)
    return found


def which_one_can_be_fixed():
    """Sagt, was mit welchem Teil zu machen ist.

    Der eine Teil ist eine Aussage über das Modell und schrumpft mit
    Daten, mit einem besseren Modell oder mit einer besseren
    Darstellung. Der andere ist eine Aussage über die Aufgabe und bleibt.

    Die Unterscheidung ist praktisch: hohe Uneinigkeit heisst, dass es
    sich lohnt, mehr Daten in dieser Gegend zu sammeln, und genau das
    ist die Grundlage des aktiven Lernens. Hohes Rauschen heisst, dass
    zusätzliche Daten in dieser Gegend nichts bringen.
    """
    return {"epistemic": "eine Aussage über das Modell",
            "aleatoric": "eine Aussage über die Aufgabe",
            "what more data fixes": "nur den ersten Teil",
            "what to do with the second": "die Vorhersage ablehnen oder "
                                          "die Merkmale ändern",
            "why it matters": "hohe Uneinigkeit sagt, wo sich Sammeln "
                              "lohnt"}
