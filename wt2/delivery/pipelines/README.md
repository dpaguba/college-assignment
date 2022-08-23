# Pipelines

Stages run in order and the first failure stops the rest, so a failing test
means no deploy stage runs at all.

## Order matters for the cost of failure

A five-second check that fails, followed by a five-minute test suite:
running the fast check first costs 5 seconds to learn the change is broken,
running it last costs 305. Same stages, same outcome, sixty times the
feedback delay.

Stages that do not need each other run together: three independent checks of
120, 90 and 30 seconds take 240 in sequence and 120 in parallel.

## The three continuous practices

| practice | builds every change | ready to release | releases automatically |
|---|---|---|---|
| integration | yes | | |
| delivery | yes | yes | no |
| deployment | yes | yes | yes |

The difference between the last two is a decision, not a technique. Delivery
means it could be released at any moment; deployment means it is, without
anyone deciding.

What a pipeline needs: everything in version control including the
configuration, a build that runs the same everywhere, tests that say why they
failed, a fast first stage, and the same artefact carried through every
stage rather than rebuilt at each one.
