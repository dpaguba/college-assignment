"""Getting the data out of the source, and the row that is missing.

A full extraction reads everything and is simple and expensive. An
incremental one reads what changed, which needs the source to say what
changed, and the methods differ in what they can see.

A timestamp column sees inserts and updates and misses deletes entirely,
because a deleted row has no timestamp to read. Reading the log sees all
three, at the price of depending on a format the database vendor does not
promise to keep.
"""

CAPTURE = {"timestamp column": {"inserts": True, "updates": True,
                                "deletes": False},
           "trigger": {"inserts": True, "updates": True, "deletes": True},
           "log reading": {"inserts": True, "updates": True, "deletes": True},
           "full comparison": {"inserts": True, "updates": True,
                               "deletes": True}}
"""What each change data capture method can detect."""


def full(rows):
    """Every row of the source."""
    return list(rows)


def incremental(rows):
    """Only the rows marked as changed."""
    return [row for row in rows if row.get("changed")]


def capture_methods():
    """The methods the lecture lists."""
    return sorted(CAPTURE)


def detects_deletes(method):
    """Whether a method notices a deleted row."""
    if method not in CAPTURE:
        raise ValueError("unknown method: %s" % method)
    return CAPTURE[method]["deletes"]


def cost(method, table_rows, changed_rows):
    """How many rows the method reads.

    A full comparison detects everything and reads the whole table, so the
    choice is between completeness and cost, and the answer depends on how
    much a missed delete matters in the warehouse.
    """
    if method == "full comparison":
        return table_rows
    return changed_rows
