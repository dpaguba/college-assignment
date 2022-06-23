# Division

Division answers a question with "for all" in it. `R ÷ S` returns the values
that appear in `R` together with every tuple of `S`.

The exercise asks for `R ÷ π(B←A,C)(S)`, so the divisor has schema `(B, C)`
and only the attribute `A` survives. The projection of `S` is
`{(1,x), (4,y)}`; of the two candidates `A = 1` and `A = 5`, only `1` occurs
with both, so the answer is `A = 1`, which is what the published solution
gives.

## Two independent computations

`divide` collects the partners of each candidate and compares sets.
`by_basic_operators` computes the same thing as
`π₁(R) − π₁((π₁(R) × S) − R)`: build every combination that would be needed,
subtract the ones that exist, and whoever is left over was missing something.
Both agree, and both agree with the doubly nested `NOT EXISTS` that sqlite3
evaluates.

That nesting is the reason division has its own symbol. Written out in SQL it
is a negation of a negation, which is exactly how the "for all" is expressed
in a language that only has "there exists".
