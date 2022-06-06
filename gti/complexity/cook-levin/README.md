# Cook and Levin

The theorem that starts the whole subject: SAT is NP-complete, proved directly
rather than by reduction from something else.

A computation becomes a formula, so that

```
the formula is satisfiable  <=>  the machine accepts the input within t steps
```

and a satisfying assignment **is** the computation, written out cell by cell.

## The tableau

One row per step, one column per tape cell. Variables say what is in each cell,
where the head is, and what state the machine is in. Four groups of clauses:

1. the first row is the start configuration
2. each cell holds exactly one symbol, the head is in exactly one place, the
   machine is in exactly one state
3. each row follows from the one above by the transition function, and cells
   away from the head do not change
4. the accepting state appears somewhere

## It runs, and the answer is readable

For the `a^n b^n` machine on input `ab` with 8 steps: **693 variables, 9585
clauses**, satisfiable, and decoding the assignment gives back the real run:

```
step 0: state scan    head 0  tape 'ab__________'
step 1: state right   head 1  tape 'Xb__________'
step 2: state back    head 0  tape 'XY__________'
step 3: state scan    head 1  tape 'XY__________'
step 4: state verify  head 2  tape 'XY__________'
step 5: state accept  head 2  tape 'XY__________'
```

which is exactly what the simulator does. On `ba` and `aab` the formula is
unsatisfiable, and the machine rejects.

## Why it needed a real solver

The brute force SAT solver is 2^n and the smallest useful formula here has 265
variables. That is not a rounding error, it is 10^79 assignments, so the
verification simply never returned until DPLL was added.

The size is polynomial in the step bound, which is the whole content of the
theorem: an accepting run of polynomial length becomes a formula of polynomial
size, so every problem in NP reduces to SAT.
