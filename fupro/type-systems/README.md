# Type systems

| Topic | |
|---|---|
| [simply-typed](simply-typed/) | three rules and what they exclude |
| [unification](unification/) | making two types equal, minimally |
| [type-inference](type-inference/) | the principal type, without annotations |

Lecture 10. The block builds the inference twice: once directly from the
rules for the simply typed calculus, and once in the style of Hindley and
Milner where unification does the work.

The result that connects this block to the previous one is negative. Self
application has no type, so `OMEGA` is rejected, and with it every term that
fails to terminate. Typing buys termination and costs expressiveness, and the
recursion the previous block obtained from the Y combinator is precisely what
a simple type system cannot express.
