# Independence

Two events are independent when their probabilities multiply. That is a
statement about numbers, not about causation, and it is stronger than it
looks in one direction and weaker in another.

**Pairwise is not jointly.** Two fair coins give three events: the first is
heads, the second is heads, and they agree. Every pair is independent, and
knowing any two determines the third, so the three are not independent
together. The module builds the example and checks both halves.

**Neither inequality holds in general.** The fourth sheet asks whether the
probability of an intersection is always at or above, or always at or below,
the product of the probabilities. Neither: an event with itself is above,
disjoint events are below, and the module exhibits both in the same space.

**Independence depends on what is known.** Two independent events can become
dependent once a third is observed. That is why the word is always relative
to an information state, and why conditional independence is a separate
notion rather than a special case.
