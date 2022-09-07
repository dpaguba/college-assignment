# Status codes

The first digit is the class: 2 success, 3 redirection, 4 the caller's fault,
5 the server's.

## The pairs that get confused

| pair | difference |
|---|---|
| 401 vs 403 | the caller is unknown against known but not allowed |
| 400 vs 409 | the request is malformed against the state conflicts |
| 404 vs 403 | hiding that something exists against admitting it |
| 500 vs 503 | broken against temporarily unavailable |
| 200 vs 204 | there is a body against there is nothing to return |

401 with credentials that are correct is wrong: logging in again will not
help, and the caller is told to try exactly that.

A stale write is 409, not 400. The request was well formed; it lost a race.
That distinction matters to the caller, who can retry a 409 and cannot
usefully retry a 400.

A creation answers 201 with a `Location` header naming the new resource, so
the caller does not have to guess the address it just made.
