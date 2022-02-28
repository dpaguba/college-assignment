# Well-founded orders

An order is well founded when it has no infinite descending chain, which is
what makes induction over it valid and recursion over it terminate. On a
finite set it means the relation has no cycle, so the question is decidable,
and the module decides it by repeatedly removing minimal elements.

## Three ways to prove termination

**A measure into the naturals.** A step that strictly decreases a natural
number can only be taken finitely often. This is the everyday argument and
the module checks it step by step over the reachable states.

**A lexicographic order.** The Ackermann function terminates while neither
argument decreases at every call: the pair decreases lexicographically, and
the pairs of naturals under that order are well founded. Checked here over
every call reachable from a starting pair.

**Noetherian induction.** A property that is preserved by every step and
holds initially holds everywhere reachable, which is the same principle as a
loop invariant, and the same computation.

The three are the same theorem seen from different sides, and the reason the
lecture presents all of them is that the measure is what one usually finds,
and the well-founded order is what actually justifies the argument.
