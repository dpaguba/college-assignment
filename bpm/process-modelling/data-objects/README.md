# Data objects and data stores

A **data object** belongs to one process instance and disappears with it. A
**data store** sits beside the process and is read and written by every
instance. That single difference decides which of the two a model needs.

Associations are dashed arrows and are not control flow: they say what an
activity reads and writes, not what runs when.

## The two findings

`check` compares the associations against the order of the activities and
reports two things:

- an object **read before it was ever written**, which means the model does
  not say where the value comes from;
- an object **written and never read**, which means it is unclear why the
  activity produces it.

The first is the one that stops an automation project. Conditions on
gateways read values, and a conceptual model usually leaves those values out:
the participants take them for granted, and nobody writes down what everybody
knows. The engine does not know it, and the gateway has nothing to evaluate.
