/**
 * The five methods of the first sheet, reproduced from the published solution.
 *
 * <p>The constraint is the exercise: the body of every method is a single
 * {@code return} using only {@code + - * /}. No comparison, no branch, no
 * remainder operator. What makes it work is that integer division truncates,
 * so {@code dividend / divisor * divisor} is the largest multiple of the
 * divisor that fits, and the difference from the dividend is the remainder.
 */
public class IntegerArithmetic {

    /** The remainder of the division, built from truncation. */
    public static int remainder(int dividend, int divisor) {
        return dividend - dividend / divisor * divisor;
    }

    /** One for an odd value, zero for an even one. */
    public static int isOdd(int value) {
        return remainder(value, 2);
    }

    /** The complement, which needs no second construction. */
    public static int isEven(int value) {
        return 1 - isOdd(value);
    }

    /** The value itself when even, the next value up when odd. */
    public static int toEven(int value) {
        return value + isOdd(value);
    }

    /** Zero when both divisors divide the dividend, non-zero otherwise. */
    public static int isDivisible(int dividend, int divisor1, int divisor2) {
        return remainder(dividend, divisor1) + remainder(dividend, divisor2);
    }

    /**
     * Whether the method bodies in the given source file stay inside the
     * operators the exercise allows.
     *
     * <p>Read from the file rather than asserted in prose, so the constraint
     * is checked along with the results. Anything outside {@code + - * /} and
     * a call to another of these methods counts as a violation.
     */
    public static boolean usesOnlyAllowedOperators(String sourcePath) {
        String source;
        try {
            source = new String(java.nio.file.Files.readAllBytes(
                    java.nio.file.Paths.get(sourcePath)), java.nio.charset.StandardCharsets.UTF_8);
        } catch (java.io.IOException problem) {
            return false;
        }
        for (String body : bodies(source)) {
            for (String forbidden : new String[] {"%", "?", "<", ">", "if", "&&", "||", "=="}) {
                if (body.contains(forbidden)) {
                    return false;
                }
            }
        }
        return true;
    }

    private static java.util.List<String> bodies(String source) {
        java.util.List<String> found = new java.util.ArrayList<>();
        for (String name : new String[] {"remainder(", "isOdd(", "isEven(", "toEven(",
                "isDivisible("}) {
            int declaration = source.indexOf("public static int " + name);
            if (declaration < 0) {
                continue;
            }
            int open = source.indexOf('{', declaration);
            int close = source.indexOf('}', open);
            found.add(source.substring(open + 1, close));
        }
        return found;
    }
}
