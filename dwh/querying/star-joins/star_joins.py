"""The star join, and the three plans for it.

The naive plan joins the fact table with each dimension in turn, so the first
join already produces an intermediate result the size of the fact table. Any
useful plan filters the dimensions first and uses the result to touch as
little of the fact table as possible.

The bitmap plan is the one the lecture builds towards: intersect the bitmaps
of the filtered dimensions and read only the fact rows that survive. On a
million rows with selectivities of one percent and ten percent, that is a
thousand rows instead of a million.
"""


def naive(dimensions, fact_rows):
    """Join the fact table with each dimension in turn."""
    return {"joins": len(dimensions), "intermediate rows": fact_rows,
            "fact rows read": fact_rows}


def with_filters(dimensions, fact_rows, selectivity):
    """Filter the dimensions first, then join, in the given order."""
    rows = fact_rows
    for dimension in dimensions:
        rows *= selectivity.get(dimension, 1.0)
    return {"joins": len(dimensions), "intermediate rows": rows,
            "fact rows read": fact_rows}


def bitmap_plan(fact_rows, selectivity):
    """Intersect the bitmaps and read only the surviving fact rows."""
    share = 1.0
    for value in selectivity.values():
        share *= value
    return {"fact rows read": fact_rows * share, "bitmaps": len(selectivity),
            "joins": 0}


def cost_of_order(order, selectivity, fact_rows):
    """The total intermediate rows produced by joining in this order.

    The most selective dimension first keeps every later intermediate result
    small, which is why the order matters even though the final answer does
    not depend on it.
    """
    rows = fact_rows
    total = 0.0
    for dimension in order:
        rows *= selectivity.get(dimension, 1.0)
        total += rows
    return total
