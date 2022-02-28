"""Well-founded orders, which are what makes induction and recursion work.

An order is well founded when it has no infinite descending chain. On a
finite set that is the same as having no cycle, which is why termination of a
finite state process can be decided, and why a measure into the naturals is
the standard way to prove that a program stops.
"""


def is_well_founded(relation):
    """Whether the relation has no cycle, so every descent is finite."""
    nodes = {node for pair in relation for node in pair}
    remaining = set(nodes)
    edges = set(relation)
    while remaining:
        minimal = {node for node in remaining
                   if not any(source == node for source, target in edges
                              if target in remaining)}
        if not minimal:
            return False
        remaining -= minimal
        edges = {(source, target) for source, target in edges
                 if source in remaining and target in remaining}
    return True


def lexicographic_less(left, right):
    """Whether the first tuple precedes the second lexicographically."""
    for first, second in zip(left, right):
        if first != second:
            return first < second
    return len(left) < len(right)


def terminates(successors, start, measure, limit=1000):
    """Whether the measure strictly decreases along every step from the start.

    A decreasing measure into the naturals is a well-founded order pulled
    back along the state space, which is the standard termination argument
    and the one this function checks step by step.
    """
    seen = set()
    frontier = [start]
    steps = 0
    while frontier:
        steps += 1
        if steps > limit:
            return False
        state = frontier.pop()
        if state in seen:
            continue
        seen.add(state)
        for following in successors(state):
            if measure(following) >= measure(state):
                return False
            frontier.append(following)
    return True


def ackermann_decreases(first, second):
    """Whether every Ackermann call decreases the argument pair lexicographically.

    The function is the standard example of a recursion that terminates
    without any single argument decreasing. The pair does, which is why the
    lexicographic order on pairs is the right well-founded order for it.
    """
    calls = [(first, second)]
    seen = set()
    while calls:
        state = calls.pop()
        if state in seen:
            continue
        seen.add(state)
        left, right = state
        if left == 0:
            continue
        if right == 0:
            following = (left - 1, 1)
        else:
            inner = (left, right - 1)
            if not lexicographic_less(inner, state):
                return False
            calls.append(inner)
            following = (left - 1, 1)
        if not lexicographic_less(following, state):
            return False
        calls.append(following)
    return True


def holds_everywhere(successors, start, claim, limit=1000):
    """Whether the claim holds in every state reachable from the start."""
    seen = set()
    frontier = [start]
    while frontier:
        if len(seen) > limit:
            raise ValueError("the state space exceeded the limit")
        state = frontier.pop()
        if state in seen:
            continue
        seen.add(state)
        if not claim(state):
            return False
        frontier.extend(successors(state))
    return True
