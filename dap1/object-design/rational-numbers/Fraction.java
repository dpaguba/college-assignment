/**
 * A rational number, the class chapter three builds twice.
 *
 * <p>The lecture writes it first with public fields and then again with the
 * fields hidden, and the second version is the one that can keep a promise:
 * a fraction is normalised when it is made, so every operation may assume it
 * and no caller can break it. Immutability is what makes that assumption
 * safe, so the arithmetic returns new objects instead of changing this one.
 */
public class Fraction implements Comparable<Fraction> {

    private final int numerator;
    private final int denominator;

    /**
     * Builds a fraction in normal form: cancelled down, with the sign in the
     * numerator.
     *
     * @throws IllegalArgumentException if the denominator is zero
     */
    public Fraction(int numerator, int denominator) {
        this((long) numerator, (long) denominator);
    }

    /**
     * Builds a fraction from values that may exceed the int range before
     * cancelling.
     *
     * <p>An intermediate result is often too large while the fraction itself
     * fits, so the arithmetic is done in long and the range is checked after
     * cancelling rather than before. A result that still does not fit is
     * reported instead of silently wrapping around, which is what an int
     * calculation would do.
     *
     * @throws IllegalArgumentException if the denominator is zero
     * @throws ArithmeticException if the cancelled fraction exceeds the int range
     */
    private Fraction(long numerator, long denominator) {
        if (denominator == 0) {
            throw new IllegalArgumentException("denominator zero");
        }
        long sign = denominator < 0 ? -1 : 1;
        long divisor = greatestCommonDivisor(Math.abs(numerator), Math.abs(denominator));
        if (divisor == 0) {
            divisor = 1;
        }
        long cancelledNumerator = sign * numerator / divisor;
        long cancelledDenominator = sign * denominator / divisor;
        if (cancelledNumerator < Integer.MIN_VALUE || cancelledNumerator > Integer.MAX_VALUE
                || cancelledDenominator < Integer.MIN_VALUE
                || cancelledDenominator > Integer.MAX_VALUE) {
            throw new ArithmeticException("fraction outside the int range: "
                    + cancelledNumerator + "/" + cancelledDenominator);
        }
        this.numerator = (int) cancelledNumerator;
        this.denominator = (int) cancelledDenominator;
    }

    /** The numerator in normal form. */
    public int getNumerator() {
        return numerator;
    }

    /** The denominator in normal form, always positive. */
    public int getDenominator() {
        return denominator;
    }

    /** The sum of this fraction and another. */
    public Fraction add(Fraction other) {
        return new Fraction((long) numerator * other.denominator + (long) other.numerator * denominator,
                (long) denominator * other.denominator);
    }

    /** The difference. */
    public Fraction sub(Fraction other) {
        return new Fraction((long) numerator * other.denominator - (long) other.numerator * denominator,
                (long) denominator * other.denominator);
    }

    /** The product. */
    public Fraction mul(Fraction other) {
        return new Fraction((long) numerator * other.numerator, (long) denominator * other.denominator);
    }

    /** The quotient. */
    public Fraction div(Fraction other) {
        if (other.numerator == 0) {
            throw new IllegalArgumentException("division by zero");
        }
        return new Fraction((long) numerator * other.denominator, (long) denominator * other.numerator);
    }

    /** Whether the fraction is below zero. */
    public boolean isNegative() {
        return numerator < 0;
    }

    /** Whether it is above zero. */
    public boolean isPositive() {
        return numerator > 0;
    }

    /**
     * Compares by cross multiplication.
     *
     * <p>Comparing the decimal values would introduce a rounding error the
     * exact representation exists to avoid, so the comparison stays in
     * integers.
     */
    @Override
    public int compareTo(Fraction other) {
        long left = (long) numerator * other.denominator;
        long right = (long) other.numerator * denominator;
        return Long.compare(left, right);
    }

    @Override
    public boolean equals(Object other) {
        if (!(other instanceof Fraction)) {
            return false;
        }
        Fraction that = (Fraction) other;
        return numerator == that.numerator && denominator == that.denominator;
    }

    @Override
    public int hashCode() {
        return 31 * numerator + denominator;
    }

    @Override
    public String toString() {
        return numerator + "/" + denominator;
    }

    private static long greatestCommonDivisor(long first, long second) {
        while (second != 0) {
            long rest = first % second;
            first = second;
            second = rest;
        }
        return first;
    }
}
