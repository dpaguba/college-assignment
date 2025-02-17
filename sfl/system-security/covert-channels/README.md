# Covert channels

A covert channel carries information over a mechanism that was not meant to
carry any. That is why access control does not see it: the policy guards the
paths that exist for communication, and this is not one of them.

Two kinds. A storage channel writes a value both sides can see, a file name,
a lock, a full disk. A timing channel changes how long something takes and
the other side measures it; nothing is written at all.

The timing channel here transmits bits by working long or briefly and reading
the measurement against a threshold. It is a model, and the mechanism is the
real one.

## Why they are hard to close

Isolating the address spaces removes the storage channel: take away the
shared object and there is nothing to write. It does not remove the timing
channel, because the two processes still share a cache, a bus and a
processor, and the load on those is measurable. `closed_by_isolation` returns
exactly that answer for the two kinds.

Noise lowers the capacity without removing the channel. At an error rate of
0.1 the capacity of a binary channel is 0.53 bits per symbol against 1.0 at
no error, and repetition buys back as much reliability as wanted.

Published bandwidths run from a few bits per second for a disk arm to
hundreds of kilobits per second across processor cores. A few bits per second
is still enough for a key.
