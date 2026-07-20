"""Politiken bewerten, ohne sie zu spielen."""

import numpy as np


def estimate(actions, rewards, behaviour, target):
    """Schätzt den Wert einer Politik aus fremden Aufzeichnungen.

    Jede aufgezeichnete Handlung wird mit dem Verhältnis der beiden
    Wahrscheinlichkeiten gewichtet: wie oft die gesuchte Politik sie
    gewählt hätte, geteilt durch wie oft die aufzeichnende sie gewählt
    hat. Der Schätzer ist damit erwartungstreu, sofern die aufzeichnende
    Politik jede Handlung der gesuchten mit positiver
    Wahrscheinlichkeit spielt.

    Raises:
        ValueError: bei unpassend vielen Angaben oder einer Handlung,
            die die aufzeichnende Politik nie spielt.
    """
    chosen = np.asarray(actions, dtype=int)
    got = np.asarray(rewards, dtype=float)
    behaved = np.asarray(behaviour, dtype=float)
    wanted = np.asarray(target, dtype=float)
    if not (len(chosen) == len(got) == len(behaved) == len(wanted)):
        raise ValueError("zu jeder Handlung gehört genau ein Eintrag")
    rows = np.arange(len(chosen))
    under = behaved[rows, chosen]
    over = wanted[rows, chosen]
    if np.any((over > 0.0) & (under <= 0.0)):
        raise ValueError("die aufzeichnende Politik spielt eine gesuchte "
                         "Handlung nie")
    return float(np.mean(got * over / np.where(under > 0.0, under, 1.0)))


def _log(size, rng, spread=0.0, arms=3, means=None):
    """Zeichnet Handlungen einer Politik und ihre Belohnungen auf."""
    means = (np.array([0.2, 0.5, 0.8])[:arms] if means is None
             else np.asarray(means, dtype=float))
    weights = np.full(arms, 1.0 / arms)
    if spread != 0.0:
        weights = np.exp(np.arange(arms) * spread)
        weights = weights / weights.sum()
    behaviour = np.tile(weights, (size, 1))
    chosen = rng.choice(arms, size=size, p=weights)
    rewards = (rng.uniform(size=size) < means[chosen]).astype(float)
    return chosen, rewards, behaviour, means


def unbiased(runs=200, size=500, seed=0):
    """Prüft, dass der Schätzer im Mittel richtig liegt.

    Gesucht wird der Wert einer Politik, die immer den dritten Arm
    zieht. Ihr wahrer Wert ist bekannt, weil die Belohnungen erzeugt
    wurden. Über viele Aufzeichnungen gemittelt trifft der Schätzer ihn.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Läufen.
    """
    if runs <= 0 or size <= 0:
        raise ValueError("Läufe und Grösse müssen positiv sein")
    found = []
    for index in range(runs):
        rng = np.random.default_rng(seed + index)
        chosen, rewards, behaviour, means = _log(size, rng)
        target = np.tile(np.array([0.0, 0.0, 1.0]), (size, 1))
        found.append(estimate(chosen, rewards, behaviour, target))
    return {"mean estimate": float(np.mean(found)),
            "truth": float(means[2]),
            "spread": float(np.std(found)), "runs": runs}


def the_variance_explodes(spreads=(0.0, 1.0, 2.0, 3.0), runs=200,
                          size=500, seed=0):
    """Zeigt, was passiert, wenn die Politiken auseinanderlaufen.

    Der Schätzer bleibt erwartungstreu, gleich wie verschieden die
    beiden Politiken sind. Seine Streuung wächst dagegen mit dem
    Verhältnis der Wahrscheinlichkeiten, und zwar ohne Grenze: spielt
    die aufzeichnende Politik eine Handlung fast nie, so hängt die
    ganze Schätzung an den wenigen Fällen, in denen sie es doch tat.

    Damit ist ein einzelner Schätzwert unbrauchbar, obwohl das
    Verfahren korrekt ist, und genau diese Verwechslung von
    Erwartungstreue und Verlässlichkeit steckt hinter vielen zu guten
    Ergebnissen.

    Returns:
        Liste mit einer Zeile je Abstand der Politiken.
    """
    found = []
    for spread in spreads:
        values = []
        for index in range(runs):
            rng = np.random.default_rng(seed + index)
            chosen, rewards, behaviour, means = _log(size, rng,
                                                     spread=-spread)
            target = np.tile(np.array([0.0, 0.0, 1.0]), (size, 1))
            values.append(estimate(chosen, rewards, behaviour, target))
        found.append({"spread of the policies": spread,
                      "mean estimate": float(np.mean(values)),
                      "spread": float(np.std(values)),
                      "truth": float(means[2])})
    return found


def choosing_on_the_same_data(candidates=40, size=500, runs=60, seed=0):
    """Zeigt, was die Auswahl auf denselben Aufzeichnungen kostet.

    Alle geprüften Politiken sind hier gleich gut: jeder Arm zahlt mit
    derselben Wahrscheinlichkeit, also ist der wahre Wert jeder Politik
    ein halbes. Was die Schätzungen unterscheidet, ist ausschliesslich
    der Zufall der Aufzeichnung.

    Genommen wird die Politik mit dem höchsten geschätzten Wert. Damit
    gewinnt fast immer eine, deren Schätzung nach oben ausschlug, und
    der berichtete Wert ist zu hoch, umso mehr, je mehr Politiken
    geprüft wurden.

    Eine zweite, unabhängige Aufzeichnung gibt die richtige Zahl. Das
    ist derselbe Befund wie beim Abstimmen von Hyperparametern, und im
    Offline-Reinforcement-Learning wiegt er schwerer, weil dort ohnehin
    keine neuen Versuche gemacht werden können.

    Gemittelt wird über viele Aufzeichnungen, denn ein einzelner Lauf
    sagt zu einer Verzerrung nichts: dort ist der Ausschlag selbst
    zufällig.

    Returns:
        Abbildung mit der geschätzten und der wahren Güte des Gewinners.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Politiken.
    """
    if candidates <= 0:
        raise ValueError("es braucht mindestens eine Politik")
    picked = []
    truths = []
    seconds = []
    for run in range(runs):
        rng = np.random.default_rng(seed * 1000 + run)
        equal = np.full(3, 0.5)
        chosen, rewards, behaviour, means = _log(size, rng, means=equal)
        fresh = _log(size, np.random.default_rng(seed * 1000 + run
                                                 + 500000), means=equal)
        policies = rng.dirichlet(np.ones(3), size=candidates)
        scores = [estimate(chosen, rewards, behaviour,
                           np.tile(policy, (size, 1)))
                  for policy in policies]
        winner = int(np.argmax(scores))
        picked.append(scores[winner])
        truths.append(float(policies[winner] @ means))
        seconds.append(estimate(fresh[0], fresh[1], fresh[2],
                                np.tile(policies[winner], (size, 1))))
    return {"candidates": candidates, "runs": runs,
            "estimate of the winner": float(np.mean(picked)),
            "true value of the winner": float(np.mean(truths)),
            "estimate on a fresh log": float(np.mean(seconds)),
            "inflation": float(np.mean(picked) - np.mean(truths)),
            "why": "der Gewinner ist meist der mit dem grössten "
                   "Ausschlag nach oben"}


def what_would_fix_it():
    """Nennt, was gegen den Befund hilft.

    Die Zahl der geprüften Politiken berichten, denn ohne sie ist die
    Zahl nicht einzuordnen. Auf einer zweiten Aufzeichnung messen, die
    bei der Auswahl keine Rolle gespielt hat. Und das Verhältnis der
    Wahrscheinlichkeiten mitberichten, denn eine Schätzung, die an
    wenigen Aufzeichnungen hängt, ist auch dann unbrauchbar, wenn sie
    unverzerrt ist.
    """
    return {"report": ["die Zahl der geprüften Politiken",
                       "das Verhältnis der Wahrscheinlichkeiten"],
            "measure on": "eine zweite, nicht benutzte Aufzeichnung",
            "why the ratio matters": "eine Schätzung an wenigen Fällen "
                                     "ist unbrauchbar, auch wenn sie "
                                     "unverzerrt ist"}
