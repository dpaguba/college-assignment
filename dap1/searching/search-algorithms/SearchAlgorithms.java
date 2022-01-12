/**
 * Linear and binary search, with the comparisons counted rather than argued.
 *
 * <p>The course introduces both in the first chapter, and the comparison is
 * the first quantitative statement it makes about an algorithm. Counting the
 * comparisons turns that statement into a measurement: on 1024 sorted entries
 * the binary search never exceeds eleven, whatever the target.
 */
public class SearchAlgorithms {

    /** The index of the value, or -1, by scanning from the front. */
    public static int linearSearch(int[] values, int wanted) {
        for (int index = 0; index < values.length; index++) {
            if (values[index] == wanted) {
                return index;
            }
        }
        return -1;
    }

    /** The index of the value in a sorted array, or -1, by halving. */
    public static int binarySearch(int[] values, int wanted) {
        int low = 0;
        int high = values.length - 1;
        while (low <= high) {
            int middle = low + (high - low) / 2;
            if (values[middle] == wanted) {
                return middle;
            }
            if (values[middle] < wanted) {
                low = middle + 1;
            } else {
                high = middle - 1;
            }
        }
        return -1;
    }

    /** The same search written recursively, as the lecture presents it. */
    public static int binarySearchRecursive(int[] values, int wanted) {
        return search(values, wanted, 0, values.length - 1);
    }

    private static int search(int[] values, int wanted, int low, int high) {
        if (low > high) {
            return -1;
        }
        int middle = low + (high - low) / 2;
        if (values[middle] == wanted) {
            return middle;
        }
        if (values[middle] < wanted) {
            return search(values, wanted, middle + 1, high);
        }
        return search(values, wanted, low, middle - 1);
    }

    /** How many comparisons the linear search performs for this target. */
    public static int comparisonsLinear(int[] values, int wanted) {
        int comparisons = 0;
        for (int index = 0; index < values.length; index++) {
            comparisons++;
            if (values[index] == wanted) {
                break;
            }
        }
        return comparisons;
    }

    /** How many comparisons the binary search performs for this target. */
    public static int comparisonsBinary(int[] values, int wanted) {
        int comparisons = 0;
        int low = 0;
        int high = values.length - 1;
        while (low <= high) {
            comparisons++;
            int middle = low + (high - low) / 2;
            if (values[middle] == wanted) {
                break;
            }
            if (values[middle] < wanted) {
                low = middle + 1;
            } else {
                high = middle - 1;
            }
        }
        return comparisons;
    }

    /** The worst case for a given size, which is the count of halvings. */
    public static int worstCaseComparisons(int size) {
        int comparisons = 0;
        int remaining = size;
        while (remaining > 0) {
            comparisons++;
            remaining /= 2;
        }
        return comparisons;
    }
}
