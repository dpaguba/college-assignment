"""Die Bewertung eines Detektors bei seltenen Ereignissen."""


def confusion(labels, flags):
    """Zählt die vier Felder der Wahrheitsmatrix.

    Raises:
        ValueError: bei verschiedenen Längen oder leeren Folgen.
    """
    if len(labels) != len(flags):
        raise ValueError("die Folgen sind verschieden lang")
    if not labels:
        raise ValueError("leere Folge")
    counted = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    for truth, flag in zip(labels, flags):
        if truth and flag:
            counted["tp"] += 1
        elif truth and not flag:
            counted["fn"] += 1
        elif flag:
            counted["fp"] += 1
        else:
            counted["tn"] += 1
    return counted


def measures(labels, flags):
    """Rechnet die üblichen Kennzahlen aus.

    Raises:
        ValueError: bei verschiedenen Längen oder leeren Folgen.
    """
    counted = confusion(labels, flags)
    positive = counted["tp"] + counted["fn"]
    flagged = counted["tp"] + counted["fp"]
    negative = counted["tn"] + counted["fp"]
    total = sum(counted.values())
    return {"precision": counted["tp"] / flagged if flagged else 0.0,
            "recall": counted["tp"] / positive if positive else 0.0,
            "false positive rate": (counted["fp"] / negative
                                    if negative else 0.0),
            "accuracy": (counted["tp"] + counted["tn"]) / total,
            "counts": counted}


def always_negative(labels):
    """Der Detektor, der nie Alarm schlägt.

    Er ist als Vergleich unentbehrlich: bei einer Grundrate von einem
    Promille erreicht er 99.9 Prozent Genauigkeit und findet nichts.
    Jede Genauigkeit, die nicht besser ist als seine, ist keine Leistung.

    Raises:
        ValueError: bei einer leeren Folge.
    """
    if not labels:
        raise ValueError("leere Folge")
    flags = [0] * len(labels)
    report = measures(labels, flags)
    return {"accuracy": report["accuracy"], "recall": report["recall"],
            "finds nothing": True,
            "why it matters": "die Genauigkeit eines Detektors muss gegen "
                              "diese Zahl gehalten werden"}


def base_rate_effect(rate, recall, false_positive_rate, population=100000):
    """Rechnet aus, wie viele Alarme echt sind.

    Die Genauigkeit im Sinne der Treffer unter den Alarmen hängt nicht
    nur am Detektor, sondern an der Grundrate, und bei seltenen
    Ereignissen entscheidet sie allein. Ein Detektor mit neunundneunzig
    Prozent Trefferquote und einem Prozent Fehlalarm liefert bei einer
    Grundrate von einem Promille auf einen echten Fund zehn falsche.

    Raises:
        ValueError: bei Anteilen ausserhalb von null bis eins oder einer
            nicht positiven Grundgesamtheit.
    """
    for value in (rate, recall, false_positive_rate):
        if not 0.0 <= value <= 1.0:
            raise ValueError("Anteil ausserhalb von 0 bis 1")
    if population < 1:
        raise ValueError("die Grundgesamtheit muss positiv sein")
    positives = rate * population
    true_alarms = positives * recall
    false_alarms = (population - positives) * false_positive_rate
    alarms = true_alarms + false_alarms
    return {"true alarms": true_alarms, "false alarms": false_alarms,
            "precision": true_alarms / alarms if alarms else 0.0,
            "false per true": (false_alarms / true_alarms
                               if true_alarms else float("inf")),
            "rate": rate}


def what_it_takes(rate, recall=0.99, wanted=0.5, population=100000):
    """Sucht die Fehlalarmrate, die eine gewünschte Genauigkeit erreicht.

    Umgestellt: damit die Hälfte der Alarme echt ist, darf die
    Fehlalarmrate höchstens die Grundrate mal der Trefferquote geteilt
    durch den Rest sein. Bei einer Grundrate von einem Promille sind das
    0.099 Prozent, also gut zehnmal weniger als das eine Prozent, das in
    Berichten als guter Wert gilt.

    Raises:
        ValueError: bei unzulässigen Anteilen.
    """
    for value in (rate, recall, wanted):
        if not 0.0 < value < 1.0:
            raise ValueError("Anteil ausserhalb von 0 bis 1")
    needed = (rate * recall * (1 - wanted)) / (wanted * (1 - rate))
    return {"rate": rate, "wanted precision": wanted,
            "false positive rate needed": needed,
            "as a percentage": needed * 100,
            "against the usual one percent": 0.01 / needed
            if needed else float("inf")}


def why_accuracy_is_the_wrong_number():
    """Nennt die Kennzahlen, die bei seltenen Ereignissen taugen.

    Die Genauigkeit im Sinne der richtig eingeordneten Fälle wird von
    der Mehrheit bestimmt und sagt nichts. Brauchbar sind die Trefferquote,
    die Genauigkeit unter den Alarmen und ihr Verhältnis; und die
    Kurve, die beide gegeneinander aufträgt, ist aussagekräftiger als
    die Kurve über die Fehlalarmrate, weil diese bei einer schiefen
    Verteilung optimistisch aussieht.
    """
    return {"do not use": "die Genauigkeit über alle Fälle",
            "use": ["Trefferquote", "Genauigkeit unter den Alarmen",
                    "die Zahl falscher Alarme je echtem"],
            "curve": "Precision gegen Recall, nicht gegen die "
                     "Fehlalarmrate",
            "why": "die Fehlalarmrate wird durch die grosse Mehrheit der "
                   "Negativen geteilt und sieht deshalb klein aus"}
