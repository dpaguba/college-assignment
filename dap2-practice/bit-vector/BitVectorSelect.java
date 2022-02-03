/**
 * Finds the position of the k-th 1-bit.
 *
 * <p>Sheet 9, task 9.1c. Holds nothing but a reference to the rank structure,
 * so it costs constant space, and answers in O(log n) by binary searching over
 * rank.
 *
 * <p>Select is the inverse of rank, and this is the cheap way to get it: rank
 * is monotone, so any monotone query can be inverted by binary search. Real
 * succinct data structures build a separate sampled index and answer select in
 * constant time too; that costs space this task explicitly forbids.
 */
public class BitVectorSelect {

    private final BitVectorRank rank;

    public BitVectorSelect(BitVectorRank rank) {
        this.rank = rank;
    }

    public int size() {
        return rank.size();
    }

    /**
     * The position of the k-th 1-bit, counting from 1, or −1 if there is none.
     *
     * <p>Binary search for the smallest position p with rank(p + 1) = k. The
     * invariant is that the answer, if it exists, lies in [low, high].
     */
    public int select(int k) {
        if (k < 1 || k > rank.rank(size())) {
            return -1;
        }

        int low = 0;
        int high = size() - 1;

        while (low < high) {
            int middle = low + (high - low) / 2;
            if (rank.rank(middle + 1) >= k) {
                high = middle;
            } else {
                low = middle + 1;
            }
        }

        return low;
    }

    /**
     * The position of the k-th 1-bit inside [start, end), or −1.
     *
     * <p>Reduced to the global query: the k-th one inside the window is the
     * (rank(start) + k)-th one overall, and it only counts if it still lands
     * before the end of the window. Two rank calls and one select.
     */
    public int select(int k, int start, int end) {
        if (k < 1 || start < 0 || end > size() || start >= end) {
            return -1;
        }

        int position = select(rank.rank(start) + k);
        return position >= 0 && position < end ? position : -1;
    }
}
