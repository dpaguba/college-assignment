import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Runs {@link IntervalScheduler} on the lecture example and against brute force.
 *
 * <p>Not part of the submission: the sheet asks for the two classes without a
 * main method. This one exists so the result can be checked rather than trusted.
 */
public class IntervalSchedulingDemo {

    public static void main(String[] args) {
        List<Interval> example = new ArrayList<>(List.of(
                new Interval(1, 4), new Interval(3, 5), new Interval(0, 6),
                new Interval(5, 7), new Interval(3, 9), new Interval(5, 9),
                new Interval(6, 10), new Interval(8, 11), new Interval(8, 12),
                new Interval(2, 14), new Interval(12, 16)));

        System.out.println("Auswahl: " + IntervalScheduler.run(example));

        Random rng = new Random(20260830);
        for (int trial = 0; trial < 2000; trial++) {
            List<Interval> intervals = new ArrayList<>();
            int count = rng.nextInt(12);
            for (int i = 0; i < count; i++) {
                int start = rng.nextInt(20);
                intervals.add(new Interval(start, start + 1 + rng.nextInt(8)));
            }
            int greedy = IntervalScheduler.run(new ArrayList<>(intervals)).size();
            int best = bruteForce(intervals);
            if (greedy != best) {
                throw new AssertionError("greedy " + greedy + " vs optimum " + best + " on " + intervals);
            }
        }
        System.out.println("2000 zufaellige Instanzen: greedy trifft jedes Mal das Optimum.");
    }

    /** Every subset, for inputs small enough that 2^n is affordable. */
    private static int bruteForce(List<Interval> intervals) {
        int count = intervals.size();
        int best = 0;

        for (int mask = 0; mask < (1 << count); mask++) {
            List<Interval> chosen = new ArrayList<>();
            for (int i = 0; i < count; i++) {
                if ((mask & (1 << i)) != 0) {
                    chosen.add(intervals.get(i));
                }
            }
            chosen.sort(null);

            boolean disjoint = true;
            for (int i = 1; i < chosen.size(); i++) {
                if (chosen.get(i).getStart() < chosen.get(i - 1).getEnd()) {
                    disjoint = false;
                    break;
                }
            }

            if (disjoint) {
                best = Math.max(best, chosen.size());
            }
        }

        return best;
    }
}
