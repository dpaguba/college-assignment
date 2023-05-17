# Loading

The tricks the lecture lists, and the single reason behind all of them: a
warehouse load writes millions of rows into a table nobody is reading, so the
machinery protecting concurrent transactions is pure overhead.

| trick | what it removes |
|---|---|
| turn off logging | the write-ahead log |
| pre-sort the data | random access during index maintenance |
| drop and rebuild the indices | per-row index updates |
| truncate before a full reload | the delete |
| disable constraint checking | per-row validation |

Rebuilding an index beats maintaining it once the load exceeds a share of the
table, which the module computes: the maintenance cost is per inserted row
and the rebuild cost is per table row, so the answer depends only on the
ratio and not on the sizes.

The load window is what the whole design is planned around. Six hours nightly
allows all of these; near real time allows none of them.
