/**
 * Recognisers built from the syntax diagrams of the first exercise sheet.
 *
 * <p>A syntax diagram is a grammar drawn as a railway, and the point of the
 * published solution is that the drawing settles a question the prose left
 * open. The nine rules given in words for arithmetic expressions are hard to
 * check against each other; the two diagrams that replace them are two
 * productions, and they derive every example uniquely.
 */
public class SyntaxDiagrams {

    /**
     * Whether the text is an identifier: a letter or underscore, then any
     * number of letters, digits or underscores.
     */
    public static boolean isIdentifier(String text) {
        if (text == null || text.isEmpty()) {
            return false;
        }
        char first = text.charAt(0);
        if (!Character.isLetter(first) && first != '_') {
            return false;
        }
        for (int index = 1; index < text.length(); index++) {
            char symbol = text.charAt(index);
            if (!Character.isLetterOrDigit(symbol) && symbol != '_') {
                return false;
            }
        }
        return true;
    }

    /**
     * Whether the text is an expression under the published diagram.
     *
     * <p>The diagram is two productions: an atom is a letter or a bracketed
     * expression, and an expression is an atom optionally followed by an
     * operator and another expression. Every one of the nine prose rules
     * follows from these two, including the ones about what may not stand
     * next to what.
     */
    public static boolean isExpression(String text) {
        if (text == null) {
            return false;
        }
        int[] position = {0};
        boolean parsed = expression(text, position);
        return parsed && position[0] == text.length();
    }

    private static boolean expression(String text, int[] position) {
        if (!atom(text, position)) {
            return false;
        }
        if (position[0] < text.length()) {
            char symbol = text.charAt(position[0]);
            if (symbol == '+' || symbol == '*') {
                position[0]++;
                return expression(text, position);
            }
        }
        return true;
    }

    private static boolean atom(String text, int[] position) {
        if (position[0] >= text.length()) {
            return false;
        }
        char symbol = text.charAt(position[0]);
        if (Character.isLetter(symbol)) {
            position[0]++;
            return true;
        }
        if (symbol == '(') {
            position[0]++;
            if (!expression(text, position)) {
                return false;
            }
            if (position[0] >= text.length() || text.charAt(position[0]) != ')') {
                return false;
            }
            position[0]++;
            return true;
        }
        return false;
    }

    /**
     * How many derivations the published diagram admits for the text.
     *
     * <p>Counted by a chart over spans, so the count is the number of parse
     * trees rather than the number of ways one particular parser happens to
     * backtrack.
     */
    public static int derivations(String text) {
        return countPublished(text, 0, text.length());
    }

    private static int countPublished(String text, int from, int to) {
        if (from >= to) {
            return 0;
        }
        int total = 0;
        if (to - from == 1 && Character.isLetter(text.charAt(from))) {
            total++;
        }
        if (text.charAt(from) == '(' && text.charAt(to - 1) == ')'
                && matches(text, from, to - 1)) {
            total += countPublished(text, from + 1, to - 1);
        }
        for (int split = from + 1; split < to - 1; split++) {
            char symbol = text.charAt(split);
            if (symbol != '+' && symbol != '*') {
                continue;
            }
            int left = countAtom(text, from, split);
            if (left == 0) {
                continue;
            }
            total += left * countPublished(text, split + 1, to);
        }
        return total;
    }

    private static int countAtom(String text, int from, int to) {
        if (to - from == 1 && Character.isLetter(text.charAt(from))) {
            return 1;
        }
        if (to - from >= 2 && text.charAt(from) == '(' && text.charAt(to - 1) == ')'
                && matches(text, from, to - 1)) {
            return countPublished(text, from + 1, to - 1);
        }
        return 0;
    }

    private static boolean matches(String text, int open, int close) {
        int depth = 0;
        for (int index = open; index <= close; index++) {
            if (text.charAt(index) == '(') {
                depth++;
            } else if (text.charAt(index) == ')') {
                depth--;
                if (depth == 0) {
                    return index == close;
                }
            }
        }
        return false;
    }

    /**
     * How many derivations the obvious grammar admits, for comparison.
     *
     * <p>Writing the rule as expression, operator, expression is the natural
     * first attempt and it is ambiguous: {@code u+v+w} has two parse trees
     * under it and one under the published diagram.
     */
    public static int naiveDerivations(String text) {
        return countNaive(text, 0, text.length());
    }

    private static int countNaive(String text, int from, int to) {
        if (from >= to) {
            return 0;
        }
        int total = 0;
        if (to - from == 1 && Character.isLetter(text.charAt(from))) {
            total++;
        }
        if (text.charAt(from) == '(' && text.charAt(to - 1) == ')'
                && matches(text, from, to - 1)) {
            total += countNaive(text, from + 1, to - 1);
        }
        for (int split = from + 1; split < to - 1; split++) {
            char symbol = text.charAt(split);
            if (symbol != '+' && symbol != '*') {
                continue;
            }
            total += countNaive(text, from, split) * countNaive(text, split + 1, to);
        }
        return total;
    }
}
