"""The snowflake: dimensions normalised into chains of tables.

Normalising a dimension removes the repetition of a category name across
thousands of product rows, and adds a join to every query that filters on it.
The saving is real and small, because the dimensions are small: in the
example it is under one percent of the schema, and the extra join is paid on
every query.

That asymmetry is the argument the lecture makes for the star. The fact table
is never normalised, because it is the table with all the rows and it has no
repeating attributes to remove.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "star-schema"))
import star_schema


def normalise(schema, dimension):
    """The schema with one dimension split into two tables."""
    result = {"fact": dict(schema["fact"]),
              "dimensions": {name: dict(value) for name, value
                             in schema["dimensions"].items()}}
    result["dimensions"][dimension] = dict(result["dimensions"][dimension])
    result["dimensions"][dimension]["references"] = [dimension + "_category"]
    result["dimensions"][dimension + "_category"] = {"rows": 50,
                                                     "references": []}
    return result


def normalises(table_kind):
    """Whether the design normalises tables of that kind."""
    if table_kind not in ("fact table", "dimension"):
        raise ValueError("unknown kind: %s" % table_kind)
    return table_kind == "dimension"


def compare():
    """The bytes and joins of a star against the snowflake of the same data."""
    star = star_schema.example()
    snowflake = normalise(star, "product")
    star_bytes = _bytes(star, category_inline=True)
    snowflake_bytes = _bytes(snowflake, category_inline=False)
    return {"star bytes": star_bytes, "snowflake bytes": snowflake_bytes,
            "saved bytes": star_bytes - snowflake_bytes,
            "total bytes": star_bytes,
            "star joins": 1, "snowflake joins": 2}


def _bytes(schema, category_inline):
    """A rough size, with the category name stored inline or referenced."""
    total = schema["fact"]["rows"] * 20
    for name, dimension in schema["dimensions"].items():
        width = 40
        if name == "product" and category_inline:
            width += 20
        total += dimension["rows"] * width
    return total
