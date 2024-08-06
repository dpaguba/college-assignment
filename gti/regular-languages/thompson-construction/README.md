# Thompson's construction

A regular expression becomes an epsilon-NFA. The easy direction of Kleene's
theorem, by induction over the five syntactic cases.

Every fragment keeps two invariants, and they are what make gluing safe:

- exactly one start state and exactly one accepting state
- nothing enters the start state, nothing leaves the accepting one

So fragments compose without interfering, and the automaton has at most twice
as many states as the expression has symbols and operators. `size_bound`
computes that number, and it matches: `a(a|b)*b` gives 12 states, predicted 12.

## Why the epsilon transitions

Merging states instead of joining them with epsilon steps would be smaller and
would break the invariants. The union case is the clearest: without a fresh
start, the two branches would share a state that has incoming edges from
outside the fragment, and the star built around it would then accept words that
interleave the branches.

Linear size is exactly why compilers use this construction rather than a
smarter one: the automaton is built once and determinised on demand.
