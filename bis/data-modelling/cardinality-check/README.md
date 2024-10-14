# Checking cardinalities against the data

A diagram says what is allowed. A database says what is there. This module
counts, for every entity, how many relationships it actually takes part in,
and compares that against the (min,max) pair.

Two kinds of violation come out: an entity below the minimum, which means a
required link is missing, and one above the maximum, which means there are
too many.

## The asymmetry worth knowing

The maximum is the easy half. A `(0,1)` on one side becomes a foreign key,
and the database enforces it without anybody thinking about it again. The
minimum is the hard half: no foreign key can express that every course must
have at least one student, because the constraint concerns rows that do not
exist yet.

So the gap between model and data almost always opens on the minimum side,
and it opens quietly. That is why the check has to run against the data
rather than against the diagram.
