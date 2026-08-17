# The abstract syntax tree

A parse tree records how the parser worked: a node per rule application, the
chains `E ::= T ::= F` that exist only to encode precedence, the brackets that
exist only to override it. A syntax tree keeps the operators and the operands.

The precedence is not lost. It has been **absorbed into the shape**: the parse
tree encodes it in the derivation, the syntax tree in which node is whose child.

| expression | parse tree | syntax tree | height |
|---|---|---|---|
| `num` | 4 | **1** | 1 |
| `num + num` | 9 | 3 | 2 |
| `num + num * num` | 13 | 5 | 3 |
| `(num + num) * num` | 18 | 5 | 3 |
| `num - num - num * num` | 18 | 7 | 3 |

The two bracketed forms are the interesting rows: `(num+num)*num` needs 18 parse
nodes against 13 for the unbracketed version, and both give a 5-node syntax
tree. The brackets did their work during parsing and have nothing left to say.

## The shape is a choice

The fold is driven by a table saying, per rule, whether to build a binary node,
drop brackets, collapse a chain or keep a leaf. Writing it out separately makes
visible that a compiler chooses the shape of its syntax tree; the grammar only
constrains which shapes are reachable.

## What the shape buys

Evaluation is a five-line tree walk, and it gets the answers right because the
tree already says what belongs to what: `2+3*4` is 14, `(2+3)*4` is 20, and
`10-3-2` is 5 rather than 9, because subtraction came out left-associative.

Printing the tree back to tokens and reparsing gives the identical tree, with
brackets re-inserted only where the shape requires them. That round trip is the
test that the tree really carries the precedence rather than merely having been
built from something that did.
