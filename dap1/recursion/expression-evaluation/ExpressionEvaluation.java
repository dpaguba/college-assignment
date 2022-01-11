/**
 * Completing a sequence of values into an expression that evaluates to zero.
 *
 * <p>The fifth sheet gives the signature with two extra parameters, position
 * and result, and the hint that they carry the state into the recursive
 * calls. That is the shape worth learning: the recursion has no local state
 * of its own, so every call is answerable on its own terms, and adding an
 * output parameter turns the decision procedure into one that also produces
 * the expression it found.
 */
public class ExpressionEvaluation {

    /** Whether some choice of plus and minus makes the values sum to zero. */
    public static boolean addCalcExists(int[] values, int position, int result) {
        if (position == values.length) {
            return result == 0;
        }
        if (position == 0) {
            return addCalcExists(values, 1, values[0]);
        }
        return addCalcExists(values, position + 1, result + values[position])
                || addCalcExists(values, position + 1, result - values[position]);
    }

    /**
     * The expression itself, or the text the sheet prescribes when there is
     * none.
     */
    public static String addCalcExp(int[] values, int position, int result, String expression) {
        if (position == values.length) {
            return result == 0 ? expression : IMPOSSIBLE;
        }
        if (position == 0) {
            return addCalcExp(values, 1, values[0], String.valueOf(values[0]));
        }
        String withPlus = addCalcExp(values, position + 1, result + values[position],
                expression + "+" + values[position]);
        if (!withPlus.equals(IMPOSSIBLE)) {
            return withPlus;
        }
        return addCalcExp(values, position + 1, result - values[position],
                expression + "-" + values[position]);
    }

    /** The value of an expression of additions and subtractions. */
    public static int evaluate(String expression) {
        int total = 0;
        int index = 0;
        int sign = 1;
        while (index < expression.length()) {
            char symbol = expression.charAt(index);
            if (symbol == '+' || symbol == '-') {
                sign = symbol == '+' ? 1 : -1;
                index++;
                continue;
            }
            int start = index;
            while (index < expression.length() && Character.isDigit(expression.charAt(index))) {
                index++;
            }
            total += sign * Integer.parseInt(expression.substring(start, index));
        }
        return total;
    }

    /**
     * The same question answered by trying every sign pattern.
     *
     * <p>An independent oracle for the recursion: the bit pattern of a
     * counter chooses the signs, so nothing about the recursive structure is
     * reused, and the two must agree on every input.
     */
    public static boolean bruteForceExists(int[] values) {
        if (values.length == 0) {
            return true;
        }
        int patterns = 1 << (values.length - 1);
        for (int pattern = 0; pattern < patterns; pattern++) {
            int total = values[0];
            for (int index = 1; index < values.length; index++) {
                boolean minus = (pattern & (1 << (index - 1))) != 0;
                total += minus ? -values[index] : values[index];
            }
            if (total == 0) {
                return true;
            }
        }
        return false;
    }

    private static final String IMPOSSIBLE = "calculation impossible";
}
