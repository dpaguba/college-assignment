# The Nerode relation

The states a language forces you to have.

```
x ~L y   iff   for every z:   xz in L  <=>  yz in L
```

**Myhill-Nerode:** L is regular exactly when `~L` has finitely many classes,
and then their number is the number of states of the minimal DFA.

That is the deepest statement of the first block. The minimal automaton is not
something a clever algorithm found; it is forced by the language itself, and
minimisation only computes what was already there.

## The exercise, reproduced

Sheet 3 gives a DFA and asks for words equivalent to given ones, then for the
classes as regular expressions. All four equivalences the solution states come
out:

| Words | Equivalent | Class |
|---|---|---|
| `aaa` ~ `a` | yes | both reach the same state |
| `bbb` ~ `b` | yes | |
| `aaaa` ~ `aa` | yes | |
| `abab` ~ `ab` | yes | the dead class |

and the index is 5, with the classes `{eps}`, `{a, aaa, ...}`, `{b, bb, ...}`,
`{aa, aaaa, ...}` and the dead words.

## Proving non-regularity with it

`lower_bound_witness` takes a family of words and checks that every pair is
separated by some continuation. An infinite family of pairwise separated words
means infinitely many classes, so the language is not regular.

For `a^n b^n` the family `eps, a, aa, aaa, ...` works, and each pair is
separated immediately. That argument is usually shorter than the
[pumping lemma](../pumping-lemma/), and unlike it, it is an
**exact characterisation**: pumping can fail to prove non-regularity for a
language that really is irregular, while Nerode never does.

## From a language rather than an automaton

`classes_from_language` groups short words by their behaviour on short
continuations. It is a test with the same limitation as any bounded check: two
words that look equal here might be separated by a longer continuation.
