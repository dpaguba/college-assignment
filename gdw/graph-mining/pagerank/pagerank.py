"""PageRank: the stationary distribution of a random surfer.

The rank of a page is the probability that a surfer who follows links at
random and occasionally jumps to a random page is looking at it. Two details
make the definition work: the damping factor, which is the chance of
following a link rather than jumping, and the handling of pages with no
outgoing links, whose probability would otherwise leak away.

The exercise graph has five nodes, and node 3 comes out on top because it is
the only one reached from both 2 and 4 as well as from 5.
"""


def _structure(edges):
    """The nodes and the outgoing links of a graph."""
    nodes = sorted({node for edge in edges for node in edge})
    outgoing = {node: [] for node in nodes}
    for source, target in edges:
        outgoing[source].append(target)
    return nodes, outgoing


def compute(edges, damping=0.85, tolerance=1e-10, limit=1000):
    """The ranks by power iteration."""
    nodes, outgoing = _structure(edges)
    count = len(nodes)
    ranks = {node: 1 / count for node in nodes}
    for _ in range(limit):
        following = {node: (1 - damping) / count for node in nodes}
        leaked = 0.0
        for node in nodes:
            targets = outgoing[node]
            if not targets:
                leaked += damping * ranks[node]
                continue
            share = damping * ranks[node] / len(targets)
            for target in targets:
                following[target] += share
        for node in nodes:
            following[node] += leaked / count
        if max(abs(following[node] - ranks[node]) for node in nodes) < tolerance:
            return following
        ranks = following
    return ranks


def solve_exactly(edges, damping=0.85):
    """The ranks as the solution of the linear system, as a cross-check.

    The power iteration converges to this vector, so computing it a second
    way is the check that the iteration was implemented correctly rather than
    merely converging to something.
    """
    nodes, outgoing = _structure(edges)
    count = len(nodes)
    matrix = [[0.0] * count for _ in range(count)]
    index = {node: position for position, node in enumerate(nodes)}
    for node in nodes:
        targets = outgoing[node]
        if not targets:
            for other in nodes:
                matrix[index[other]][index[node]] += damping / count
            continue
        for target in targets:
            matrix[index[target]][index[node]] += damping / len(targets)
    for row in range(count):
        for column in range(count):
            matrix[row][column] -= 1.0 if row == column else 0.0
    rows = [row + [-(1 - damping) / count] for row in matrix]
    rows[-1] = [1.0] * count + [1.0]
    solution = _gauss(rows)
    return {node: solution[index[node]] for node in nodes}


def _gauss(rows):
    """Solves a linear system given as an augmented matrix."""
    size = len(rows)
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(rows[row][column]))
        rows[column], rows[pivot] = rows[pivot], rows[column]
        divisor = rows[column][column]
        rows[column] = [value / divisor for value in rows[column]]
        for row in range(size):
            if row == column:
                continue
            factor = rows[row][column]
            rows[row] = [value - factor * other
                         for value, other in zip(rows[row], rows[column])]
    return [row[-1] for row in rows]
