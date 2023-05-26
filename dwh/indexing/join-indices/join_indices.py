"""A join index: the result of a join, stored.

Instead of computing which fact rows match which dimension rows, store the
pairs. A join becomes a lookup, and the price is the space and the
maintenance: every load has to update the index as well as the tables.

The saving grows with the fact table, because the join it replaces does, and
the maintenance grows with the load rather than with the table, which is why
the trade favours a large warehouse loaded once a night.
"""


def build(dimension_rows, fact_rows):
    """The pairs of matching row identifiers."""
    index = {}
    keys = {key for key, _value in dimension_rows}
    for position, (key, _value) in enumerate(fact_rows):
        if key in keys:
            index.setdefault(key, []).append(position)
    return [(key, position) for key, positions in index.items()
            for position in positions]


def probe(index, key):
    """The fact rows matching a dimension key."""
    return [position for stored, position in index if stored == key]


def cost(fact_rows, dimension_rows):
    """The space and maintenance the index costs."""
    return {"index entries": fact_rows,
            "maintenance per load": fact_rows // 100,
            "bytes": fact_rows * 8}


def saving(fact_rows, dimension_rows=1000):
    """The comparisons the index avoids on one join."""
    return fact_rows * dimension_rows - fact_rows
