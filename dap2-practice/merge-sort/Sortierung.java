/**
 * Merge sort against insertion sort on the same test harness.
 *
 * <p>Sheet 2, task 2.2. Usage:
 * {@code java Sortierung n [insert|merge [auf|ab|rand]]}. The filling methods,
 * the sortedness check and the reporting come from {@link InsertionSort}.
 */
public class Sortierung {

    public static void main(String[] args) {
        if (args.length < 1 || args.length > 3) {
            System.out.println("FEHLER: Es muessen zwischen 1 und 3 Parameter angegeben werden.");
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

        String algorithm = args.length >= 2 ? args[1] : "merge";
        if (!algorithm.equals("insert") && !algorithm.equals("merge")) {
            System.out.println("FEHLER: Unbekanntes Sortierverfahren: " + algorithm);
            usage();
            return;
        }

        String order = args.length == 3 ? args[2] : "rand";
        if (!order.equals("auf") && !order.equals("ab") && !order.equals("rand")) {
            System.out.println("FEHLER: Unbekanntes Vorsortierverfahren: " + order);
            usage();
            return;
        }

        int[] array = InsertionSort.fill(size, order);
        int[] original = array.clone();

        if (algorithm.equals("insert")) {
            InsertionSort.insertionSort(array);
        } else {
            mergeSort(array);
        }

        InsertionSort.report(original, array);
    }

    /**
     * Allocates the scratch array once and hands it to the recursion.
     *
     * <p>Allocating inside the recursion would be correct but would make the
     * algorithm allocate Theta(n log n) memory in total instead of Theta(n).
     */
    public static void mergeSort(int[] array) {
        int[] tmpArray = new int[array.length];
        mergeSort(array, tmpArray, 0, array.length - 1);
        assert InsertionSort.isSorted(array) : "merge sort left the array unsorted";
    }

    /**
     * Divide and conquer: sort both halves, then merge them.
     *
     * <p>T(n) = 2T(n/2) + Theta(n), which is the balanced case of the master
     * theorem and gives Theta(n log n) on every input. Insertion sort's best
     * case beats it on nearly sorted data; its worst case is quadratic and this
     * one is not.
     *
     * <p>The split puts the smaller half on the left, which is how the lecture states
     * the algorithm. It changes nothing asymptotically, but it does change the
     * comparison count on small inputs, and the sheet pins that count down: six
     * descending elements must cost nine.
     */
    private static void mergeSort(int[] array, int[] tmpArray, int left, int right) {
        if (left >= right) {
            return;
        }

        int middle = left + (right - left + 1) / 2 - 1;
        mergeSort(array, tmpArray, left, middle);
        mergeSort(array, tmpArray, middle + 1, right);
        merge(array, tmpArray, left, middle, right);
    }

    /**
     * Merges two sorted neighbouring ranges through the scratch array.
     *
     * <p>Only the head-to-head tests count as comparisons between elements. Once
     * one side is exhausted the rest is copied without comparing, which is why a
     * six element descending input costs nine comparisons and not fifteen.
     */
    private static void merge(int[] array, int[] tmpArray, int left, int middle, int right) {
        System.arraycopy(array, left, tmpArray, left, right - left + 1);

        int i = left;
        int j = middle + 1;
        int target = left;

        while (i <= middle && j <= right) {
            InsertionSort.comparisons++;
            if (tmpArray[i] <= tmpArray[j]) {
                array[target++] = tmpArray[i++];
            } else {
                array[target++] = tmpArray[j++];
            }
        }

        while (i <= middle) {
            array[target++] = tmpArray[i++];
        }
        while (j <= right) {
            array[target++] = tmpArray[j++];
        }
    }

    private static void usage() {
        System.out.println("Aufruf mit: java Sortierung n [insert|merge [auf|ab|rand]]");
        System.out.println("Beispiel: java Sortierung 10000 merge rand");
    }
}
