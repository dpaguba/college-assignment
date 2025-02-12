# Substitution cipher

Each letter is mapped to an arbitrary but fixed other letter. The key space
is 26 factorial, about 4·10²⁶, which is far too large to search and entirely
beside the point.

The encryption renames the letters; it does not change how often they occur.
`frequencies_are_preserved` checks that directly: the sorted list of
frequencies before and after is the same list. The same holds for pairs and
for quadruples, and that is what the attack uses.

## The attack

Start from the frequency comparison: the most common ciphertext letter is
mapped to the most common English letter, and so on down. That start is
usually wrong in detail and roughly right in shape. Then climb: run through
all 325 letter pairs, swap each one, keep the swap when the text scores
better, and repeat until a full pass improves nothing. Several restarts with
a slightly disturbed start get past local maxima.

The score has three parts: letter pairs, letter triples, and the letters
standing in a recognised word. The pairs give a smooth gradient for the climb
to follow; the triples separate the good mappings from the nearly good ones.
Unseen groups get a smoothed value rather than a fixed penalty, which keeps
the score from falling off a cliff at every rare combination.

The word part is what finishes the job. On the groups alone the climb stops
at eighty-five percent: the common letters are right and the rare ones sit in
a cycle that no single swap can undo, because *development* and *dekelobment*
score almost the same. As words they do not: *of* is a word and *om* is not,
and one swap then pays for itself. The list is a hundred ordinary English
function words.

Both the tables and the word list are ordinary English that has nothing to do
with the answer, so the method is not quietly recognising the text it is
supposed to find.

## Exercise 5.2

The ciphertext is the opening of C. E. Shannon's *A Mathematical Theory of
Communication* (1948), beginning "the recent development of various methods
of modulation such as pcm and ppm". Recovering the author was the second half
of the question, and the text names Nyquist and Hartley in its first
paragraph, which identifies it even before the decryption is complete.

## Why the key space does not save it

A large key space only helps when nothing but the key distinguishes the
candidates. Here the statistics of the language point at one of them, and the
search never has to look at the other 10²⁶.

`length_matters` makes the same point from the other side. On the first fifty
characters the statistics are too thin to decide and the recovered text is
partly wrong; on the full passage they decide it completely. What the attack
needs is not computation but material.
