# Client and server over TCP

The practical part of the course: a chat-style application where a server
accepts connections and relays between clients, written in Java over
`java.net.Socket`.

```
javac -d out Server/*.java Client/*.java
java -cp out Server.Server
java -cp out Client.Client
```

## What the sockets hide and what they do not

A `Socket` looks like a pair of streams, and most of the protocol stack is
genuinely invisible: the segmentation, the retransmissions, the congestion
window. Three things are not, and each shows up in this code.

**A stream has no message boundaries.** TCP delivers bytes in order and says
nothing about where one message ends, so the application defines that itself,
with a line terminator here. Reading a fixed number of bytes and hoping is the
classic bug, and it works until a message crosses a segment.

**Accepting is not connecting.** `accept` returns a new socket per client while
the listening socket stays open, which is why the server needs a thread or a
select loop per connection and why the port number in the code is the listening
one and not the one the traffic uses.

**Closing is asymmetric.** Each direction closes separately, so a client that
exits without closing leaves the server reading until a timeout, and the server
has to treat an end of stream as a disconnection rather than as an error.

The protocol concepts behind all three are in [rvs](../../rvs/), in
[tcp-connection](../../rvs/transport-layer/tcp-connection/) in particular.
