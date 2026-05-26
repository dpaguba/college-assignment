# Algebraic data types

A declaration lists the ways a value can be built and nothing else is
possible. That closure is what makes exhaustive matching a decidable question
and what lets a compiler warn about a missing case.

```haskell
data Maybe a = Nothing | Just a
data Nat     = Z | S Nat
data Bin     = LSB | Zero Bin | One Bin
data Baum a  = Leer | Knoten a (Baum a) (Baum a)
```

The types of the lecture and the exam are declared here, and a value is a
constructor with its arguments, so equality is structural: two values are
equal exactly when they were built the same way, with no equality method to
write.

The recursive types are where the shape of the data becomes the shape of
every function over it. `Nat` has two constructors, so every function over it
is two equations, and the recursion follows the constructor rather than being
designed.
