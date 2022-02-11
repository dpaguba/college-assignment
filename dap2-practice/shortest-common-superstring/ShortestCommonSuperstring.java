import java.util.ArrayList;
import java.util.Random;

/**
 * A greedy heuristic for the shortest common superstring.
 *
 * <p>Sheet 5, task 5.2. Two ways to call it:
 * {@code java ShortestCommonSuperstring n [seed]} generates n random strings
 * (default seed 6521), and
 * {@code java ShortestCommonSuperstring str1 str2 str3 [...]} takes them from
 * the command line. With at most ten strings the merging steps are printed.
 *
 * <p>Case is irrelevant to the problem, so the input is normalised to upper case
 * before any overlap is computed.
 */
public class ShortestCommonSuperstring {

    private static final int DEFAULT_SEED = 6521;

    public static void main(String[] args) {
        String[] input = readInput(args);
        if (input == null) {
            return;
        }

        ArrayList<String> parts = new ArrayList<>();
        for (String part : input) {
            parts.add(part.toUpperCase());
        }

        boolean verbose = parts.size() <= 10;
        if (verbose) {
            System.out.println(String.join(" ", parts));
        }

        ArrayList<String> originals = new ArrayList<>(parts);
        String superstring = merge(parts, verbose);

        for (String original : originals) {
            assert superstring.contains(original)
                    : "the result is not a superstring of " + original;
        }

        System.out.println("Superstring " + superstring + " mit Laenge " + superstring.length()
                + " gefunden.");
    }

    /**
     * Repeatedly merges the two strings with the largest overlap.
     *
     * <p>Each round is O(k² · L) for k remaining strings of length up to L, and
     * there are k − 1 rounds. The greedy choice is a heuristic, not an optimum:
     * the shortest common superstring problem is NP-hard, and this rule is only
     * known to stay within a constant factor of the best answer.
     *
     * <p>One case the rule ignores entirely: a string that is already contained
     * in another one. It is never removed, so it gets concatenated as if it
     * carried new letters, and the result can be longer than necessary. Feeding
     * it AB and AAB shows it.
     *
     * <p>When no pair overlaps at all, the first two strings are concatenated,
     * which keeps the loop making progress.
     *
     * <p>The largest overlap is updated only on a strictly greater value, so the
     * earliest pair wins a tie and the output stays reproducible. When the pair is
     * removed from the list the larger index goes first, or the second removal
     * would take the wrong element.
     */
    private static String merge(ArrayList<String> parts, boolean verbose) {
        while (parts.size() > 1) {
            int bestFirst = 0;
            int bestSecond = 1;
            int bestOverlap = 0;

            for (int i = 0; i < parts.size(); i++) {
                for (int j = 0; j < parts.size(); j++) {
                    if (i == j) {
                        continue;
                    }
                    int overlap = stringOverlap(parts.get(i), parts.get(j));
                    if (overlap > bestOverlap) {
                        bestOverlap = overlap;
                        bestFirst = i;
                        bestSecond = j;
                    }
                }
            }

            String first = parts.get(bestFirst);
            String second = parts.get(bestSecond);
            String merged = first + second.substring(bestOverlap);

            if (verbose) {
                System.out.println("Ersetze " + first + " und " + second + " durch " + merged);
            }

            parts.remove(Math.max(bestFirst, bestSecond));
            parts.remove(Math.min(bestFirst, bestSecond));
            parts.add(merged);

            assert merged.contains(first) && merged.contains(second)
                    : "the merged string must contain both of its parts";

            if (verbose) {
                System.out.println(String.join(" ", parts));
            }
        }

        return parts.get(0);
    }

    /**
     * How many characters at the end of the first string start the second one.
     *
     * <p>Tries every length up to the shorter string and keeps the largest that
     * matches, which is O(n²) in the string length. Knuth-Morris-Pratt does the
     * same in O(n), and for the string counts on this sheet it makes no
     * difference.
     */
    public static int stringOverlap(String str1, String str2) {
        int m = str1.length();
        int n = str2.length();
        int max = 0;

        for (int i = 1; i <= Math.min(m, n); i++) {
            if (str1.substring(m - i, m).equals(str2.substring(0, i))) {
                max = i;
            }
        }

        return max;
    }

    /** Random string of three to six vowels, exactly as prescribed by the sheet. */
    public static String generateRandomString(Random numberGenerator) {
        String alphabet = "AEIOU";
        StringBuilder builder = new StringBuilder();
        int length = 3 + numberGenerator.nextInt(4);
        while (length-- > 0) {
            int randomIdx = numberGenerator.nextInt(alphabet.length());
            builder.append(alphabet.charAt(randomIdx));
        }
        return builder.toString();
    }

    /** Parses the two argument forms, or prints the error and returns null. */
    private static String[] readInput(String[] args) {
        if (args.length == 0) {
            System.out.println("FEHLER: Es wurde kein Parameter übergeben.");
            usage();
            return null;
        }

        if (args.length <= 2) {
            int count;
            try {
                count = Integer.parseInt(args[0]);
            } catch (NumberFormatException notANumber) {
                System.out.println("FEHLER: Der erste Parameter muss eine natuerliche Zahl >1 sein.");
                usage();
                return null;
            }

            if (count <= 1) {
                System.out.println("FEHLER: Der erste Parameter muss eine natuerliche Zahl >1 sein.");
                usage();
                return null;
            }

            int seed = DEFAULT_SEED;
            if (args.length == 2) {
                try {
                    seed = Integer.parseInt(args[1]);
                } catch (NumberFormatException notANumber) {
                    System.out.println("FEHLER: Der Seed Parameter konnte nicht gelesen werden.");
                    usage();
                    return null;
                }
            }

            Random rng = new Random(seed);
            String[] generated = new String[count];
            for (int i = 0; i < count; i++) {
                generated[i] = generateRandomString(rng);
            }
            return generated;
        }

        for (String argument : args) {
            if (argument.length() < 2) {
                System.out.println("FEHLER: Uebergebene Strings muessen mindestens Laenge 2 haben.");
                usage();
                return null;
            }
        }

        return args;
    }

    private static void usage() {
        System.out.println("Aufruf des Programms mit:");
        System.out.println("- java ShortestCommonSuperstring n [seed]");
        System.out.println("- java ShortestCommonSuperstring str1 str2 str3 [str4 ...]");
    }
}
