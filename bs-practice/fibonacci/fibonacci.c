#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

/**
 * The recursive definition, written as the definition reads.
 *
 * Every call spawns two more, so the number of calls is itself a Fibonacci
 * number and the running time is exponential. That is the point of the
 * exercise: the shortest program is not the fastest one, and the difference is
 * visible by hand at n = 40.
 */
static unsigned long long fib_recursive(unsigned int n)
{
    if (n <= 1) {
        return n;
    }
    return fib_recursive(n - 1) + fib_recursive(n - 2);
}

/**
 * The same function computed by carrying two values forward.
 *
 * Linear time and constant space, because the recursion recomputed the same
 * subproblems and the loop does not.
 */
static unsigned long long fib_iterative(unsigned int n)
{
    unsigned long long previous = 0;
    unsigned long long current = 1;

    if (n == 0) {
        return 0;
    }

    for (unsigned int index = 1; index < n; index++) {
        unsigned long long next = previous + current;
        previous = current;
        current = next;
    }

    return current;
}

/**
 * Read a non-negative number, rejecting anything else.
 *
 * scanf returns the number of items it converted, so a non-numeric input
 * returns zero rather than failing loudly. Checking that return value is the
 * whole of the input validation the assignment asks for.
 */
static int read_number(unsigned int *out)
{
    long value;

    printf("Enter a number: ");
    if (scanf("%ld", &value) != 1) {
        fprintf(stderr, "not a number\n");
        return -1;
    }
    if (value < 0) {
        fprintf(stderr, "the Fibonacci sequence is not defined for %ld\n", value);
        return -1;
    }
    if (value > 90) {
        fprintf(stderr, "%ld would overflow an unsigned long long\n", value);
        return -1;
    }

    *out = (unsigned int)value;
    return 0;
}

int main(void)
{
    unsigned int n;

    if (read_number(&n) != 0) {
        return EXIT_FAILURE;
    }

    printf("fib(%u) = %llu\n", n, fib_iterative(n));

    if (n <= 30) {
        printf("recursively:  %llu\n", fib_recursive(n));
    } else {
        printf("recursively:  skipped, the recursion is exponential\n");
    }

    return EXIT_SUCCESS;
}
