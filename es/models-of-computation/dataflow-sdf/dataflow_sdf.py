"""Synchronous dataflow: fixed rates, and everything decidable in advance.

Each actor consumes and produces a fixed number of tokens per firing, so the
balance equations can be solved before anything runs. Their solution is the
repetition vector, the number of firings that returns every channel to its
starting state, and it exists exactly when the rates are consistent.

That is the trade the model makes. Data dependent rates are forbidden, and in
exchange the schedule, the buffer sizes and the absence of deadlock are all
decided at compile time, which is why the model is used for signal processing
and not for general computation.
"""

from fractions import Fraction


class Graph:
    """An SDF graph: actors and channels with production and consumption rates."""

    def __init__(self, actors, channels):
        """Channels are (source, target, produced, consumed, initial tokens)."""
        self.actors = list(actors)
        self.channels = [channel if len(channel) == 5 else channel + (0,)
                         for channel in channels]


def repetition_vector(graph):
    """The smallest firing counts that leave every channel unchanged.

    Solved by propagating the rate ratios through the graph and scaling the
    result to integers. When two paths disagree, the equations have no
    solution and the graph is inconsistent, which is reported as nothing.
    """
    rates = {graph.actors[0]: Fraction(1)}
    changed = True
    while changed:
        changed = False
        for source, target, produced, consumed, _tokens in graph.channels:
            if source in rates and target not in rates:
                rates[target] = rates[source] * Fraction(produced, consumed)
                changed = True
            elif target in rates and source not in rates:
                rates[source] = rates[target] * Fraction(consumed, produced)
                changed = True
    if len(rates) != len(graph.actors):
        return None
    for source, target, produced, consumed, _tokens in graph.channels:
        if rates[source] * produced != rates[target] * consumed:
            return None
    denominator = 1
    for value in rates.values():
        denominator = denominator * value.denominator // _gcd(
            denominator, value.denominator)
    scaled = {name: int(value * denominator) for name, value in rates.items()}
    divisor = 0
    for value in scaled.values():
        divisor = _gcd(divisor, value)
    return {name: value // divisor for name, value in scaled.items()}


def _gcd(first, second):
    """The greatest common divisor."""
    while second:
        first, second = second, first % second
    return first


def initial_tokens(graph):
    """The tokens on each channel before anything fires."""
    return {(source, target): tokens
            for source, target, _p, _c, tokens in graph.channels}


def schedule(graph):
    """A firing order realising the repetition vector, or nothing.

    Greedy: fire whatever is enabled and still owes firings. If the greedy
    order gets stuck while firings remain, the graph deadlocks, which for SDF
    means it deadlocks under every order.
    """
    vector = repetition_vector(graph)
    if vector is None:
        return None
    remaining = dict(vector)
    tokens = initial_tokens(graph)
    order = []
    while any(remaining.values()):
        progress = False
        for actor in graph.actors:
            if not remaining[actor]:
                continue
            if not _enabled(graph, actor, tokens):
                continue
            _fire(graph, actor, tokens)
            remaining[actor] -= 1
            order.append(actor)
            progress = True
        if not progress:
            return None
    return order


def _enabled(graph, actor, tokens):
    """Whether every input channel has enough tokens."""
    for source, target, _produced, consumed, _initial in graph.channels:
        if target == actor and tokens[(source, target)] < consumed:
            return False
    return True


def _fire(graph, actor, tokens):
    """Consumes and produces the tokens of one firing."""
    for source, target, produced, consumed, _initial in graph.channels:
        if target == actor:
            tokens[(source, target)] -= consumed
        if source == actor:
            tokens[(source, target)] += produced


def tokens_after(graph, order):
    """The token counts after the given firing order."""
    tokens = initial_tokens(graph)
    for actor in order:
        _fire(graph, actor, tokens)
    return tokens


def buffer_sizes(graph):
    """The largest number of tokens each channel holds during a schedule."""
    order = schedule(graph)
    if order is None:
        return None
    tokens = initial_tokens(graph)
    largest = dict(tokens)
    for actor in order:
        _fire(graph, actor, tokens)
        for key, value in tokens.items():
            largest[key] = max(largest[key], value)
    return largest
