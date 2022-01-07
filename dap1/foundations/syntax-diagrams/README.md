# Syntax diagrams

The first sheet describes arithmetic expressions in nine rules of prose:
an expression begins with a letter or a bracket, an operator must be preceded
by a letter or a closing bracket, two letters may not follow each other, no
prefix may contain more closing brackets than opening ones, and so on. The
published solution replaces all nine with two diagrams.

```
Atom       ::= letter | "(" Expression ")"
Expression ::= Atom [ ("+" | "*") Expression ]
```

Every one of the nine rules follows from these two, and the solution says the
diagram is easier to read than the prose. There is a stronger claim available,
and it can be checked:

| Input | Published diagram | Expression, operator, expression |
|---|---:|---:|
| `u+v+w` | 1 derivation | 2 |
| `u+v*w+x` | 1 | 5 |

The obvious first attempt at a grammar, an expression being two expressions
with an operator between them, is ambiguous: `u+v+w` can be built by grouping
either pair first. The published diagram is not, because the left operand of
an operator is an atom rather than an expression, so the grouping is forced.
The counts come from a chart over spans, so they are counts of parse trees
rather than counts of one parser's backtracking.

The identifier diagram is the simpler one and makes the same point about
where a rule belongs: at least one character, a letter or underscore first,
letters, digits or underscores afterwards. Three prose conditions, one
diagram, no room for a reading that satisfies all three and is still wrong.
