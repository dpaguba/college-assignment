# Semantic analysis

Everything a compiler checks that a grammar cannot express.

| Topic | |
|---|---|
| [abstract-syntax-tree](abstract-syntax-tree/) | the parse tree with the grammar thrown away |
| [attribute-grammars](attribute-grammars/) | computing values on the tree, and when they can be computed |
| [symbol-tables](symbol-tables/) | which declaration a name refers to |
| [type-checking](type-checking/) | whether the operations agree with the types |

## The line this block draws

Syntax says which token sequences are programs. Semantics says which programs
mean anything. The three checks here are all of the second kind, and all three
are decided on the syntax tree rather than on the token stream, which is why
the tree is built at all.

The type checker is where the limits of static analysis become concrete. It
accepts a fragment that certainly fails at run time, and it is right to: the
alternative would reject every downcast, including the ones that work.
