"""Die Warteschlange M/M/c: mehrere Server an einer Schlange."""

import heapq
import math
import random


def erlang_c(arrival, service, servers):
    """Die Wahrscheinlichkeit, dass ein Ankömmling warten muss.

    Das ist die Formel von Erlang: der Anteil der Fälle, die keinen freien
    Server vorfinden. Bei einem Server geht sie in die Auslastung über,
    und aus ihr folgen alle weiteren Kennzahlen.

    Args:
        arrival: die Ankunftsrate λ.
        service: die Bedienrate μ eines einzelnen Servers.
        servers: die Zahl der Server c.

    Raises:
        ValueError: bei nicht positiven Raten, weniger als einem Server
            oder einer instabilen Schlange.
    """
    if arrival <= 0 or service <= 0:
        raise ValueError("die Raten müssen positiv sein")
    if servers < 1:
        raise ValueError("mindestens ein Server")
    offered = arrival / service
    rho = offered / servers
    if rho >= 1.0:
        raise ValueError("die Schlange ist nicht stabil")
    top = offered ** servers / math.factorial(servers) / (1.0 - rho)
    below = sum(offered ** index / math.factorial(index)
                for index in range(servers))
    return top / (below + top)


def measures(arrival, service, servers):
    """Rechnet die Kennzahlen einer M/M/c-Schlange aus.

    Returns:
        Abbildung mit Auslastung, Schlangenlänge, Wartezeit, Zykluszeit,
        Bestand und der Wartewahrscheinlichkeit.

    Raises:
        ValueError: bei unzulässigen Werten oder einer instabilen
            Schlange.
    """
    probability = erlang_c(arrival, service, servers)
    rho = arrival / (service * servers)
    waiting = probability / (servers * service - arrival)
    cycle = waiting + 1.0 / service
    return {"utilisation": rho, "probability of waiting": probability,
            "length of queue": arrival * waiting,
            "waiting time": waiting, "cycle time": cycle,
            "work in process": arrival * cycle, "servers": servers}


def call_centre(servers, per_server, arrival=50.0, target_minutes=1.0):
    """Das Call-Center als Pool von Mitarbeitern statt als ein Schalter.

    Acht Mitarbeiter, die je zehn Anrufe in der Stunde schaffen, sind
    nicht dasselbe wie ein Schalter mit achtzig Anrufen: der Pool hat
    mehrere Warteplätze weniger nötig, weil ein langer Anruf die anderen
    Server nicht blockiert.

    Returns:
        Abbildung mit den Kennzahlen und dem Urteil.
    """
    report = measures(arrival, per_server, servers)
    minutes = report["waiting time"] * 60.0
    report.update({"waiting minutes": minutes,
                   "within the target": minutes <= target_minutes,
                   "target minutes": target_minutes,
                   "per server": per_server, "arrival": arrival})
    return report


def pooling_effect(arrival=50.0, servers=8, per_server=10.0):
    """Vergleicht den Pool mit dem einen schnellen Server.

    Beide haben dieselbe Gesamtkapazität. Der eine schnelle Server ist
    trotzdem schlechter: wer ankommt, während er bedient, wartet auf genau
    diesen einen Vorgang, während im Pool sieben andere Vorgänge
    danebenlaufen und einer davon gleich fertig wird.

    Returns:
        Abbildung mit beiden Wartezeiten in Minuten und ihrem Verhältnis.
    """
    pooled = measures(arrival, per_server * servers, 1)["waiting time"] * 60
    spread = measures(arrival, per_server, servers)["waiting time"] * 60
    return {"single fast server": pooled, "many slow servers": spread,
            "ratio": pooled / spread if spread else float("inf"),
            "same total capacity": per_server * servers}


def simulate(arrival, service, servers, customers=100000, seed=0):
    """Spielt die Schlange mit mehreren Servern nach.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Kunden oder
            Servern.
    """
    if customers < 1:
        raise ValueError("mindestens ein Kunde")
    if servers < 1:
        raise ValueError("mindestens ein Server")
    generator = random.Random(seed)
    free = [0.0] * servers
    heapq.heapify(free)
    now = 0.0
    waiting = 0.0
    inside = 0.0
    for _ in range(customers):
        now += generator.expovariate(arrival)
        first = heapq.heappop(free)
        start = max(now, first)
        finish = start + generator.expovariate(service)
        heapq.heappush(free, finish)
        waiting += start - now
        inside += finish - now
    return {"waiting time": waiting / customers,
            "cycle time": inside / customers,
            "customers": customers}


def what_the_sheet_asks():
    """Ordnet die beiden Modelle der Aufgabe zu.

    Die Aufgabe steht unter der Überschrift M/M/1 und nennt zugleich acht
    Mitarbeiter. Beide Rechnungen sind möglich und führen zu
    verschiedenen Antworten: als ein Schalter mit achtzig Anrufen je
    Stunde wird die Vorgabe von einer Minute verfehlt, als Pool aus acht
    Mitarbeitern wird sie deutlich eingehalten. Welche Antwort gemeint
    ist, hängt daran, ob ein Anruf von einem oder von jedem Mitarbeiter
    bedient werden kann.
    """
    return {"as one counter": "M/M/1 with mu = 80 per hour",
            "as a pool": "M/M/c with c = 8 and mu = 10 per hour",
            "answers differ": True,
            "decides": "whether any clerk can take any call"}
