/**
 * The two stacks of exam papers, unsorted and sorted.
 *
 * <p>The exercise asks five questions about two piles of about 500 papers and
 * then asks what changes when the piles are sorted. The published solution
 * gives the answer as a count: n1 times n2 comparisons without sorting, n1
 * plus n2 with it. Both variants are implemented here with their comparisons
 * counted, so the claim can be checked instead of believed.
 */
public class StackComparison {

    /** Whether at least one number occurs in both arrays. */
    public static boolean writtenBoth(int[] first, int[] second) {
        for (int left : first) {
            for (int right : second) {
                if (left == right) {
                    return true;
                }
            }
        }
        return false;
    }

    /** Whether no number occurs in both, which is the negation. */
    public static boolean notWrittenBoth(int[] first, int[] second) {
        return !writtenBoth(first, second);
    }

    /**
     * How many numbers occur in both.
     *
     * <p>This is the question that cannot stop early. The first two can
     * return on the first match; counting has to see every element, which is
     * the distinction the exercise is really about.
     */
    public static int countWrittenBoth(int[] first, int[] second) {
        int count = 0;
        for (int left : first) {
            for (int right : second) {
                if (left == right) {
                    count++;
                    break;
                }
            }
        }
        return count;
    }

    /** Whether every number in the first array exceeds every one in the second. */
    public static boolean biggerThan(int[] first, int[] second) {
        int smallest = Integer.MAX_VALUE;
        for (int left : first) {
            smallest = Math.min(smallest, left);
        }
        int largest = Integer.MIN_VALUE;
        for (int right : second) {
            largest = Math.max(largest, right);
        }
        return first.length > 0 && second.length > 0 && smallest > largest;
    }

    /** Whether at least one number in the first exceeds every one in the second. */
    public static boolean oneBiggerThanAll(int[] first, int[] second) {
        int largest = Integer.MIN_VALUE;
        for (int right : second) {
            largest = Math.max(largest, right);
        }
        for (int left : first) {
            if (left > largest) {
                return true;
            }
        }
        return false;
    }

    /** The same count on sorted arrays, by walking both at once. */
    public static int countWrittenBothSorted(int[] first, int[] second) {
        int count = 0;
        int left = 0;
        int right = 0;
        while (left < first.length && right < second.length) {
            if (first[left] == second[right]) {
                count++;
                left++;
                right++;
            } else if (first[left] < second[right]) {
                left++;
            } else {
                right++;
            }
        }
        return count;
    }

    /** How many comparisons the unsorted count performs. */
    public static int comparisonsUnsorted(int[] first, int[] second) {
        int comparisons = 0;
        for (int left : first) {
            for (int right : second) {
                comparisons++;
                if (left == right) {
                    break;
                }
            }
        }
        return comparisons;
    }

    /** How many the sorted walk performs. */
    public static int comparisonsSorted(int[] first, int[] second) {
        int comparisons = 0;
        int left = 0;
        int right = 0;
        while (left < first.length && right < second.length) {
            comparisons++;
            if (first[left] == second[right]) {
                left++;
                right++;
            } else if (first[left] < second[right]) {
                left++;
            } else {
                right++;
            }
        }
        return comparisons;
    }
}
