# Velocity

Story points completed per sprint, and what they forecast.

Story points measure size, not hours. Velocity is the only bridge between the
two, and it is **measured**, never estimated, which is what makes it reliable and
what makes it useless for a team that has not run any sprints yet.

## The exercise, computed

Ten stories over five sprints from sheet 2:

| sprint | planned points | actual points | completed |
|---|---|---|---|
| 1 | 15 | 11 | U2, U3, U4 |
| 2 | 16 | 11 | U1, U5, U7 |
| 3 | 15 | 10 | U6, U8 |
| 4 | 9 | 5 | U9 |
| 5 | 4 | 4 | U10 |

```
     start |########################################| 41
   after 1 |#############################           | 30
   after 2 |###################                     | 19
   after 3 |#########                               | 9
   after 4 |####                                    | 4
   after 5 |                                        | 0
```

## Partial credit is deliberately not given

A story half finished at the end of a sprint contributes nothing. That looks
harsh and it is the point: partial credit smooths the number, and a smooth
velocity signals nothing. The burndown above is readable precisely because
each step is a story that is actually done.

## Median, not mean

The lecture's rule: velocity settles after about three sprints, and from then
on the planning number is the median of recent ones. A median survives one
sprint where half the team was ill; a mean does not.

For this board the median of the last three is 5, against a first-sprint
velocity of 11. Planning at 11 would be planning on the best week the team ever
had.

## The signals the tool reports

Two fire on the exercise data:

- velocity ranges from 4 to 11, so a median hides more than it says
- only 41 of 59 committed points were finished, so the team is systematically
  over-committing

Both are what the exercise's third question asks for in words. A forecast from
a number with that much scatter is arithmetic, not a plan, and saying so is
more useful than the forecast.
