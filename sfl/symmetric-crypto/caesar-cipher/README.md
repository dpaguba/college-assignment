# Caesar cipher

Every letter is shifted by the same amount. Twenty-six keys, so breaking it
means trying all of them and reading which output is English; the module
scores the candidates by counting common words and returns the winner.

## Exercise 5.1

The ciphertext decodes with **key 13** to

> A cryptographic system should be secure even if everything about the
> system, except the key, is public knowledge.

which is Kerckhoffs's principle, and it is the reason the exercise uses this
particular sentence. A cipher whose design has to stay secret cannot be
reviewed, so its flaws are found by whoever looks hardest rather than by
whoever is friendliest. Both the key and the plaintext match the published
solution.

Case and punctuation survive the shift, which is itself a leak: word lengths
and the shape of the sentence are visible before any letter is decided.

## Why it fails

Twenty-six keys is a few seconds by hand. The letter frequencies are moved
rather than changed, so the histogram alone gives the key away. One known
plaintext letter fixes it completely. And the same letter always maps to the
same letter, which is the property the next module attacks.
