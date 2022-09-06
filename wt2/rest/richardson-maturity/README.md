# The Richardson maturity model

| level | what it has |
|---|---|
| 0 | one endpoint, one method, the action is in the body |
| 1 | many resources, still one method |
| 2 | the methods carry the meaning |
| 3 | the answers carry links |

Level 1 buys addressable, cacheable resources. Level 2 buys intermediaries
that understand the request: a cache knows a GET is safe to store, a proxy
knows a PUT can be retried. Level 3 buys the ability to change the addresses
without breaking the caller, because the caller reads them from the answer
rather than building them.

Most interfaces called REST are at level 2. That is a reasonable place to
stop, as long as it is a decision rather than an accident.

The hypermedia example returns a book with links to itself, its author and
its reviews. What it buys is exactly what the caller no longer needs to know.
