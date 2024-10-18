# Relationships and cardinalities

A relation is a diamond connecting at least two entity types, and it is named
after a noun. `Besuch`, not `hört`: a verb fixes a reading direction that the
relation does not have, and the other direction then has to be phrased
awkwardly.

## The (min,max) notation

Two numbers per side. The **minimum** says how often an entity **must** take
part, the **maximum** how often it **can**. An `n` stands for no fixed upper
bound.

Reading `(0,n)` on both sides of Studierende and Vorlesung: a student may
attend no course at all and up to n; a course may go unattended and be
attended by up to n students. Both zeros are deliberate, and both would be
wrong in a system where enrolment is mandatory.

`kind` derives the familiar 1:1, 1:n and n:m from the two maxima, which is
the only thing those labels ever meant.

## Why n and not a number

A number in the maximum is a business rule, not a property of the data.
Writing five because nobody currently takes more than five courses means
changing the model the day somebody takes six. Write a number only where the
rule is actually enforced.

## Parallel edges

An entity type can relate to itself, and then both ends of the diamond touch
the same rectangle. Two shapes recur: a **hierarchy**, where each entity has
at most one above it and any number below, and a **network**, where both
sides are unbounded. The difference is one character in the notation and the
whole difference between an organisation chart and a friend list.
