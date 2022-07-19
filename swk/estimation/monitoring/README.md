# Monitoring: goal, question, metric

The exercise asks for a goal, three questions, and a metric for each. That
order **is** the method.

A metric chosen before the question it answers measures whatever was easy to
collect, and the team then optimises that. GQM, from Basili and Rombach, is
the discipline of the arrow: goal to question to metric, never backwards.

## The example, as the exercise sets it

```
Goal: improve the conversion rate of mobile app onboarding,
      from the view of the product team

  Q1: How many users who start onboarding finish it?
      M: onboarding completion rate            [share, better up]
  Q2: How long does finishing take?
      M: median time to finish onboarding      [seconds, better down]
  Q3: Where exactly do users give up?
      M: step with the largest drop-off        [step number, better down]
```

The three metrics are deliberately of different kinds: a rate, a duration and
a location. A tree with three variations of the same number answers one
question three times and calls it three.

## KPIs need a decision attached

The second field of every KPI here is the decision it supports:

| KPI | Decision it supports |
|---|---|
| activation rate | keep investing in onboarding, or move on |
| day 30 retention | does the product deliver lasting value |
| crash-free sessions | next sprint on features or on stability |

An indicator nobody would act on differently is a number on a dashboard.
Naming the decision is the cheapest test for whether it belongs there.

## Goodhart's law, made checkable

A measure that becomes a target stops being a good measure.
`goodharts_warning` looks for the pattern in a history: the indicator rises
steadily while the outcome it stands for does not move. That is a crude test
of a real failure, and it is worth running against any metric that has been
on a wall for a quarter.
