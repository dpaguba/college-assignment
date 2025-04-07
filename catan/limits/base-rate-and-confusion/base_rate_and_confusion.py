"""Die Grundrate und die Verwechslungsmatrix."""


def confusion(truth, predicted):
    """Zählt die vier Fälle und rechnet die üblichen Masse aus.

    Raises:
        ValueError: bei verschiedenen Längen oder einer leeren Liste.
    """
    if len(truth) != len(predicted) or not truth:
        raise ValueError("zu jedem Fall gehört genau eine Vorhersage")
    counted = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    for real, guess in zip(truth, predicted):
        if real and guess:
            counted["tp"] += 1
        elif real and not guess:
            counted["fn"] += 1
        elif not real and guess:
            counted["fp"] += 1
        else:
            counted["tn"] += 1
    positives = counted["tp"] + counted["fn"]
    negatives = counted["tn"] + counted["fp"]
    recall = counted["tp"] / positives if positives else 0.0
    specificity = counted["tn"] / negatives if negatives else 0.0
    chosen = counted["tp"] + counted["fp"]
    counted.update({
        "accuracy": (counted["tp"] + counted["tn"]) / len(truth),
        "recall": recall, "specificity": specificity,
        "precision": counted["tp"] / chosen if chosen else 0.0,
        "balanced accuracy": (recall + specificity) / 2.0,
    })
    return counted


def always_the_majority(share=0.99, size=10000):
    """Rät immer die häufige Klasse und misst, wie gut das aussieht.

    Bei einem Anteil von neunundneunzig Prozent erreicht diese Regel
    neunundneunzig Prozent Trefferquote, ohne irgendetwas zu erkennen.
    Die ausgewogene Trefferquote sieht das sofort: sie liegt bei
    fünfzig Prozent, weil die seltene Klasse nie erkannt wird.

    Raises:
        ValueError: bei einem Anteil ausserhalb von null bis eins.
    """
    if not 0.0 < share < 1.0:
        raise ValueError("der Anteil liegt zwischen null und eins")
    common = int(size * share)
    truth = [0] * common + [1] * (size - common)
    predicted = [0] * size
    report = confusion(truth, predicted)
    return {"accuracy": report["accuracy"],
            "balanced accuracy": report["balanced accuracy"],
            "recall of the rare class": report["recall"],
            "share of the common class": share,
            "what it learned": "nichts"}


def positive_predictive_value(prevalence=0.01, sensitivity=0.99,
                              specificity=0.99):
    """Rechnet aus, was ein positiver Befund wirklich wert ist.

    Bei einer Häufigkeit von einem Prozent und einem Test, der in
    neunundneunzig Prozent der Fälle richtig liegt, ist ein positiver
    Befund nur zur Hälfte richtig. Der Grund ist die Grundrate: unter
    zehntausend Menschen sind hundert krank, davon werden neunundneunzig
    gefunden, und unter den neuntausendneunhundert Gesunden gibt es
    neunundneunzig Fehlalarme.

    Dieselbe Rechnung gilt für jeden seltenen Fall, also auch für einen
    Zug, der nur selten spielentscheidend ist.

    Raises:
        ValueError: bei einer Wahrscheinlichkeit ausserhalb von null bis
            eins.
    """
    for value in (prevalence, sensitivity, specificity):
        if not 0.0 <= value <= 1.0:
            raise ValueError("Wahrscheinlichkeiten liegen zwischen null "
                             "und eins")
    found = prevalence * sensitivity
    alarms = (1.0 - prevalence) * (1.0 - specificity)
    return {"prevalence": prevalence,
            "positive predictive value": found / (found + alarms)
            if found + alarms > 0 else 0.0,
            "true positives per 10000": round(found * 10000, 1),
            "false alarms per 10000": round(alarms * 10000, 1),
            "why": "die Grundrate schlägt die Güte des Tests"}


def what_this_means_for_a_game_ai():
    """Überträgt die Grundrate auf die Bewertung von Zügen.

    Die meisten Züge einer Partie sind gleichgültig. Ein Modell, das
    lernt, gute von schlechten Zügen zu trennen, arbeitet also mit einer
    sehr schiefen Verteilung, und eine Trefferquote von fünfundneunzig
    Prozent bedeutet dort gar nichts: sie ist mit «alles ist
    gleichgültig» zu erreichen.

    Gemessen werden muss deshalb auf der seltenen Klasse, und bewertet
    wird nicht die Zahl der richtigen Antworten, sondern was die
    falschen kosten.
    """
    return {"the trap": "die meisten Züge sind gleichgültig, also ist "
                        "eine hohe Trefferquote wertlos",
            "what to measure": "die seltene Klasse",
            "what to weigh": "was die Fehler kosten",
            "the yardstick": "die Grundrate, nicht die Null"}
