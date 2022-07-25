# Coding standards

A standard as executable rules, each tied to a quality attribute.

The exercise asks for a definition and three concrete, checkable rules linked
to quality attributes. The definition that matters is operational: a rule that
cannot be checked mechanically is a preference, and a rule that can be is a
standard, because a build can fail on it.

| Rule | Attribute | Limit |
|---|---|---|
| short-name | readability | 3 characters |
| long-function | maintainability | 60 lines |
| many-parameters | testability | 5 parameters |
| deep-nesting | readability | 4 levels |
| missing-docstring | understandability | public names |
| bare-except | reliability | none allowed |
| high-complexity | testability | 15 |

## Why each rule names an attribute

A rule without one is a habit nobody can argue with or against. Naming the
attribute makes the trade explicit: the parameter limit exists because each
parameter multiplies the combinations a test must cover, so relaxing it is a
decision about testing effort, not about taste.

## The exemptions matter as much as the rules

`short_names` exempts loop counters. `i` in a three-line loop is clearer than
`index_of_current_element`, and a rule that cannot make that distinction gets
switched off wholesale, which is worse than not having it. Every real standard
lives or dies on this: a rule with too many false positives is disabled, and a
disabled rule protects nothing.

`missing_docstring` exempts private names for the same reason: the standard
asks for an interface to be described, not for every helper to be narrated.

## Run on this repository

48 violations in `swk`, 75 in `dap2`, and most of both are nested helper
functions without docstrings. That is the acceptable case, and it is exactly
the kind of finding that decides whether a rule stays: either the rule learns
about nesting, or the team learns to ignore a third of its output.
