# Integer arithmetic

The fourth task of the first sheet, with a published solution: implement five
methods whose bodies contain a single `return` and no operator beyond
`+ - * /`. No comparison, no branch, no remainder operator.

```java
public static int remainder(int dividend, int divisor) {
    return dividend - dividend / divisor * divisor;
}
public static int isOdd(int value)  { return remainder(value, 2); }
public static int isEven(int value) { return 1 - isOdd(value); }
public static int toEven(int value) { return value + isOdd(value); }
public static int isDivisible(int dividend, int divisor1, int divisor2) {
    return remainder(dividend, divisor1) + remainder(dividend, divisor2);
}
```

All five are reproduced exactly and checked against Java's own operators over
every dividend up to 60 and every divisor up to 12.

What makes the exercise worth doing is that each answer is built from the one
before it. Integer division truncates, so `dividend / divisor * divisor` is
the largest multiple of the divisor that fits and the difference is the
remainder. Once that exists, odd is the remainder modulo two, even is its
complement, rounding up to even is adding the oddness, and divisibility by
two numbers is the sum of two remainders being zero. Nothing is derived twice.

The constraint itself is checked rather than asserted: the method reading the
source file scans the five bodies for anything outside the allowed operators,
so the rule of the exercise is verified along with its results.
