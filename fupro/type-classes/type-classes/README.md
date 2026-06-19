# Type classes

A class declares methods and may supply defaults; an instance fills in the
rest for one type. Resolution happens on the **type**, not on the value,
which is what separates a type class from an object's method table: an
instance can be added for a type that was written long before the class.

```haskell
class Eq a where
  (==) :: a -> a -> Bool
  (/=) :: a -> a -> Bool
  x /= y = not (x == y)      -- default
```

The default is why an instance needs one method and gets two. The module
reproduces that: `resolve("Eq", "Int")` returns both, with the second built
from the first.

## Constraints

An instance for a parametrised type may need one for the parameter. Lists can
be compared exactly when their elements can, and the module derives the list
instance from the element instance rather than declaring one per element
type. That derivation is the constraint written before the arrow in a Haskell
instance head, and it is what makes a single definition cover infinitely many
types.

A superclass makes its methods available to the subclass, which the module
checks by resolving `Ord` and calling an `Eq` method on the result.
