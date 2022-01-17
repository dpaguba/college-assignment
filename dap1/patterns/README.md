# Design patterns

| Topic | |
|---|---|
| [iterator](iterator/) | separating the walk from the thing walked |
| [strategy](strategy/) | separating the computation from the traversal |

Two patterns, and one idea between them: an algorithm and a structure that
know about each other multiply, and an interface between them stops the
multiplication.

The iterator lets one comparison method serve every structure that can produce
one, and lets a structure be walked in ways it was never written for. The
strategy lets one traversal serve fourteen computations, which is what the
tenth sheet asks for and what makes the point at that scale: the list is
written once and never changes, and each new question is a new small class.

Chapters fifteen to seventeen of the lecture apply both to the pattern
recognition project, where the strategy chooses the matching algorithm and the
iterator walks the candidate positions. That part is a Swing application and
is not implemented here, since the parts of it worth checking are the two
patterns themselves.
