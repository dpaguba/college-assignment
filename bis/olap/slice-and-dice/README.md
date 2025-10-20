# Slicing and dicing

Two operations that are easy to confuse because their results can be the same
size.

**Slicing** fixes one dimension to one value. That dimension then carries no
information and drops out: a three-dimensional cube becomes a two-dimensional
sheet. Slicing on Quartal = Q3 leaves 9 of the 24 rows and three axes instead
of four.

**Dicing** restricts several dimensions to a subset of their values each.
Every axis survives, just shorter. Dicing on Quartal in {Q4} and Risikoart in
{Technisch, Markt} leaves 10 rows and all four axes.

## Where the confusion comes from

Slicing on Q4 and dicing on {Q4} both leave 15 rows. The results are the same
rows and different cubes: one has three dimensions and one has four. Which
one is wanted depends on what comes next. If the next step compares quarters,
dropping the quarter axis has thrown away the thing being compared.
