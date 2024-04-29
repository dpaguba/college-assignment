# Searching algorithms

Ten ways to find something in an array, one folder each, in plain Python with
no dependencies. Every folder holds the implementation and a README explaining
how it works, what it costs, and when it is the right choice.

Sorting had one meaning. Searching has several, and this folder covers only
the first: finding a value, or a rank, inside a sequence. Searching a tree, a
graph, a text or a game tree are different problems with different folders
waiting for them.

## Finding a value

Everything below linear search needs the array sorted first, which is the most
practical answer to why sorting matters at all.

| Algorithm | Average | Worst | Needs | |
|---|---|---|---|---|
| [linear-search](linear-search/) | O(n) | O(n) | nothing | works on streams and lists |
| [sentinel-linear-search](sentinel-linear-search/) | O(n) | O(n) | a writable end slot | half the comparisons, same complexity |
| [binary-search](binary-search/) | O(log n) | O(log n) | sorted | the default |
| [jump-search](jump-search/) | O(√n) | O(√n) | sorted | never moves backwards |
| [exponential-search](exponential-search/) | O(log i) | O(log n) | sorted | unbounded input, targets near the front |
| [interpolation-search](interpolation-search/) | O(log log n) | O(n) | sorted and evenly spread | guesses from the value |
| [fibonacci-search](fibonacci-search/) | O(log n) | O(log n) | sorted | no division |

## Finding a peak

| Algorithm | Average | Worst | Needs | |
|---|---|---|---|---|
| [ternary-search](ternary-search/) | O(log₃ n) | O(log₃ n) | unimodal | optimisation, not lookup |

## Finding a rank

| Algorithm | Average | Worst | Needs | |
|---|---|---|---|---|
| [quickselect](quickselect/) | O(n) | O(n²) | nothing | medians and top-k |
| [median-of-medians](median-of-medians/) | O(n) | O(n) | nothing | the linear guarantee |

## Using them

The seven value searches share one signature: they take a sequence and a
target, and return an index or -1.

```python
from binary_search import binary_search

binary_search([1, 3, 5, 7, 9], 7)                 # 3
binary_search([1, 3, 5, 7, 9], 4)                 # -1
binary_search(people, 30, key=lambda p: p.age)    # by any key
```

The other three answer different questions and have their own shapes:

```python
ternary_search([1, 5, 9, 12, 8, 4])   # 3, the index of the peak
quickselect([5, 3, 8, 1], 0)          # 1, the smallest value
median_of_medians([5, 3, 8, 1], 2)    # 5, the third smallest
```

Nothing here modifies the array it is given.

## Choosing one

Unsorted data and a single lookup: linear search, and it is optimal, not
naive. Sorted data: binary search, unless one of its assumptions is worth
trading. Give up backwards movement and take jump search; know the keys are
evenly spread and take interpolation search; have no array length and take
exponential search; have no divider in the hardware and take Fibonacci search.

If the question is a rank rather than a position, none of them apply: that is
quickselect, and sorting first to index into the result is the mistake it
exists to prevent.

## How this was built

Test first. Each algorithm got a test file before it had an implementation,
run to watch it fail for the right reason, then the code, then the run again.
A shared contract checked every value search against the same 29 arrays, empty
through fifty elements, including duplicates, negatives and targets at both
ends, and asserted that an absent value comes back as -1 rather than as a
guess. The three that answer other questions got contracts of their own: a
peak in every unimodal shape, and the k-th smallest for every k in the array.

The tests were removed once all 30 passed, so what remains is the library and
the explanations.
