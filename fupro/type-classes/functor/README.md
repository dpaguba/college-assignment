# Functor

One method and two laws that the compiler does not check:

```
fmap id      = id
fmap (f . g) = fmap f . fmap g
```

Any instance satisfying them has to leave the shape alone, which is why the
instance for a type is usually unique and why the exam can ask for "a
sensible instance" without further explanation.

Instances here for lists, `Maybe`, the exam's binary tree, and the function
type. The last one strains the container slogan: mapping over a function is
composing after it, and there is no container anywhere. Both laws hold, which
is the answer to whether it counts.

A deliberately broken instance that reverses the list is included, and it
fails the identity law immediately, which is what the law is for.
