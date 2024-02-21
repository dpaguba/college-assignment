# Shingling

A document becomes a set: the set of its windows of k consecutive characters
or words. Comparing documents then becomes comparing sets, which the rest of
the block can do quickly.

The window length decides how much order survives. Single characters keep
almost none, so any two English texts share nearly the same set. Long windows
keep so much that two documents share nothing unless they are nearly
identical. Two or three words is the usual compromise and is what the seventh
sheet uses.

Counting shingles measures variety and not length. A paragraph repeating one
sentence thirty times has as many distinct shingles as the sentence, which is
the trap in describing a corpus by its size.
