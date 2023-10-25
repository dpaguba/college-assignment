"""The four scales, and the operation each one permits.

Nominal values can only be compared for equality, ordinal ones can be
ordered, interval ones can be subtracted, and only ratio ones can be divided,
because only they have a true zero. Twenty degrees Celsius is not twice ten,
and a penguin of four kilograms is twice one of two.

The lecture adds a second axis: whether the data has a schema. A relational
table does, plain text does not, and half of the engineering effort in a data
project is turning the second into the first.
"""

SCALES = {"species": "nominal", "island": "nominal", "sex": "nominal",
          "rating": "ordinal", "class": "ordinal",
          "temperature_celsius": "interval", "year": "interval",
          "body_mass_g": "ratio", "bill_length_mm": "ratio",
          "count": "ratio"}
"""The scale of the columns used in this subject."""

OPERATIONS = {"nominal": ["equality"],
              "ordinal": ["equality", "order"],
              "interval": ["equality", "order", "difference"],
              "ratio": ["equality", "order", "difference", "quotient"]}
"""What each scale permits."""


def scale(column):
    """The scale of a column."""
    if column not in SCALES:
        raise ValueError("unknown column: %s" % column)
    return SCALES[column]


def allows(scale_name, operation):
    """Whether a scale permits an operation."""
    if scale_name not in OPERATIONS:
        raise ValueError("unknown scale: %s" % scale_name)
    return operation in OPERATIONS[scale_name]


def doubling_is_meaningful(column):
    """Whether saying one value is twice another means anything."""
    return allows(scale(column), "quotient")


def has_schema(source):
    """Whether the source carries a schema of its own."""
    schemas = {"relational table": True, "csv with a header": True,
               "json document": True, "plain text": False, "image": False,
               "log file": False}
    if source not in schemas:
        raise ValueError("unknown source: %s" % source)
    return schemas[source]
