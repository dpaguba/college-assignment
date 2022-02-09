import java.math.BigDecimal;

/**
 * A range of indices together with the product it achieves.
 *
 * <p>Sheet 6, task 6.2a.
 */
public class Range {

    private final int left;
    private final int right;
    private final BigDecimal prod;

    public Range(int left, int right, BigDecimal prod) {
        this.left = left;
        this.right = right;
        this.prod = prod;
    }

    public int getLeft() {
        return left;
    }

    public int getRight() {
        return right;
    }

    public BigDecimal getProd() {
        return prod;
    }

    @Override
    public String toString() {
        return "[" + left + "," + right + "," + prod + "]";
    }
}
