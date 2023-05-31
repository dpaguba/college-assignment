"""What a job costs, and why more reducers stop helping.

The map phase reads the input, the shuffle moves the map output over the
network, and the reduce phase writes the result. More reducers shorten the
reduce phase and add a fixed overhead each, so the total has a minimum and
adding reducers past it makes the job slower.

A combiner lowers the shuffle, which is usually the dominant term, and it is
the cheapest change available: it needs no extra machines and no change to
the algorithm beyond a combinable measure.
"""


def estimate(input_size, map_output, reducers, combiner_share=1.0,
             overhead_per_reducer=5.0):
    """The rough cost of a job, in arbitrary units."""
    shuffled = map_output * combiner_share
    map_time = input_size
    reduce_time = shuffled / max(1, reducers)
    overhead = reducers * overhead_per_reducer
    return {"map time": map_time, "network": shuffled,
            "reduce time": reduce_time, "overhead": overhead,
            "disk": input_size + shuffled,
            "total": map_time + shuffled + reduce_time + overhead}


def best_reducers(input_size, map_output, combiner_share=1.0, limit=200):
    """The number of reducers minimising the total."""
    best, best_cost = 1, None
    for reducers in range(1, limit + 1):
        value = estimate(input_size, map_output, reducers,
                         combiner_share)["total"]
        if best_cost is None or value < best_cost:
            best, best_cost = reducers, value
    return {"reducers": best, "total": best_cost}
