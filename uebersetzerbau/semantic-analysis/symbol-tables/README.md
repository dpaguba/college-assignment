# Symbol tables

A grammar can say that an identifier may appear; it cannot say which
declaration it refers to. The rule for that is one line, and the whole
structure follows from it: **the innermost open declaration wins**.

So: a stack of scopes, a lookup that walks it from the top, a declaration that
checks only the topmost frame for duplicates.

| situation | result |
|---|---|
| `int x` then a block with `String x` | the block sees `String`, at depth 1 |
| leaving that block | `int` is visible again, at depth 0 |
| declaring `x` twice in one scope | `RedeclarationError` |
| declaring `x` in an inner scope | allowed, that is shadowing |
| using an undeclared name | `UndeclaredError` carrying the position |

Discarding a scope on exit is what makes shadowing work and what keeps a
compiler's memory use independent of how many blocks a program has. A tool that
needs the information afterwards, a debugger or an IDE, keeps the scopes as a
tree and pays for it.

## Classes are a second kind of scope

A name not found in a class is looked for in its superclass rather than in an
enclosing block. Fields and methods are both inherited, an overriding field
hides the inherited one, and the subtype relation is the reflexive transitive
closure of the same chain, which is why one structure holds all of it.

Inheritance cycles are rejected when the class is added, because every
operation on the table walks that chain and would otherwise not terminate.
