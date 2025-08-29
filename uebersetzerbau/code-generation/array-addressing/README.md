# Array addressing

Memory is one-dimensional, so a multi-dimensional array is flattened, and the
compiler generates the arithmetic that undoes the flattening on every access.

## The published calculation

For `a: array[-5..10, 0..19] of Integer` with 4-byte integers, stored row-wise:

| | |
|---|---|
| extents | 16 x 20 |
| total size | 1280 bytes |
| elements between `a[0,0]` and `a[3,5]` | **65** |
| bytes | 260 |
| address of `a[3,5]` when `a[0,0]` is at 1000 | **1260** |

which is the solution's reasoning exactly: skip rows 0 to 2 entirely, three
rows of twenty, then five more elements in row 3.

## Non-zero lower bounds cost nothing

`array[-5..10]` looks more expensive than `array[0..15]` and is not. The lower
bound is a constant, so the correction folds into the base address at compile
time:

    t0 := i + 5
    t1 := t0 * 20
    t1 := t1 + (j)
    offset := t1 * 4
    address := base + offset

One multiplication and one addition per dimension beyond the first, plus a
final scaling. That is where the run-time cost of an array access is, and it is
why hoisting the row computation out of an inner loop matters so much.

## Row-major and column-major

Row-major varies the **last** index fastest, column-major the first. C chose
one and Fortran the other, and every interoperability layer between the two
exists because of that choice. Both are implemented so the difference is one
argument rather than a rewrite: on a 3x3 array, walking the indices in each
order produces the addresses 0 through 8 in sequence.
