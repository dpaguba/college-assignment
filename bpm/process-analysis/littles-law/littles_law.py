"""Das Little'sche Gesetz und was daraus für die Kapazität folgt."""

import random


def work_in_process(arrival, cycle):
    """Die Zahl der Fälle in Bearbeitung: WIP = λ · CT.

    Raises:
        ValueError: bei einem negativen Wert.
    """
    if arrival < 0 or cycle < 0:
        raise ValueError("negativer Wert")
    return arrival * cycle


def cycle_time(arrival, work_in_process):
    """Die Durchlaufzeit aus Ankunftsrate und Bestand.

    Raises:
        ValueError: bei einer nicht positiven Ankunftsrate.
    """
    if arrival <= 0:
        raise ValueError("die Ankunftsrate muss positiv sein")
    return work_in_process / arrival


def arrival_rate(work_in_process, cycle):
    """Die Ankunftsrate aus Bestand und Durchlaufzeit.

    Raises:
        ValueError: bei einer nicht positiven Durchlaufzeit.
    """
    if cycle <= 0:
        raise ValueError("die Durchlaufzeit muss positiv sein")
    return work_in_process / cycle


def restaurant(seats=110):
    """Das Restaurant aus Übungsaufgabe 3.

    Geöffnet von 10 bis 22 Uhr, 1200 Gäste am Tag. In den sechs Stunden
    der Stosszeit kommen 900 Gäste, im Mittel sitzen 90 gleichzeitig; in
    den übrigen sechs Stunden 300 Gäste bei 30 Sitzenden. Beide Male
    ergibt das Gesetz dieselbe Verweildauer: die Stosszeit unterscheidet
    sich in der Zahl der Gäste, nicht darin, wie lange einer bleibt.

    Args:
        seats: die Kapazität des Raumes.

    Returns:
        Abbildung mit beiden Zeitfenstern und der Schranke aus den Plätzen.
    """
    peak_hours = 6
    quiet_hours = 6
    peak = {"guests": 900, "hours": peak_hours, "work in process": 90}
    quiet = {"guests": 300, "hours": quiet_hours, "work in process": 30}
    for window in (peak, quiet):
        window["arrival rate"] = window["guests"] / window["hours"]
        window["cycle time"] = cycle_time(window["arrival rate"],
                                          window["work in process"])
    return {"peak": peak, "off peak": quiet, "seats": seats,
            "most arrivals the seats allow":
                arrival_rate(seats, peak["cycle time"]),
            "answer": "shorten the stay, because the seats are fixed"}


def check_by_simulation(arrival, cycle, runs=20000, seed=0):
    """Prüft das Gesetz an einem nachgespielten Zustrom.

    Die Fälle kommen mit exponentiellen Abständen und bleiben genau die
    angegebene Zeit. Gemessen wird der mittlere Bestand über die Zeit;
    er muss das Produkt aus Rate und Verweildauer treffen.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Fällen.
    """
    if runs < 1:
        raise ValueError("mindestens ein Fall")
    generator = random.Random(seed)
    now = 0.0
    events = []
    for _ in range(runs):
        now += generator.expovariate(arrival)
        events.append((now, 1))
        events.append((now + cycle, -1))
    events.sort()
    inside = 0
    previous = 0.0
    area = 0.0
    for moment, change in events:
        area += inside * (moment - previous)
        previous = moment
        inside += change
    return {"measured": area / previous if previous else 0.0,
            "predicted": work_in_process(arrival, cycle),
            "cases": runs}


def what_it_says():
    """Nennt die beiden Aussagen des Gesetzes.

    Steigt die Bearbeitungszeit oder die Zahl neuer Fälle, so steigt der
    Bestand. Und umgekehrt: wer bei steigendem Zustrom den Bestand halten
    will, muss die Durchlaufzeit verkürzen; eine dritte Möglichkeit gibt
    es nicht.
    """
    return {"first": "longer cycle time or more arrivals means more cases "
                     "in progress",
            "second": "to hold the number of cases while arrivals grow, "
                      "the cycle time has to fall",
            "holds for": "any stable system, whatever the distributions"}
