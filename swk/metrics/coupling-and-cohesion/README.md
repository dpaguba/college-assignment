# Coupling and cohesion

The lecture defines both in words and states the rule: minimise coupling,
maximise cohesion, and expect the two to pull against each other.

This module turns the words into numbers using Robert Martin's package
metrics, because they can be computed from imports alone.

| Metric | Meaning |
|---|---|
| Ca, afferent | how many modules depend on this one |
| Ce, efferent | how many modules this one depends on |
| I = Ce / (Ca + Ce) | instability, from 0 (stable) to 1 (free to change) |

## What instability is not

It is not a quality score. A module with I = 0 is depended upon by everything
and therefore expensive to change; a module with I = 1 depends on everything
and can be rewritten freely. Both are fine.

The rule is about **direction**: dependencies should point from unstable
modules towards stable ones. A stable module depending on an unstable one is
the shape that hurts, and `violations` lists exactly those pairs.

## Cycles

Two modules that depend on each other cannot be understood, tested or released
separately, whatever the directory structure claims. `cycles` finds them with
Tarjan's algorithm, and a cycle is the strongest coupling signal there is:
everything else is a matter of degree, and this is a structural fact.

## Measured on this repository

```
while_language               Ca=15 Ce= 0 I=0.00
control_flow_graph           Ca= 7 Ce= 1 I=0.12
linear_arithmetic            Ca= 5 Ce= 1 I=0.17
dependency cycles: none
violations: 0
```

The most depended-upon module has no dependencies of its own, which is what a
layered design looks like from the outside. That was not planned as a
demonstration; it is what the analysis found when pointed at the folder next
door.
