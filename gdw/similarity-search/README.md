# Similarity search

| Topic | |
|---|---|
| [shingling](shingling/) | a document as a set |
| [jaccard](jaccard/) | the shared share |
| [minhash](minhash/) | estimating it without comparing |
| [locality-sensitive-hashing](locality-sensitive-hashing/) | finding the neighbours without all pairs |

The seventh lecture, and a chain in which each step removes one cost.
Shingling turns documents into sets, Jaccard compares two sets, MinHash
replaces the sets with short signatures, and banding replaces the comparison
of all pairs with a lookup.

The block's own defect is the one worth reporting. The textbook linear hash
family biased the MinHash estimate by 0.025 in both directions, which is
three times the sampling error and entirely invisible in a single run. It was
found by averaging over eight seeds and fixed by using a proper mixer.
