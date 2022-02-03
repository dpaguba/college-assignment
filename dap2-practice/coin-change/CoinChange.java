/**
 * Greedy change-making for two currencies.
 *
 * <p>Sheet 5, task 5.1. Usage: {@code java CoinChange Euro|Mira n}, where n is
 * the amount in the smallest unit.
 *
 * <p>Euro has the coins 1, 2, 5, 10, 20, 50, 100, 200. Mira is the invented
 * currency from the sheet and adds 7 and 9, which is exactly what breaks the
 * greedy rule. {@code CoinChangeOptimality} in this folder answers the question
 * the sheet ends with.
 */
public class CoinChange {

    private static final int[] EURO = {200, 100, 50, 20, 10, 5, 2, 1};
    private static final int[] MIRA = {200, 100, 50, 20, 10, 9, 7, 5, 2, 1};

    public static void main(String[] args) {
        if (args.length != 2) {
            System.out.println("FEHLER: Falsche Parameteranzahl!");
            usage();
            return;
        }

        int[] coins;
        if (args[0].equals("Euro")) {
            coins = EURO;
        } else if (args[0].equals("Mira")) {
            coins = MIRA;
        } else {
            System.out.println("FEHLER: Unbekannte Waehrung " + args[0] + "!");
            usage();
            return;
        }

        int amount;
        try {
            amount = Integer.parseInt(args[1]);
        } catch (NumberFormatException notANumber) {
            System.out.println("FEHLER: Falscher Parametertyp fuer das Wechselgeld!");
            usage();
            return;
        }

        if (amount < 0) {
            System.out.println("FEHLER: Wechselgeld darf nicht negativ sein!");
            usage();
            return;
        }

        String unit = args[0].equals("Euro") ? "Eurocent" : "Mira";
        System.out.println("Auszugebendes Wechselgeld: " + amount + " " + unit);

        int[] counts = change(amount, coins);

        int paid = 0;
        for (int i = 0; i < coins.length; i++) {
            if (counts[i] > 0) {
                paid += coins[i] * counts[i];
                System.out.println("(" + coins[i] + "," + counts[i] + "," + (amount - paid) + ")");
            }
        }

        assert paid == amount : "the coins handed out do not add up to the amount";
        System.out.println("Ausgegebenes Wechselgeld: " + paid + " " + unit);
    }

    /**
     * Takes the largest coin that still fits, as often as it fits.
     *
     * <p>Linear in the number of denominations once they are sorted downwards,
     * and it never looks back. That is the appeal and also the problem: whether
     * the result is optimal depends on the coin system, and the algorithm has no
     * way to notice when it is not.
     *
     * <p>The final remainder is always zero because the smallest coin has value
     * 1, which the sheet states as part of the currency definition. Drop that
     * assumption and the loop can end with an amount it cannot pay at all.
     *
     * @return how many of each denomination, in the order the coins were given
     */
    public static int[] change(int b, int[] w) {
        int[] counts = new int[w.length];
        int remainder = b;

        for (int i = 0; i < w.length && remainder > 0; i++) {
            counts[i] = remainder / w[i];
            remainder -= w[i] * counts[i];
        }

        assert remainder == 0 : "a currency without a 1 coin cannot pay every amount";
        return counts;
    }

    private static void usage() {
        System.out.println("Aufruf mit : java CoinChange Euro|Mira n");
        System.out.println("Bsp: java CoinChange Euro 100");
    }
}
