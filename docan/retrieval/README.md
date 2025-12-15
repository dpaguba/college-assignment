# Retrieval

| Module | Topic |
|---|---|
| [word-segmentation](word-segmentation/) | binarisation, profiles, and the gap |
| [query-by-example](query-by-example/) | an image as the query |
| [query-by-string](query-by-string/) | a drawn word as the query |
| [patch-retrieval](patch-retrieval/) | the same search without segmentation |
| [retrieval-evaluation](retrieval-evaluation/) | precision, recall, average precision |

The four project topics from the second half of the course, on a page the
module draws because the George Washington dataset is not included. Drawing it
has one advantage: the ground truth is known rather than estimated.

| Task | mAP | chance |
|---|---:|---:|
| query by example | 0.609 | 0.097 |
| query by string | 0.457 | 0.125 |
| segmentation-free, at 50 % overlap | 0.568 | 0.020 |

The evaluation module is last in the table and first in importance: the
average precision from slide 47 is reproduced to the last digit, and the
50 %-overlap threshold turns out to have two readings that disagree on the
same detection.
