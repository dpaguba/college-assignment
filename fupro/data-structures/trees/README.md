# Trees

The exam's type:

```haskell
data Baum a = Leer | Knoten a (Baum a) (Baum a)
```

Two constructors, so every function is two equations. Height, with the empty
tree at zero and counting the `Knoten` constructors on the longest path; the
three traversals, which differ only in where the root is emitted; and the
functor instance.

The functor instance is forced by the type. Applying the function to the
values and leaving the shape alone is the only definition satisfying the
laws, which is why "a sensible instance" is an unambiguous instruction. The
tests check both laws on the instance and that the height is unchanged by
mapping.

The count of leaves is one more than the count of inner nodes, which the
tests check and which is the structural induction from the mathematics
course arriving in a different vocabulary.
