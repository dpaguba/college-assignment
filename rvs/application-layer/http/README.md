# HTTP

The protocol is text and trivially parseable, which is most of why it won. The
performance is not in the parsing but in the connection handling: every new TCP
connection costs a round trip before any data moves.

For ten objects at a 100 ms round trip:

| scheme | time |
|---|---|
| non-persistent | **2000 ms** |
| persistent | 1100 ms |
| persistent and pipelined | **200 ms** |

That table is the history of the protocol's versions in three rows, and it is
entirely about latency: no bandwidth appears in it.

`304 Not Modified` carries no body, so a cache revalidation costs one round trip
and a few bytes rather than the object. Caching is a protocol feature rather
than an optimisation for that reason.

## Idempotence is a protocol promise

`GET`, `PUT` and `DELETE` may be repeated safely; `POST` may not. That is what
lets a proxy retry after a timeout and why a browser warns before resubmitting
a form. It is a contract the method name carries, and a server that mutates
state in a `GET` breaks every intermediary that relies on it.
