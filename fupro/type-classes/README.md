# Type classes

| Topic | |
|---|---|
| [type-classes](type-classes/) | interfaces resolved on the type |
| [functor](functor/) | one method, two unchecked laws |
| [applicative](applicative/) | a function inside the container |
| [monad](monad/) | sequencing with a context |
| [monad-laws](monad-laws/) | what the compiler does not verify |

Lectures 5 to 7. The ladder is Functor, Applicative, Monad, and each step
adds one operation and a few laws, so a monad is a functor that can do more
rather than a different thing.

The theme is the laws. None of them is checked by a compiler, all of them are
relied on by code that uses the class, and every one is checked here by
running both sides on samples. A deliberately broken instance is included at
each level, and in every case the first law catches it.
