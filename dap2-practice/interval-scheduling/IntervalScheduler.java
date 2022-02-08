import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Interval scheduling: the largest set of intervals that do not overlap.
 *
 * <p>Sheet 6, task 6.1b.
 */
public class IntervalScheduler {

    /**
     * Greedily accepts the interval that finishes earliest among those still compatible.
     *
     * <p>O(n log n), all of it the sort. The input arrives unsorted, which is
     * stated on the sheet and is the only reason the sort is inside this method.
     *
     * <p>Correctness is a "stays ahead" argument. Compare the greedy picks
     * g1, g2, … with those of any optimal solution o1, o2, …, both by finishing
     * time. By induction gi finishes no later than oi: it holds for the first
     * pick because greedy takes the earliest finisher of all, and if it holds
     * for i then gi leaves at least as much room as oi. If the optimum had more
     * intervals, the next one would still be compatible with the greedy prefix,
     * so greedy would have taken it instead of stopping.
     *
     * <p>Finishing early is the right thing to be greedy about. Earliest start
     * fails on [(0,10), (1,2), (3,4)] and shortest duration fails on
     * [(0,5), (4,6), (5,10)]; both accept one interval where two fit.
     *
     * @param intervals the requests, in any order; the list is sorted in place
     * @return a largest set of pairwise disjoint intervals
     */
    public static List<Interval> run(List<Interval> intervals) {
        Collections.sort(intervals);

        List<Interval> accepted = new ArrayList<>();
        int freeFrom = Integer.MIN_VALUE;

        for (Interval interval : intervals) {
            if (interval.getStart() >= freeFrom) {
                accepted.add(interval);
                freeFrom = interval.getEnd();
            }
        }

        return accepted;
    }
}
