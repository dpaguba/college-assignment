# Estimation and measurement

Five modules for the planning half of the course: point estimation, velocity,
planning poker, monitoring, and A/B testing.

| Folder | Question it answers |
|---|---|
| [point-estimation](point-estimation/) | how long will this take, and how sure are we |
| [velocity](velocity/) | how much does this team actually finish |
| [planning-poker](planning-poker/) | how do several opinions become one number |
| [monitoring](monitoring/) | is the thing we built doing anything |
| [ab-testing](ab-testing/) | did our change cause it |

## The thread through all five

Every one of them is about **uncertainty that people would rather round away**.

A three-point estimate produces a range and the plan quotes the middle.
Velocity has scatter and the roadmap uses the best sprint. A p-value bounds one
kind of error and gets read as the probability of being right. In each case the
number that survives into the slide deck is the one with the uncertainty
removed.

So each module reports the spread as well as the value: a one-sigma interval
and a probability of hitting the budget, a velocity range with the
over-commitment signal, a confidence interval instead of a point, and a
simulation of what peeking does to the error rate.

## Verification

The two published examples both come out: the game project totals 248 hours by
two-point and 250 by three-point estimation, and the ten-story board gives
velocities 11, 11, 10, 5, 4 with the burndown reaching zero.

Where the course publishes no answer, the numbers were checked against an
independent computation: Monte Carlo over beta-PERT samples against the closed
form, and a simulation of repeated significance testing against the nominal
error rate.

The Monte Carlo check found something worth keeping: the lecture's
`S = (b - a) / 6` understates the spread by about ten per cent on skewed
packages, because it is exact only for a symmetric distribution.
