"""Die Warteschlange M/M/1: ein Server, exponentielle Zeiten."""

import random


def measures(arrival, service):
    """Rechnet die fünf Kennzahlen einer M/M/1-Schlange aus.

    Args:
        arrival: die mittlere Ankunftsrate λ.
        service: die mittlere Bedienrate μ.

    Returns:
        Abbildung mit Auslastung, Schlangenlänge, Wartezeit, Zykluszeit
        und Bestand.

    Raises:
        ValueError: bei nicht positiven Raten oder wenn die Ankunftsrate
            die Bedienrate erreicht.
    """
    if arrival <= 0 or service <= 0:
        raise ValueError("die Raten müssen positiv sein")
    if arrival >= service:
        raise ValueError("die Schlange ist nicht stabil")
    rho = arrival / service
    length = rho * rho / (1.0 - rho)
    waiting = length / arrival
    cycle = waiting + 1.0 / service
    return {"utilisation": rho, "length of queue": length,
            "waiting time": waiting, "cycle time": cycle,
            "work in process": arrival * cycle}


def call_centre(capacity, arrival=50.0, target_minutes=1.0):
    """Die Aufgabe aus Zettel 4: reicht die Kapazität für eine Minute?

    Zur Stosszeit von elf bis vierzehn Uhr kommen 150 der 260 Anrufe, also
    fünfzig in der Stunde. Das Call-Center wird hier als ein Server mit
    der gemeinsamen Bedienrate gerechnet, so wie es die Aufgabe unter der
    Überschrift M/M/1 vorgibt.

    Args:
        capacity: die Zahl der Anrufe, die das Center je Stunde schafft.
        arrival: die Anrufe je Stunde zur Stosszeit.
        target_minutes: die Vorgabe für die mittlere Wartezeit.

    Returns:
        Abbildung mit den Kennzahlen und dem Urteil.
    """
    report = measures(arrival, capacity)
    minutes = report["waiting time"] * 60.0
    report.update({"capacity": capacity, "arrival": arrival,
                   "waiting minutes": minutes,
                   "within the target": minutes <= target_minutes,
                   "target minutes": target_minutes})
    return report


def peak_arrival_rate():
    """Die Ankunftsraten der drei Zeitfenster des Call-Centers.

    Von acht bis siebzehn Uhr kommen 260 Anrufe, davon 150 zwischen elf
    und vierzehn und fünfzig zwischen vierzehn und siebzehn; für das erste
    Fenster bleiben sechzig.

    Returns:
        Abbildung vom Fenster auf die Anrufe je Stunde.
    """
    windows = {"08-11": 260 - 150 - 50, "11-14": 150, "14-17": 50}
    return {name: calls / 3.0 for name, calls in windows.items()}


def simulate(arrival, service, customers=100000, seed=0):
    """Spielt die Schlange nach und misst die Wartezeit.

    Die Abstände zwischen den Ankünften und die Bedienzeiten sind
    exponentiell verteilt, ein Server bedient in der Reihenfolge der
    Ankunft. Das ist die Definition von M/M/1 und damit eine von den
    Formeln unabhängige Gegenrechnung.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Kunden.
    """
    if customers < 1:
        raise ValueError("mindestens ein Kunde")
    generator = random.Random(seed)
    now = 0.0
    free_at = 0.0
    waiting = 0.0
    inside = 0.0
    for _ in range(customers):
        now += generator.expovariate(arrival)
        start = max(now, free_at)
        free_at = start + generator.expovariate(service)
        waiting += start - now
        inside += free_at - now
    return {"waiting time": waiting / customers,
            "cycle time": inside / customers,
            "customers": customers}


def why_the_queue_explodes():
    """Sagt, warum die Wartezeit vor der Kapazitätsgrenze davonläuft.

    Die Schlangenlänge ist ρ²/(1 − ρ). Bei einer Auslastung von der Hälfte
    steht im Mittel ein halber Fall an, bei neunzig Prozent sind es acht,
    bei neunundneunzig Prozent achtundneunzig. Der Nenner treibt das, und
    das ist der Grund, warum eine fast ausgelastete Stelle sich anfühlt,
    als sei sie überlastet.
    """
    return {rho: rho * rho / (1.0 - rho)
            for rho in (0.5, 0.8, 0.9, 0.95, 0.99)}
