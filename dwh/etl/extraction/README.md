# Extraction

Full or incremental, and the incremental version needs the source to say what
changed.

| method | inserts | updates | deletes |
|---|---|---|---|
| timestamp column | yes | yes | **no** |
| trigger | yes | yes | yes |
| log reading | yes | yes | yes |
| full comparison | yes | yes | yes |

The gap in the first row is the one that causes trouble, and it is
structural: a deleted row has no timestamp to read, so a method that reads
timestamps cannot see it. The warehouse then keeps a customer who no longer
exists, and no error is reported anywhere.

The alternatives each cost something. A trigger slows the source, log reading
depends on a format the vendor does not promise, and a full comparison reads
the whole table.
