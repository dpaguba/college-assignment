# Anonymous classes and lambdas

Chapter fourteen, where a piece of behaviour becomes a value.

```java
Condition even = value -> value % 2 == 0;
Lambdas.countMatching(values, even);
Lambdas.countMatching(values, new Condition() {
    public boolean holds(int value) { return value % 2 == 0; }
});
```

The two arguments are interchangeable, which is the point: the lambda has no
type of its own and takes the type the context expects. That is why the
interface needs exactly one abstract method. With two there would be nothing
to say which one the lambda is, and with none there would be nothing to
implement.

## Capture

A lambda may read locals of the enclosing method, and Java requires them to be
effectively final. The reason is that the lambda can outlive the call that
created it, and a variable that changed afterwards would leave the captured
value meaning nothing. Requiring it not to change makes the captured copy and
the original permanently agree.

## Combinators

Because a condition is a value, conditions can be combined: `and` and `not`
here return new conditions built from old ones, and neither knows anything
about the values it will eventually see. The same idea gives `map` and `fold`,
which are the traversal written once with the interesting part passed in, and
that is the strategy pattern with the ceremony removed.
