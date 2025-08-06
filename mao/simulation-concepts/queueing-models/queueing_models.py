"""The single server queue, analytically and by simulation.

The M/M/1 queue has closed forms, which makes it the standard check on a
simulator: run it long enough and the measured response time has to approach
the formula. When it does not, the simulator is wrong, and finding that out
on a model with a known answer is far cheaper than finding it out later.

The formulas also show why utilisation is the quantity to watch. The expected
number in the system is rho over one minus rho, so it grows without bound as
the load approaches one: at 50 percent load the queue holds one customer and
at 95 percent it holds nineteen.
"""

import math
import random


def mm1(arrival_rate, service_rate):
    """The steady state results, or nothing when the queue is unstable."""
    if arrival_rate >= service_rate:
        return None
    load = arrival_rate / service_rate
    in_system = load / (1 - load)
    response = 1 / (service_rate - arrival_rate)
    return {"utilisation": load, "in system": in_system,
            "in queue": load ** 2 / (1 - load), "response time": response,
            "waiting time": response - 1 / service_rate}


def simulate_mm1(arrival_rate, service_rate, customers, seed=0):
    """A single server queue simulated customer by customer."""
    generator = random.Random(seed)
    arrival = 0.0
    finished = 0.0
    total_response = 0.0
    for _ in range(customers):
        arrival += generator.expovariate(arrival_rate)
        start = max(arrival, finished)
        finished = start + generator.expovariate(service_rate)
        total_response += finished - arrival
    return {"response time": total_response / customers}


def queue_trace(arrival_rate, service_rate, customers, seed=0):
    """The number in the system seen by each arriving customer.

    A correlated series, which is what makes the output analysis of a
    simulation different from the analysis of independent samples, and what
    the batch means module exists to handle.
    """
    generator = random.Random(seed)
    arrival = 0.0
    departures = []
    trace = []
    for _ in range(customers):
        arrival += generator.expovariate(arrival_rate)
        departures = [time for time in departures if time > arrival]
        trace.append(len(departures))
        start = max(arrival, departures[-1] if departures else arrival)
        departures.append(start + generator.expovariate(service_rate))
    return trace


def littles_law(arrival_rate, response_time):
    """The number in the system, from the rate and the time spent."""
    return arrival_rate * response_time
