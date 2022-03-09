# Countability

Two questions that look alike and have opposite answers.

**The pairs of naturals can be listed.** Cantor's pairing function is a
bijection from pairs to naturals, verified here on 400 pairs for injectivity,
by inverting it, and by checking that the first hundred naturals are all
reached.

**The rationals can be listed too.** Every rational appears exactly once in
the enumeration built from the pairing, which is the point: a listing needs
only to reach each element eventually, not in order.

**The infinite binary sequences cannot.** Given any listing, change the first
digit of the first sequence, the second of the second, and so on. The result
differs from every listed sequence in at least one place, so no listing is
complete. The construction assumes nothing about how the listing was
produced, which is what makes it a proof rather than an objection to a
particular attempt.

## The same argument, twice

Cantor's theorem for an arbitrary set is the diagonal again: for any map from
a set into its power set, the set of elements that their own image leaves out
is not an image of anything. Checked here over 200 sampled maps on a
five-element set, where the witness is found every time, because it exists
every time.

This is the one place in the course where a size question about infinite sets
has an answer that cannot be reached by counting, and it is the reason the
lecture spends a whole section on it.
