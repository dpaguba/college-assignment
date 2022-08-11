# Abstraction

The learner needs an alphabet; the application has requests. The mapper
between them decides what can be learned.

Five concrete actions map to three letters here: the three GET requests all
become "view a page", because for the protocol being learned they behave the
same.

## What a coarse mapper destroys

Map log in and log out to the same letter and the abstracted system stops
being deterministic: the same word leads to different states depending on
what the letter meant that time. No automaton describes it, and the learner
either fails to terminate or returns something that fits none of the
observations.

Parameters are the other trap. An identifier in the path yields infinitely
many letters; the usual answer is to map it to a few classes such as own,
other and missing.

## What is learned

Not the application, but its image under the abstraction. What the mapper
conflates the model cannot separate; what it omits does not appear. A wrong
mapper produces a model that is internally consistent, passes every
equivalence check, and describes something other than the system in front of
you.
