# Monad

Bind runs a second computation on the result of the first and lets the
instance decide what to do with the context. The same do-notation then reads
as failure propagation, as a nested loop, or as a state machine.

## What the exam asks

**mapM.** A step applied to every element, failing as a whole if any step
fails. Written with bind, and the exam asks for the translation into
do-notation, which is mechanical: each bind whose result is named becomes a
binding line.

**tryMap.** The same function specialised to `Maybe`, so a list of successes
becomes a success and one failure loses everything.

**A stack machine in the State monad.** `clear` returns the stack and empties
it, `pushN` pushes a list so the head ends up on top, and `popN` takes the
top n values or as many as there are. The state is threaded by bind and never
mentioned, which is the whole point of the monad: the plumbing is in the
instance and not in the program.

```
runState (pushN [1,2,3]) []  =  ((), [1,2,3])
runState (popN 5) [1,2]      =  ([1,2], [])
```

Both reproduced by the module.
