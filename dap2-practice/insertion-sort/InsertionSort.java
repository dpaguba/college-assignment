import java.util.Random;

/**
 * Insertion sort with a comparison counter and a small test harness.
 *
 * <p>Sheet 2, task 2.1. Usage: {@code java InsertionSort n [auf|ab|rand]}.
 * The seed for the random filling is fixed at 951 so that runs are comparable.
 */
public class InsertionSort {

    /** Comparisons between two array elements, counted across the whole run. */
    public static long comparisons = 0;

    /** Seed prescribed by the task, so that everyone's random arrays match. */
    private static final int SEED = 951;

    public static void main(String[] args) {
        if (args.length < 1 || args.length > 2) {
            System.out.println("FEHLER: Es muessen zwischen 1 und 2 Parameter angegeben werden.");
            usage();
            return;
        }

        int size;
        try {
            size = Integer.parseInt(args[0]);
            if (size < 0) {
                throw new NumberFormatException();
            }
        } catch (NumberFormatException notANaturalNumber) {
            System.out.println("FEHLER: Der erste Parameter muss eine natuerliche Zahl sein.");
            usage();
            return;
        }

        String order = args.length == 2 ? args[1] : "rand";
        if (!order.equals("auf") && !order.equals("ab") && !order.equals("rand")) {
            System.out.println("FEHLER: Unbekanntes Vorsortierverfahren: " + order);
            usage();
            return;
        }

        int[] array = fill(size, order);
        int[] original = array.clone();

        insertionSort(array);

        report(original, array);
    }

    /**
     * Sorts ascending by repeatedly inserting the next element into the sorted prefix.
     *
     * <p>Loop invariant: before iteration i, the range array[0..i-1] holds the
     * first i elements of the input in ascending order. The inner loop shifts
     * everything greater than the key one place right, which opens the gap the
     * key belongs in without ever losing an element.
     *
     * <p>Theta(n²) comparisons on a descending input, Theta(n) on an ascending
     * one, since the inner loop then fails on its first test every time.
     *
     * <p>Only the element-to-element test is counted. Reaching the left end of the
     * array is a bounds check, not a comparison, which is what makes ten descending
     * elements cost 45 and not 54.
     */
    public static void insertionSort(int[] array) {
        for (int i = 1; i < array.length; i++) {
            int key = array[i];
            int j = i - 1;

            while (j >= 0) {
                comparisons++;
                if (key >= array[j]) {
                    break;
                }
                array[j + 1] = array[j];
                j--;
            }

            array[j + 1] = key;
        }

        assert isSorted(array) : "insertion sort left the array unsorted";
    }

    /** True when the array is in ascending order. */
    public static boolean isSorted(int[] array) {
        for (int i = 1; i < array.length; i++) {
            if (array[i - 1] > array[i]) {
                return false;
            }
        }
        return true;
    }

    /**
     * Builds the test array: ascending, descending, or random with the fixed seed.
     */
    public static int[] fill(int size, String order) {
        int[] array = new int[size];

        switch (order) {
            case "auf" -> {
                for (int i = 0; i < size; i++) {
                    array[i] = i + 1;
                }
            }
            case "ab" -> {
                for (int i = 0; i < size; i++) {
                    array[i] = size - i;
                }
            }
            default -> {
                Random rng = new Random(SEED);
                for (int i = 0; i < size; i++) {
                    array[i] = rng.nextInt(1000);
                }
            }
        }

        return array;
    }

    /**
     * Prints both arrays (only for at most 100 elements), the verdict, and the count.
     */
    public static void report(int[] original, int[] sorted) {
        if (sorted.length <= 100) {
            System.out.println(join(original));
            System.out.println(join(sorted));
        }

        System.out.println(isSorted(sorted) ? "Feld ist sortiert!" : "FEHLER: Feld ist NICHT sortiert!");
        System.out.println("Das Sortieren des Arrays hat " + comparisons + " Vergleiche benoetigt.");
    }

    /** Elements separated by single spaces. */
    public static String join(int[] array) {
        StringBuilder line = new StringBuilder();
        for (int value : array) {
            if (line.length() > 0) {
                line.append(' ');
            }
            line.append(value);
        }
        return line.toString();
    }

    private static void usage() {
        System.out.println("Aufruf mit: java InsertionSort n [auf|ab|rand]");
        System.out.println("Beispiel: java InsertionSort 10000 rand");
    }
}
