/**
 * The test program given on sheet 9, used to check the three classes.
 *
 * <p>Its expected output is printed at the end of the sheet, which makes this
 * the one task on the practical that comes with its own oracle.
 */
public class Example {

    private static BitVector bvFromString(String s) {
        BitVector bv = new BitVector(s.length());
        for (int i = 0; i < s.length(); i++) {
            bv.set(i, s.charAt(i) != '0');
        }
        return bv;
    }

    private static String bvToString(BitVector bv) {
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < bv.size(); i++) {
            result.append(bv.get(i) ? '1' : '0');
        }
        return result.toString();
    }

    public static void main(String[] args) {
        String input = "0100110111100010101011";
        BitVector bvDs = bvFromString(input);
        System.out.println("Bitvektor: " + bvToString(bvDs) + "\n");

        BitVectorRank rankDs = new BitVectorRank(bvDs);
        for (int i = 0; i < rankDs.size() + 1; i++) {
            System.out.println("rank(" + i + ") = " + rankDs.rank(i));
        }

        System.out.println("count(2, 9) = " + rankDs.count(2, 9) + "\n");

        BitVectorSelect selectDs = new BitVectorSelect(rankDs);
        for (int k = 0; k <= 12; k++) {
            System.out.println("select(" + k + ") = " + selectDs.select(k));
        }

        System.out.println("select(" + 13 + ") = " + selectDs.select(13)
                + " (BV enthaelt nur 12 1-Bits)" + "\n");

        for (int k = 0; k <= 5; k++) {
            System.out.println("select(" + k + ", 9, 20) = " + selectDs.select(k, 9, 20));
        }

        System.out.println("select(" + 6 + ", 9, 20) = " + selectDs.select(6, 9, 20)
                + " (BV-Intervall enthaelt nur 5 1-Bits)");
    }
}
