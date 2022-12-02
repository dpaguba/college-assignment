# Well-formedness

Four rules, checked on the graph:

- the chain begins and ends with events;
- events and functions alternate, connectors skipped;
- no deciding split directly after an event;
- no connector both branches and joins.

## Two ways to the same answer

`check` walks the edges. `alternation_holds` enumerates the paths from every
start to every end, strikes out the connectors and looks at what is left.
Two independent routes to the alternation rule, and on the example they
agree.

That is worth the duplication. The edge walk is local and fast and can miss a
case that only shows up along a path; the path enumeration is exhaustive and
would be too slow on a large model. Having both means a disagreement is a
signal.
