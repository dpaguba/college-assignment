# Code generation

From the checked syntax tree to something a machine can run.

| Topic | |
|---|---|
| [three-address-code](three-address-code/) | flattening trees into named instructions |
| [control-structures](control-structures/) | translating loops and conditionals into jumps |
| [array-addressing](array-addressing/) | from indices to a byte address |
| [register-allocation](register-allocation/) | which values share a register |
| [bootstrapping](bootstrapping/) | how a compiler for a language gets written in it |

## The recurring shape

Each of these replaces something structured by something flat: a tree by a
list, a loop by labels and jumps, an array index by arithmetic, a variable by a
register number. Every step loses information the earlier phases needed and the
machine does not have, which is why they happen in this order and not another.
