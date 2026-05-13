# Categories

Objects, arrows, composition, two laws: identities do nothing and composition
is associative. That is all, and the point of asking for so little is that so
much satisfies it.

The module builds a small category with three objects and checks both laws by
enumerating the arrows. A deliberately broken version with one composite
removed fails, which is what makes the check a check.

A functor is a map that preserves identities, sources, targets and
composition. The identity functor passes; a map that sends every arrow to an
identity fails on composition, and the module reports which.

What connects this to the rest of the course is that Haskell's `Functor` is
the same definition applied to one category: types are the objects, functions
are the arrows, and `fmap` is what a functor does to arrows. The laws in the
type class are the functor laws, which is why they cannot be dropped.
