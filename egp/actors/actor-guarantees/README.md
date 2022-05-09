# What may be relied on

Two senders, two messages each, one receiver. Twenty-four orders are
conceivable. The guarantee that each sender's own order is preserved cuts
that to six and settles nothing: with three actors involved there is still no
order.

That is the practical content of the whole question. A computation that
depends on which of two senders arrives first is wrong, whatever the
implementation happens to do today.

## What is left

- the actor's own state is private, and nobody else can see it;
- a message is handled whole or not at all;
- an order exists only where acknowledgements create one.

Everything beyond that is an assumption about the implementation, and code
built on it breaks when the implementation changes.
