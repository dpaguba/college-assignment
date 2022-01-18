# Searching

| Topic | |
|---|---|
| [search-algorithms](search-algorithms/) | linear against binary, counted |
| [stack-comparison](stack-comparison/) | the exam papers, sorted and unsorted |

Both modules answer the same question in different words: what does knowing
the data is ordered buy? Eleven comparisons instead of 1024 for one search,
666 instead of 194 389 for one intersection. Neither number is an estimate;
both are counted by the code that does the work.

The second module adds the observation the sheet is really after. Two of its
five questions may stop at the first match, one may not stop at all, and two
are questions about a single pair of extremes that a nested loop answers 250
times more expensively than necessary. Which question is being asked decides
the algorithm before any data structure does.
