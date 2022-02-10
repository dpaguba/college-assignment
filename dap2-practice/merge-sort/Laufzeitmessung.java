/**
 * Task 2.3, optional: measures insertion sort against merge sort.
 *
 * <p>Usage: {@code java Laufzeitmessung [repetitions]}. Every size is run
 * several times and the median is reported, because a single measurement on a
 * JIT-compiled runtime says more about the warm-up than about the algorithm.
 *
 * <p>The sizes grow by a factor of two so that the two shapes separate: a
 * Theta(n log n) algorithm takes slightly more than twice as long when the
 * input doubles, a Theta(n²) one takes four times as long.
 */
public class Laufzeitmessung {

    private static final int[] SIZES = {1000, 2000, 4000, 8000, 16000, 32000, 64000};

    public static void main(String[] args) {
        int repetitions = args.length > 0 ? Integer.parseInt(args[0]) : 5;

        System.out.printf(java.util.Locale.ROOT, "%8s %14s %14s %10s%n", "n", "insert (ms)", "merge (ms)", "ratio");

        for (int size : SIZES) {
            int[] template = InsertionSort.fill(size, "rand");

            double insert = median(time(template, true, repetitions));
            double merge = median(time(template, false, repetitions));

            System.out.printf(java.util.Locale.ROOT, "%8d %14.2f %14.2f %10.1f%n", size, insert, merge,
                    merge > 0 ? insert / merge : Double.NaN);
        }
    }

    /** One timing series for a single algorithm, in milliseconds. */
    private static double[] time(int[] template, boolean useInsertion, int repetitions) {
        double[] measurements = new double[repetitions];

        for (int run = 0; run < repetitions; run++) {
            int[] array = template.clone();
            long start = System.nanoTime();
            if (useInsertion) {
                InsertionSort.insertionSort(array);
            } else {
                Sortierung.mergeSort(array);
            }
            measurements[run] = (System.nanoTime() - start) / 1e6;
        }

        return measurements;
    }

    private static double median(double[] values) {
        double[] copy = values.clone();
        java.util.Arrays.sort(copy);
        return copy[copy.length / 2];
    }
}
