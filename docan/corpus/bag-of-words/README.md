# Bag-of-words

A vocabulary of the N most frequent terms, and one histogram over that
vocabulary per document. Words outside the vocabulary are dropped, so every
document becomes a vector of the same length and documents become comparable.

## What is thrown away

The order of the words, and with it the sentence. "The dog bites the man" and
"the man bites the dog" have the same histogram. So does every negation, and
every adjective's attachment.

It works anyway because the category of a text hangs on which words are used
and not on how they are arranged. It stops working exactly where the
arrangement carries the meaning, which is why the same representation is weak
at sentiment and strong at topic.

## Choosing the vocabulary by frequency

Frequency is a decision with consequences: it keeps what is common and
discards what is rare, although a rare word can be the one that gives a
category away. The method leans on the weighting to push the common words back
down afterwards, which means the two steps have to be read together.
