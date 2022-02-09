import java.util.Random;

/**
 * Longest common subsequence of two strings, by dynamic programming.
 *
 * <p>Sheet 7, task 7.1. Two ways to call it:
 * {@code java LongestCommonSubsequence seed n1 n2} generates two random strings
 * of the given lengths, and {@code java LongestCommonSubsequence str1 str2}
 * takes them from the command line. Case is significant here, unlike on the
 * previous sheets.
 */
public class LongestCommonSubsequence {

    public static void main(String[] args) {
        String a;
        String b;

        if (args.length == 3) {
            int seed;
            int firstLength;
            int secondLength;

            try {
                seed = Integer.parseInt(args[0]);
            } catch (NumberFormatException notANumber) {
                System.out.println("FEHLER: Der Seed Parameter muss eine positive Zahl sein.");
                usage();
                return;
            }
            if (seed <= 0) {
                System.out.println("FEHLER: Der Seed Parameter muss eine positive Zahl sein.");
                usage();
                return;
            }

            try {
                firstLength = Integer.parseInt(args[1]);
                secondLength = Integer.parseInt(args[2]);
            } catch (NumberFormatException notANumber) {
                System.out.println("FEHLER: Ein Parameter konnte nicht gelesen werden.");
                usage();
                return;
            }

            if (firstLength < 10 || secondLength < 10) {
                System.out.println("FEHLER: Eine angegebene Laenge ist <10.");
                usage();
                return;
            }

            Random rng = new Random(seed);
            a = randStr(firstLength, rng);
            b = randStr(secondLength, rng);
        } else if (args.length == 2) {
            a = args[0];
            b = args[1];

            if (a.length() < 5 || b.length() < 5) {
                System.out.println("FEHLER: Uebergebene Strings muessen mindestens Laenge 5 haben.");
                usage();
                return;
            }
            if (!a.matches("[a-zA-Z]+") || !b.matches("[a-zA-Z]+")) {
                System.out.println("FEHLER: Uebergebene Strings duerfen nur Buchstaben enthalten.");
                usage();
                return;
            }
        } else {
            System.out.println("FEHLER: Falsche Parameteranzahl uebergeben.");
            usage();
            return;
        }

        System.out.println("A: " + a);
        System.out.println("B: " + b);

        int[][] table = lcsLaenge(a, b);
        String lcs = lcs(table, a);

        assert lcs.length() == table[a.length()][b.length()] : "table and reconstruction disagree";
        assert isSubsequence(lcs, a) && isSubsequence(lcs, b) : "the result is not a common subsequence";

        if (lcs.isEmpty()) {
            System.out.println("Es existiert keine gemeinsame Teilfolge mit mindestens einem Element.");
        } else {
            System.out.println("LCS " + lcs + " mit Laenge " + lcs.length() + " gefunden.");
        }
    }

    /**
     * Fills the length table: C[i][j] is the LCS length of the first i and first j characters.
     *
     * <p>Equal characters extend the diagonal predecessor by one; unequal ones
     * take the better of dropping one character from either side. Theta(n·m)
     * time and space.
     *
     * <p>The table is one row and one column larger than the strings, and that
     * border of zeros is what removes every special case: the empty prefix has
     * an LCS of length zero against anything.
     */
    public static int[][] lcsLaenge(String a, String b) {
        int[][] table = new int[a.length() + 1][b.length() + 1];

        for (int i = 1; i <= a.length(); i++) {
            for (int j = 1; j <= b.length(); j++) {
                if (a.charAt(i - 1) == b.charAt(j - 1)) {
                    table[i][j] = table[i - 1][j - 1] + 1;
                } else {
                    table[i][j] = Math.max(table[i - 1][j], table[i][j - 1]);
                }
            }
        }

        return table;
    }

    /**
     * Reconstructs one longest common subsequence from the table.
     *
     * <p>Walks back from the bottom right corner. A cell that equals the one
     * above it was not produced by a match, so the row can be dropped; likewise
     * for the column. Anything else must have come from the diagonal, and that
     * character belongs to the subsequence.
     *
     * <p>The second string is never needed, which is why the signature only
     * takes the table and A. The table already records where the matches were.
     *
     * <p>The LCS is not unique when there are ties, and the order of the two
     * tests decides which one comes out. The length is the same either way.
     * O(n + m).
     */
    public static String lcs(int[][] table, String a) {
        StringBuilder result = new StringBuilder();

        int i = a.length();
        int j = table[0].length - 1;

        while (i > 0 && j > 0) {
            if (table[i][j] == table[i - 1][j]) {
                i--;
            } else if (table[i][j] == table[i][j - 1]) {
                j--;
            } else {
                result.append(a.charAt(i - 1));
                i--;
                j--;
            }
        }

        return result.reverse().toString();
    }

    /** Random string over the letters, exactly as prescribed by the sheet. */
    private static String randStr(int length, Random r) {
        String alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
        StringBuilder res = new StringBuilder(length);
        while (--length >= 0) {
            res.append(alphabet.charAt(r.nextInt(alphabet.length())));
        }
        return res.toString();
    }

    /** True when candidate can be read off text in order, used only by the assertions. */
    private static boolean isSubsequence(String candidate, String text) {
        int position = 0;
        for (int i = 0; i < text.length() && position < candidate.length(); i++) {
            if (text.charAt(i) == candidate.charAt(position)) {
                position++;
            }
        }
        return position == candidate.length();
    }

    private static void usage() {
        System.out.println("Aufruf des Programms mit:");
        System.out.println("- java LongestCommonSubsequence seed n1 n2");
        System.out.println("- java LongestCommonSubsequence str1 str2");
    }
}
