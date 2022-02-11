import java.util.Random;

/**
 * Quicksort with a random pivot, sorting in descending order.
 *
 * <p>Sheet 3, task 3.1. Usage: {@code java QuickSort 5 3 9 1}. The first output
 * line is the sorted array, the second is how often partition was called.
 *
 * <p>The generator is seeded with 1337 and created once, so the pivot sequence
 * and therefore the partition count are reproducible.
 */
public class QuickSort {

    private static final Random rng = new Random(1337);

    /** How often partition was called, which is what the second output line reports. */
    private static int partitionCalls = 0;

    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("FEHLER: Es wurden keine Argumente uebergeben.");
            return;
        }

        int[] array = new int[args.length];
        try {
            for (int i = 0; i < args.length; i++) {
                array[i] = Integer.parseInt(args[i]);
            }
        } catch (NumberFormatException notANumber) {
            System.out.println("FEHLER: Es koennen nur ganze Zahlen sortiert werden.");
            return;
        }

        quickSort(array);

        StringBuilder line = new StringBuilder();
        for (int value : array) {
            if (line.length() > 0) {
                line.append(", ");
            }
            line.append(value);
        }
        System.out.println(line);
        System.out.println(partitionCalls);
    }

    /** Sorts the whole array descending. */
    public static void quickSort(int[] array) {
        quickSort(array, 0, array.length - 1);
        assert isDescending(array) : "quicksort left the array unsorted";
    }

    /**
     * Sorts array[p..r] descending.
     *
     * <p>Partition puts the pivot where it belongs and guarantees everything
     * left of it is at least as large, so the two sides can be sorted
     * independently with no merge step. That is the difference from merge sort:
     * the work is in the split, not in the combine.
     *
     * <p>Expected O(n log n) with a random pivot, Theta(n²) in the worst case,
     * which a fixed pivot makes reachable by sorted input and a random one does
     * not. The left side is recursed into first, which the sheet requires so
     * that the partition counts match.
     */
    private static void quickSort(int[] array, int p, int r) {
        if (p < r) {
            int q = partition(array, p, r);
            quickSort(array, p, q - 1);
            quickSort(array, q + 1, r);
        }
    }

    /**
     * Hoare-style partition around a randomly chosen pivot, for descending order.
     *
     * <p>The pivot is swapped to the end, then i walks right past everything
     * that belongs on the left (values greater than the pivot) and j walks left
     * past everything that belongs on the right. Every swap fixes two
     * misplaced elements at once.
     *
     * <p>The comparisons are the mirror image of the ascending version from the
     * lecture: {@code >} where it had {@code <}, and the pivot ends up with
     * larger values before it instead of after.
     *
     * <p>The first inner walk deliberately has no bounds test: the pivot sits at
     * position r and is not greater than itself, so the walk always stops. Adding
     * the obvious guard breaks the algorithm and the array comes out unsorted.
     *
     * <p>Afterwards i points at the first element that does not belong on the
     * left, so if it is smaller than the pivot, that is exactly where the pivot
     * belongs.
     */
    private static int partition(int[] array, int p, int r) {
        partitionCalls++;

        int z = rng.nextInt((r - p) + 1) + p;
        swap(array, z, r);

        int pivot = array[r];
        int i = p;
        int j = r - 1;

        while (i < j) {
            while (array[i] > pivot) {
                i++;
            }
            while (i < j && array[j] <= pivot) {
                j--;
            }
            if (i < j) {
                swap(array, i, j);
            }
        }

        if (array[i] < array[r]) {
            swap(array, i, r);
        }

        return i;
    }

    private static void swap(int[] array, int first, int second) {
        int temporary = array[first];
        array[first] = array[second];
        array[second] = temporary;
    }

    private static boolean isDescending(int[] array) {
        for (int i = 1; i < array.length; i++) {
            if (array[i - 1] < array[i]) {
                return false;
            }
        }
        return true;
    }
}
