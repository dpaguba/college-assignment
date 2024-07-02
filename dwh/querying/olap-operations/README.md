# OLAP operations

Roll up removes a dimension by summing over it, drill down is the inverse,
slice fixes one dimension and dice restricts several. All four are
aggregations over the same cells, so an OLAP system is a storage question
rather than an algorithm question.

The count that makes it a hard one:

| dimensions | 3 | 5 | 10 | 20 |
|---|---:|---:|---:|---:|
| possible aggregates | 8 | 32 | 1024 | 1 048 576 |

Every subset of the dimensions is an aggregate someone may ask for, and
materialising them all is impossible past a handful of dimensions. The next
two modules are about choosing which ones to keep.

The total is preserved by a roll up, which the module checks. That invariance
is what lets a user drill down and up without the numbers changing under
them, and it is the property a broken aggregation breaks first.
