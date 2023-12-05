# Patterns and dimensions

| Topic | |
|---|---|
| [fp-growth](fp-growth/) | two passes instead of one per level |
| [closed-and-maximal](closed-and-maximal/) | keeping fewer itemsets |
| [curse-of-dimensionality](curse-of-dimensionality/) | when distance stops working |
| [principal-components](principal-components/) | the directions that matter |
| [subspace-clustering](subspace-clustering/) | clusters in some dimensions only |

Chapters seven and eight. The twelfth sheet's answers come out exactly: 13
frequent itemsets, 10 closed and the two maximal ones {ACE} and {DEF}.

The second half is the reason the first half needs help. At 200 dimensions
the spread of the distances is a twelfth of what it is at two, so nearest
neighbours stop meaning anything, and the answers are to reduce the
dimensions or to look inside subspaces. Both are searches, and both reuse the
anti-monotone pruning from the pattern mining half.
