import java.util.Scanner;

/**
 * Addition, subtraction and multiplication of binary numbers, digit by digit.
 *
 * <p>The operands are kept as strings of '0' and '1' throughout. Converting
 * them to {@code int} and letting the processor do the work would produce the
 * right answer while skipping the exercise, and it would also cap the operands
 * at 32 bits. Here the only limit is memory.
 *
 * <p>Usage: {@code java BinaryCalculator 1011 + 110}, or run without arguments
 * for the interactive prompt.
 */
public class BinaryCalculator {

    public static void main(String[] args) {
        String left;
        String right;
        String operator;

        if (args.length == 3) {
            left = args[0];
            operator = args[1];
            right = args[2];
        } else if (args.length == 0) {
            Scanner in = new Scanner(System.in);
            System.out.print("First binary number: ");
            left = in.next();
            System.out.print("Operator (+, -, *): ");
            operator = in.next();
            System.out.print("Second binary number: ");
            right = in.next();
        } else {
            System.out.println("Usage: java BinaryCalculator <binary> <+|-|*> <binary>");
            return;
        }

        if (!isBinary(left) || !isBinary(right)) {
            System.out.println("Error: operands must consist of 0 and 1 only.");
            return;
        }

        String result = switch (operator) {
            case "+" -> add(left, right);
            case "-" -> subtract(left, right);
            case "*" -> multiply(left, right);
            default -> null;
        };

        if (result == null) {
            System.out.println("Error: unknown operator " + operator + ". Use +, - or *.");
        } else {
            System.out.println(left + " " + operator + " " + right + " = " + result);
        }
    }

    /**
     * Ripple-carry addition, least significant digit first.
     *
     * <p>Theta(n) digit operations for operands of n digits, which is optimal:
     * flipping any single input digit changes the answer, so every digit has
     * to be read.
     */
    public static String add(String left, String right) {
        StringBuilder result = new StringBuilder();
        int i = left.length() - 1;
        int j = right.length() - 1;
        int carry = 0;

        while (i >= 0 || j >= 0 || carry != 0) {
            int sum = carry;
            if (i >= 0) {
                sum += left.charAt(i--) - '0';
            }
            if (j >= 0) {
                sum += right.charAt(j--) - '0';
            }
            result.append((char) ('0' + (sum & 1)));
            carry = sum >> 1;
        }

        return normalise(result.reverse().toString());
    }

    /**
     * Subtraction by borrowing, with the sign handled by comparing magnitudes.
     *
     * <p>Two's complement would need a fixed width agreed in advance. Comparing
     * first and always subtracting the smaller magnitude from the larger keeps
     * the operands unbounded, at the cost of one extra pass.
     */
    public static String subtract(String left, String right) {
        if (compare(left, right) < 0) {
            return "-" + subtract(right, left);
        }

        StringBuilder result = new StringBuilder();
        int i = left.length() - 1;
        int j = right.length() - 1;
        int borrow = 0;

        while (i >= 0) {
            int difference = (left.charAt(i--) - '0') - borrow - (j >= 0 ? right.charAt(j--) - '0' : 0);
            if (difference < 0) {
                difference += 2;
                borrow = 1;
            } else {
                borrow = 0;
            }
            result.append((char) ('0' + difference));
        }

        return normalise(result.reverse().toString());
    }

    /**
     * Shift and add: for every 1 in the right operand, add the left one shifted.
     *
     * <p>This is the schoolbook method, Theta(n*m). It is the algorithm that
     * Karatsuba improves on by replacing four half-sized products with three.
     */
    public static String multiply(String left, String right) {
        String result = "0";

        for (int j = right.length() - 1, shift = 0; j >= 0; j--, shift++) {
            if (right.charAt(j) == '1') {
                result = add(result, left + "0".repeat(shift));
            }
        }

        return normalise(result);
    }

    /** Magnitude comparison: shorter is smaller once leading zeros are gone. */
    private static int compare(String left, String right) {
        String a = normalise(left);
        String b = normalise(right);
        if (a.length() != b.length()) {
            return a.length() < b.length() ? -1 : 1;
        }
        return a.compareTo(b);
    }

    /** Strip leading zeros, but leave a single zero standing. */
    private static String normalise(String bits) {
        int start = 0;
        while (start < bits.length() - 1 && bits.charAt(start) == '0') {
            start++;
        }
        return bits.substring(start);
    }

    private static boolean isBinary(String candidate) {
        if (candidate.isEmpty()) {
            return false;
        }
        for (int i = 0; i < candidate.length(); i++) {
            if (candidate.charAt(i) != '0' && candidate.charAt(i) != '1') {
                return false;
            }
        }
        return true;
    }
}
