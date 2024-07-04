# Star joins

Three plans for the same query, on a fact table of a million rows filtered to
one percent by product and ten percent by time.

| plan | fact rows touched |
|---|---:|
| join each dimension in turn | 1 000 000 |
| filter the dimensions first | 1 000 000 read, 1 000 kept |
| intersect the bitmaps first | 1 000 |

The bitmap plan reads a thousandth of the table, which is the point of the
whole indexing block: the filters are on the dimensions and the rows are in
the fact table, so the useful plan carries the filters to the rows rather
than the rows to the filters.

The join order matters even when the plan does not change. Joining the most
selective dimension first produces 15 000 intermediate rows and the other
order produces 505 000, for the same result.
