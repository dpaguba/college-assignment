# Single page applications

The first request brings the document, the bundle and the styles; every later
navigation asks only for data. The module counts the requests: the first load
makes four, a navigation makes one.

## The break-even

With a 322 KB first load and 8 KB per view against 40 KB for a
server-rendered page, the application transfers less than the server-rendered
site only after about **11 pages**. Below that it transfers more; at five
pages, which sounded like plenty, it is still 362 KB against 200.

That is the trade, stated as a number rather than as a preference. A site
whose visitors read one page and leave pays for the bundle and gets nothing
back. An application whose users stay for twenty views gets it back several
times.

The router matches paths against patterns and extracts the parameters:
`/books/:id` against `/books/7` yields the component and `{"id": "7"}`. An
unknown path returns nothing, which is where the not-found view goes.
