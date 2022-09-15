# Active automata learning

The observation table, Angluin's L*, the three kinds of equivalence query,
and the abstraction that decides what the alphabet is.

L* was checked on 55 random automata against an independently written
minimisation: every model learned was correct and had the minimal number of
states. The two things that break it are also measured: an equivalence oracle
that looks too shallow returns a one-state model for a four-state language,
and a mapper that conflates two actions makes the abstracted system
non-deterministic.
