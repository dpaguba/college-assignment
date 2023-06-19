# Context-free grammars

Rules of the form `A -> alpha`, where the left side is always a single
variable. That restriction is what "context-free" means: a variable is
replaced without looking at what surrounds it.

The step up from regular languages is real. A rule can put symbols on **both**
sides of a recursive call, which is what makes `a^n b^n` expressible here and
impossible one level down.

## Deriving forwards is the definition, not a parser

`derivations` searches sentential forms breadth-first with two prunings, and it
exists so a derivation can be printed the way an exercise asks. For deciding
membership use [CYK](../cyk/): cubic, complete, and unaffected by how the
grammar is written.

## Ambiguity

`is_ambiguous` looks for a word with two parse trees, by counting parses with
CYK rather than enumerating them, since the number of trees grows much faster
than the number of words.

It can only ever find a **witness**. Ambiguity of a context-free grammar is
undecidable, so a search that finds nothing has proved nothing, and the
docstring says so. On the usual expression grammar `S -> S+S | S*S | (S) | a`
it finds `a*a*a` immediately.

## The notation

```
S -> Dd | Aa | aE
A -> Da | aD | B
```

Variables are the symbols that appear on a left-hand side, so a multi-character
name like `Wa` works as long as it has its own rule. Right-hand sides are
tokenised by longest match against that set, which is what makes `Dd` two
symbols and `Wa` one.
