# Resource design

An address names a thing; the method says what happens to it. `/books/7` is
a resource, `/getBook?id=7` is a remote procedure call wearing a URL, and
`/books/7/delete` puts the verb back in the path after the method already
carried it.

Collections are plural, hierarchy shows containment, and filtering lives in
the query string:

- `/books` the collection
- `/books/7` one book
- `/authors/3/books` the books of one author
- `/books?author=3&sort=year` a filtered, sorted view

The parent of `/authors/3/books/7` is `/authors/3`, which the module computes
by dropping the last two segments.

`rewrite` turns `/deleteBook?id=7` into DELETE `/books/7`, which is the
mechanical part of the translation. The part that is not mechanical is
deciding what the resources are.

No file extensions: the media type says whether the answer is JSON or XML,
and that is what content negotiation is for.
