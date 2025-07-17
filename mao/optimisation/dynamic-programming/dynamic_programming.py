"""Dynamic programming: one decision at a time, backwards.

Bellman's principle says an optimal policy has the property that whatever the
first decision was, the rest is optimal for the state it leads to. That is
what makes the recursion valid, and it is a condition on the problem rather
than a property of the method: without it, solving the subproblem optimally
does not help.

Memoisation is the other half. The plain recursion for the Fibonacci numbers
makes 21891 calls for the twentieth number and the memoised one makes 39, and
the answers are identical, which is the whole argument in two numbers.
"""


def shortest_path(layers, start, end):
    """The cheapest path through a layered graph, computed backwards."""
    nodes = {start}
    for layer in layers:
        for source, edges in layer.items():
            nodes.add(source)
            nodes.update(edges)
    if end not in nodes:
        raise ValueError("the target %s is not in the graph" % end)
    costs = {end: 0}
    paths = {end: [end]}
    for layer in reversed(layers):
        for source, edges in layer.items():
            best, best_path = None, None
            for target, cost in edges.items():
                if target not in costs:
                    continue
                total = cost + costs[target]
                if best is None or total < best:
                    best, best_path = total, [source] + paths[target]
            if best is not None:
                costs[source] = best
                paths[source] = best_path
    if start not in costs:
        raise ValueError("no path from %s" % start)
    return {"cost": costs[start], "path": paths[start]}


def optimality_holds(layers, start, end):
    """Whether the tail of the optimal path is optimal for its own start.

    Bellman's principle, checked on the example rather than assumed. If it
    failed, the backward recursion would be computing the wrong thing.
    """
    whole = shortest_path(layers, start, end)
    if len(whole["path"]) < 3:
        return True
    second = whole["path"][1]
    tail = shortest_path(layers, second, end)
    return whole["cost"] == _edge_cost(layers, start, second) + tail["cost"]


def _edge_cost(layers, source, target):
    """The cost of one edge."""
    for layer in layers:
        if source in layer and target in layer[source]:
            return layer[source][target]
    raise ValueError("no edge from %s to %s" % (source, target))


def knapsack(values, weights, capacity):
    """The knapsack solved in stages, one item at a time."""
    table = [0] * (capacity + 1)
    for value, weight in zip(values, weights):
        for room in range(capacity, weight - 1, -1):
            table[room] = max(table[room], table[room - weight] + value)
    return table[capacity]


def fibonacci_calls(index):
    """The cost of the plain recursion against the memoised one."""
    plain = [0]
    memo = [0]

    def slow(number):
        """The recursion that recomputes everything."""
        plain[0] += 1
        return number if number < 2 else slow(number - 1) + slow(number - 2)

    cache = {}

    def fast(number):
        """The same recursion with the results remembered."""
        memo[0] += 1
        if number < 2:
            return number
        if number not in cache:
            cache[number] = fast(number - 1) + fast(number - 2)
        return cache[number]

    return {"plain value": slow(index), "plain calls": plain[0],
            "memoised value": fast(index), "memoised calls": memo[0]}
