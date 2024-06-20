"""Kimball's four steps, in the order that makes the third answerable.

Select the business process, declare the grain, identify the dimensions,
identify the facts. The order is the content: the grain says what one row of
the fact table means, and until that is fixed there is no way to decide
whether an attribute is a dimension or whether a measure belongs in the
table at all.

The check the module performs is the one the order exists for: every fact has
to be measured at the declared grain or coarser. A fact at a finer grain
cannot be stored in a row that stands for something larger.
"""

STEPS = ["select the business process", "declare the grain",
         "identify the dimensions", "identify the facts"]
"""The four steps in order."""

GRAIN_SIZES = {"individual item": 10 ** 9, "line item": 10 ** 8,
               "receipt": 10 ** 7, "day and store": 10 ** 5,
               "month and region": 10 ** 3}
"""Rough row counts for the usual grains of a retail warehouse."""


def steps():
    """The four steps in order."""
    return list(STEPS)


def position(step):
    """Where a step sits in the sequence."""
    if step not in STEPS:
        raise ValueError("unknown step: %s" % step)
    return STEPS.index(step)


def example():
    """A retail design at the grain of one line item on a receipt."""
    return {"process": "retail sales", "grain": "line item",
            "dimensions": ["date", "product", "store", "promotion"],
            "facts": [{"name": "quantity", "grain": "line item"},
                      {"name": "amount", "grain": "line item"},
                      {"name": "daily_store_total", "grain": "day and store"}]}


def consistent(design):
    """Whether every fact is measured at the declared grain or coarser."""
    declared = GRAIN_SIZES.get(design["grain"])
    if declared is None:
        raise ValueError("unknown grain: %s" % design["grain"])
    for fact in design["facts"]:
        size = GRAIN_SIZES.get(fact["grain"])
        if size is None:
            raise ValueError("unknown grain: %s" % fact["grain"])
        if size > declared:
            return False
    return True


def row_estimate(grain):
    """How many rows a fact table at this grain holds."""
    if grain not in GRAIN_SIZES:
        raise ValueError("unknown grain: %s" % grain)
    return GRAIN_SIZES[grain]
