"""The star: one fact table, dimensions around it, nothing else.

Every dimension is joined directly to the fact table and no dimension joins
another, so a query touches the fact table and the dimensions it filters on
and never a chain of tables. The shape is what makes the query plan
predictable, and predictability is what an optimiser needs on a table with a
hundred million rows.

The fact table holds nearly all the rows: in the example it is a thousand
times the size of everything else together, which is why the design spends
its normalisation budget there and nowhere else.
"""


def example():
    """A retail star with three dimensions."""
    return {"fact": {"name": "sales", "rows": 10 ** 7,
                     "references": ["product", "time", "store"]},
            "dimensions": {"product": {"rows": 10 ** 4, "references": []},
                           "time": {"rows": 3650, "references": []},
                           "store": {"rows": 200, "references": []}}}


def is_star(schema):
    """Whether the fact table references every dimension and they none."""
    names = set(schema["dimensions"])
    if set(schema["fact"]["references"]) != names:
        return False
    return all(not dimension["references"]
               for dimension in schema["dimensions"].values())


def sizes(schema):
    """The row count of every table."""
    result = {schema["fact"]["name"]: schema["fact"]["rows"]}
    for name, dimension in schema["dimensions"].items():
        result[name] = dimension["rows"]
    return result


def plan(schema, filtered):
    """The joins a query needs, which is one per filtered dimension."""
    unknown = set(filtered) - set(schema["dimensions"])
    if unknown:
        raise ValueError("no such dimension: %s" % sorted(unknown))
    return {"fact table": schema["fact"]["name"], "joins": len(filtered),
            "tables": 1 + len(filtered)}
