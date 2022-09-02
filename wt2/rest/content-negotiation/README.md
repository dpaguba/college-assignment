# Content negotiation

The caller says what it can read, the service says what it can produce, and
the two are matched. The quality value orders the wishes; the more specific
pattern wins at equal quality; the position in the header breaks the
remaining ties.

Checked against a table of cases:

| Accept | offered | chosen |
|---|---|---|
| `application/json` | json, xml | json |
| `application/xml;q=0.5, application/json;q=0.9` | xml, json | json |
| `*/*` | json | json |
| `text/csv` | json | none, 406 |
| `application/*;q=0.9, application/json;q=0.8` | xml, json | xml |
| `application/json;q=0` | json | none |

The fifth row is the one worth noting: the wildcard has the higher quality,
so it wins even though the exact type is also acceptable. A quality of zero
means "not this one", not "no preference".

## Vary

The answer must say which header it varied on. A cache that stores a JSON
answer without `Vary: Accept` will hand it to the next caller who asked for
XML.
