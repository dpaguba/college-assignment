/**
 * The sorting algorithms of chapter four and the fourth exercise sheet.
 *
 * <p>Every method has a counting twin, because the interesting property of
 * these algorithms is not that they sort. It is how their work responds to
 * the input: selection sort performs the same comparisons on every input of a
 * given length, insertion sort performs the fewest possible on sorted input,
 * and the improved bubble sort stops after a single pass when nothing moved.
 */
public class ElementarySorts {

    /** Sorting by repeatedly selecting the smallest remaining value. */
    public static int[] selectionSort(int[] values) {
        for (int start = 0; start < values.length - 1; start++) {
            int smallest = start;
            for (int index = start + 1; index < values.length; index++) {
                if (values[index] < values[smallest]) {
                    smallest = index;
                }
            }
            swap(values, start, smallest);
        }
        return values;
    }

    /** Sorting by inserting each value into the sorted prefix. */
    public static int[] insertionSort(int[] values) {
        for (int start = 1; start < values.length; start++) {
            int value = values[start];
            int index = start - 1;
            while (index >= 0 && values[index] > value) {
                values[index + 1] = values[index];
                index--;
            }
            values[index + 1] = value;
        }
        return values;
    }

    /** Sorting by exchanging neighbours until nothing is out of order. */
    public static int[] bubbleSort(int[] values) {
        for (int pass = 0; pass < values.length - 1; pass++) {
            for (int index = 0; index < values.length - 1 - pass; index++) {
                if (values[index] > values[index + 1]) {
                    swap(values, index, index + 1);
                }
            }
        }
        return values;
    }

    /** The same, stopping as soon as a pass exchanges nothing. */
    public static int[] improvedBubbleSort(int[] values) {
        boolean exchanged = true;
        int pass = 0;
        while (exchanged && pass < values.length) {
            exchanged = false;
            for (int index = 0; index < values.length - 1 - pass; index++) {
                if (values[index] > values[index + 1]) {
                    swap(values, index, index + 1);
                    exchanged = true;
                }
            }
            pass++;
        }
        return values;
    }

    /**
     * Insertion sort that finds the insertion point by binary search.
     *
     * <p>Fewer comparisons, the same number of moves. The exercise asks for
     * the improvement and the counting twin shows what it buys: on eight
     * random values the comparisons drop, while the array traffic does not.
     */
    public static int[] binaryInsertionSort(int[] values) {
        for (int start = 1; start < values.length; start++) {
            int value = values[start];
            int low = 0;
            int high = start - 1;
            while (low <= high) {
                int middle = low + (high - low) / 2;
                if (values[middle] <= value) {
                    low = middle + 1;
                } else {
                    high = middle - 1;
                }
            }
            for (int index = start - 1; index >= low; index--) {
                values[index + 1] = values[index];
            }
            values[low] = value;
        }
        return values;
    }

    /**
     * Sorting by counting occurrences, which needs no comparisons at all.
     *
     * <p>The exercise calls it sorting by tallying. It works only because the
     * values are bounded, and that is the trade: the bound buys linear time
     * and costs an array the size of the value range.
     */
    public static int[] countingSort(int[] values, int largest) {
        int[] tally = new int[largest + 1];
        for (int value : values) {
            tally[value]++;
        }
        int position = 0;
        for (int value = 0; value <= largest; value++) {
            for (int repeat = 0; repeat < tally[value]; repeat++) {
                values[position++] = value;
            }
        }
        return values;
    }

    /** How many comparisons selection sort performs. */
    public static int selectionComparisons(int[] values) {
        int comparisons = 0;
        for (int start = 0; start < values.length - 1; start++) {
            int smallest = start;
            for (int index = start + 1; index < values.length; index++) {
                comparisons++;
                if (values[index] < values[smallest]) {
                    smallest = index;
                }
            }
            swap(values, start, smallest);
        }
        return comparisons;
    }

    /** How many comparisons insertion sort performs. */
    public static int insertionComparisons(int[] values) {
        int comparisons = 0;
        for (int start = 1; start < values.length; start++) {
            int value = values[start];
            int index = start - 1;
            while (index >= 0) {
                comparisons++;
                if (values[index] <= value) {
                    break;
                }
                values[index + 1] = values[index];
                index--;
            }
            values[index + 1] = value;
        }
        return comparisons;
    }

    /** How many comparisons the binary variant performs. */
    public static int binaryInsertionComparisons(int[] values) {
        int comparisons = 0;
        for (int start = 1; start < values.length; start++) {
            int value = values[start];
            int low = 0;
            int high = start - 1;
            while (low <= high) {
                comparisons++;
                int middle = low + (high - low) / 2;
                if (values[middle] <= value) {
                    low = middle + 1;
                } else {
                    high = middle - 1;
                }
            }
            for (int index = start - 1; index >= low; index--) {
                values[index + 1] = values[index];
            }
            values[low] = value;
        }
        return comparisons;
    }

    /** How many passes the plain bubble sort makes. */
    public static int bubblePasses(int[] values) {
        int passes = 0;
        for (int pass = 0; pass < values.length - 1; pass++) {
            passes++;
            for (int index = 0; index < values.length - 1 - pass; index++) {
                if (values[index] > values[index + 1]) {
                    swap(values, index, index + 1);
                }
            }
        }
        return passes;
    }

    /** How many passes the improved one makes. */
    public static int improvedBubblePasses(int[] values) {
        boolean exchanged = true;
        int passes = 0;
        while (exchanged && passes < values.length) {
            exchanged = false;
            for (int index = 0; index < values.length - 1 - passes; index++) {
                if (values[index] > values[index + 1]) {
                    swap(values, index, index + 1);
                    exchanged = true;
                }
            }
            passes++;
        }
        return passes;
    }

    private static void swap(int[] values, int first, int second) {
        int held = values[first];
        values[first] = values[second];
        values[second] = held;
    }
}
