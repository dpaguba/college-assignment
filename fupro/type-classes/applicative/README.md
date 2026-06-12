# Applicative

A functor maps a plain function over a container. An applicative can also
apply a function that is itself inside the container, which is what lets a
function of several arguments meet several containers.

```
[(+1), (*2)] <*> [10, 20]  =  [11, 21, 20, 40]
```

Every combination, in that order. For `Maybe` the absence of either side
wins. The two instances are the same interface answering different questions
about context, which is the pattern the monad module then generalises.

The law worth stating is that applying a pure function has to agree with
`fmap`. That is what makes an applicative a functor rather than something
merely similar, and the module checks it for every instance rather than
assuming it.
