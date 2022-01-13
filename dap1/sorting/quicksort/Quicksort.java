/**
 * Quicksort, and what the choice of pivot costs.
 *
 * <p>The lecture presents the version that takes the last element as the
 * pivot. That choice is what makes sorted input the worst case, and the
 * counting methods here measure the difference: on sixteen ascending values
 * the last-element pivot needs more than a hundred comparisons and a middle
 * pivot fewer than seventy.
 */
public class Quicksort {

    /** Sorting with the last element of each range as the pivot. */
    public static int[] sort(int[] values) {
        quicksort(values, 0, values.length - 1);
        return values;
    }

    private static void quicksort(int[] values, int low, int high) {
        if (low >= high) {
            return;
        }
        int boundary = partition(values, low, high);
        quicksort(values, low, boundary - 1);
        quicksort(values, boundary + 1, high);
    }

    /**
     * Rearranges the range so that the pivot sits at its final position.
     *
     * <p>Returns that position. Everything before it is at most the pivot and
     * everything after it is at least the pivot, which is the invariant the
     * recursion depends on.
     */
    public static int partition(int[] values, int low, int high) {
        int pivot = values[high];
        int boundary = low - 1;
        for (int index = low; index < high; index++) {
            if (values[index] <= pivot) {
                boundary++;
                swap(values, boundary, index);
            }
        }
        swap(values, boundary + 1, high);
        return boundary + 1;
    }

    /** Sorting with the middle element as the pivot instead. */
    public static int[] sortWithMiddlePivot(int[] values) {
        middlePivotSort(values, 0, values.length - 1);
        return values;
    }

    private static void middlePivotSort(int[] values, int low, int high) {
        if (low >= high) {
            return;
        }
        swap(values, low + (high - low) / 2, high);
        int boundary = partition(values, low, high);
        middlePivotSort(values, low, boundary - 1);
        middlePivotSort(values, boundary + 1, high);
    }

    /** How many comparisons the lecture's version performs. */
    public static int comparisons(int[] values) {
        int[] counter = {0};
        countingSort(values, 0, values.length - 1, counter, false);
        return counter[0];
    }

    /** How many the middle pivot performs on the same input. */
    public static int comparisonsWithMiddlePivot(int[] values) {
        int[] counter = {0};
        countingSort(values, 0, values.length - 1, counter, true);
        return counter[0];
    }

    private static void countingSort(int[] values, int low, int high, int[] counter,
            boolean middlePivot) {
        if (low >= high) {
            return;
        }
        if (middlePivot) {
            swap(values, low + (high - low) / 2, high);
        }
        int pivot = values[high];
        int boundary = low - 1;
        for (int index = low; index < high; index++) {
            counter[0]++;
            if (values[index] <= pivot) {
                boundary++;
                swap(values, boundary, index);
            }
        }
        swap(values, boundary + 1, high);
        countingSort(values, low, boundary, counter, middlePivot);
        countingSort(values, boundary + 2, high, counter, middlePivot);
    }

    private static void swap(int[] values, int first, int second) {
        int held = values[first];
        values[first] = values[second];
        values[second] = held;
    }
}
