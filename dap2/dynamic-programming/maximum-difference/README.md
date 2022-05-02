# Maximum difference

The largest `values[j] − values[i]` where i comes before j.

| | |
|---|---|
| Time | Θ(n) |
| Space | O(1) |
| Shape | linear |

## The idea

The order constraint is the problem. Without it the answer would be max minus
min and there would be nothing to say. With it, `[100, 1, 5]` answers 4, not
99, because the largest value appears before everything it could be subtracted
from.

One pass: remember the smallest value seen so far and, at each position, ask
what the difference would be if this were the later element. Keep the best.

## The answer can be negative, and it should be

On a falling sequence every ordered pair is a loss, and the correct answer is
the least bad one. `[9, 7, 4, 1]` answers −2.

Clamping to zero is the common variant, and it quietly changes the question
from "the best ordered pair" to "the best pair, or no pair at all". Both are
reasonable problems; conflating them is not.

## The same problem as Kadane

Take the consecutive differences `d[i] = values[i+1] − values[i]`. Any ordered
pair telescopes: `values[j] − values[i]` is exactly the sum of `d[i..j−1]`. So
the maximum ordered difference is the maximum subarray sum of the difference
array.

`max_difference_via_kadane()` does it that way, and it is tested against the
single pass and against brute force on 400 random inputs. The single pass is
[kadane](../kadane/) with the subtraction inlined, which is why both are Θ(n)
with one running value.

Two problems that look unrelated in a textbook turn out to be one problem in
different coordinates. That is worth more than either algorithm.

## Related

[kadane](../kadane/) for the linear form and
[maximum-subarray](../../divide-and-conquer/maximum-subarray/) for the
divide and conquer form of the same underlying question.
