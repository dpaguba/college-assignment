# Data binding

One-way binding moves a value from the model to the view. Editing in the view
does not move it back, which the module verifies by editing and reading the
model. Two-way binding moves it in both directions and is what a form field
needs.

A change notifies only the bindings of that field: three bound fields, one
write, one notification. A framework that re-rendered everything on every
change would be simpler and is the usual reason an interface becomes slow.

## The two ways to notice a change

Dirty checking compares the values after every event and costs time in
proportion to the number of bindings. Observation announces the change and
costs a setter on every write. Which is better depends on how many bindings
there are and how often they change, and that is why frameworks have moved
between the two.
