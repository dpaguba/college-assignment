"""Loading: the tricks that make a bulk insert finish in the window.

The lecture lists them and the reason is the same in every case: a warehouse
load writes millions of rows into a table nobody is reading at that moment,
so the machinery that protects concurrent transactions is pure overhead.

Turning off logging, pre-sorting the data, dropping the indices and
rebuilding them afterwards, and truncating before a full reload are all the
same move: pay a fixed cost once instead of a small cost per row.
"""


def tricks():
    """The techniques the lecture names."""
    return ["turn off logging", "pre-sort the data",
            "drop and rebuild the indices", "truncate before a full reload",
            "load in parallel", "disable constraint checking"]


def compare(rows, row_cost=1.0, bulk_cost=0.05, fixed=1000.0):
    """The cost of a bulk load against inserting row by row."""
    return {"row by row": rows * row_cost,
            "bulk": fixed + rows * bulk_cost}


def rebuild_is_better(share, index_cost=5.0, rebuild_cost=1.0):
    """Whether rebuilding the index beats maintaining it during the load.

    Maintaining costs per inserted row and rebuilding costs per table row, so
    the answer depends only on the share of the table that is being loaded.
    """
    return share * index_cost > rebuild_cost


def window_hours(mode):
    """How long the load window is under each loading strategy."""
    windows = {"nightly": 6.0, "hourly": 0.5, "near real time": 0.01}
    if mode not in windows:
        raise ValueError("unknown mode: %s" % mode)
    return windows[mode]
