# Interfaces and generics

Chapters twelve and thirteen, which answer two halves of the same question:
how does code state what it needs from a type it has never seen?

**Generics** move a cast from run time to compile time. The stack written over
`Object` needed a cast on every read that the compiler could not check; the
stack written over `T` needs none. The one place the cast survives is the
array inside, because Java cannot create an array of a type parameter. Making
an `Object[]` and casting once, in a single method, is the standard answer.

**Bounds** let a method call something on a type parameter. Without
`T extends Comparable<T>` the compiler has no reason to believe a `compareTo`
exists; with it, the method works for every type that implements the
interface, including types written after the method was.

**Interfaces** are the promise itself. A class may implement several, which is
where they differ from a superclass, and a default method lets an interface
gain behaviour without breaking the classes that already implement it.

The cost of generics is erasure: the type argument is gone at run time, so
`new T[]` is impossible, `instanceof List<String>` is not a question Java can
answer, and two methods that differ only in their type argument have the same
signature. Those three limits are all the same limit.
