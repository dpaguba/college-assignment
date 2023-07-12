# XPath

A path selects nodes: `/library/book` walks down from the root, `//title`
takes the descendant axis, `@year` reads an attribute, and a predicate in
brackets filters what a step found.

## Positions count per parent

`//b[1]` does not mean the first `b` in the document. The step is a child
step, so the position is counted within each parent, and on
`<l><b y=1/><b y=2/><c><b y=3/></c></l>` the answer is `y = 1` and `y = 3`.
The implementation therefore groups the descendant axis by parent instead of
flattening it, and `/l/b[2]` still returns the single `y = 2`.

An index past the end selects nothing rather than raising, matching XPath;
position zero is rejected, since XPath counts from one.

A predicate the module does not implement raises instead of being ignored. A
silently ignored predicate returns too many nodes and looks like a correct
answer, which is worse than an error.
