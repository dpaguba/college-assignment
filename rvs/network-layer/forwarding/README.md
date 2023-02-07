# Forwarding

A forwarding table maps prefixes to interfaces and a lookup takes the **most
specific** match. That rule is what lets a default route coexist with
exceptions, and it is why the order of the entries does not matter:

| address | matched by | interface |
|---|---|---|
| `9.23.97.5` | `9.23.96.0/21` | eth0 |
| `9.23.104.9` | `9.23.104.0/22` | eth1 |
| `9.23.200.1` | `9.23.0.0/16` | eth2 |
| `10.0.0.1` | `0.0.0.0/0` | default |

The default route is not a special case in the lookup. It is the same rule
applied to the least specific possible entry.

## Aggregation keeps the table finite

Two sibling `/25` blocks pointing at the same interface merge into one `/24`.
The check that they are **siblings** rather than merely adjacent is what makes
it safe: a prefix must start at a multiple of its size, so only one of the two
possible pairings is a valid merge.

Verified as a behaviour rather than a shape: after aggregation, every address
tried resolves to the same interface it did before.
