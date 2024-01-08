# Subprocesses

A closed, coherent set of activities that reaches one result. Collapsed it is
a single box with a plus sign; expanded it is the detail.

The point is that both are the same model. The overview shows three boxes,
and the reader who needs the middle one opens it. A model with every activity
on one level is complete and unreadable, which is the state most real process
documentation is in.

`flatten` expands the whole hierarchy and returns the leaves; the example
turns three top-level activities into six. `depth` measures the nesting. Both
refuse a subprocess that contains itself, which would otherwise be an
infinite expansion.

## Embedded or called

An embedded subprocess belongs to its parent and is used only there. A call
activity refers to a process of its own that several parents invoke; it is
maintained once and changes everywhere at the same time. The second is the
right choice as soon as more than one process needs it, and the wrong one
before that, because it separates the definition from the only place that
reads it.
