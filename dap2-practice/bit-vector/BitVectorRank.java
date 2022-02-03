/**
 * Counts the 1-bits before a position, in constant time.
 *
 * <p>Sheet 9, task 9.1b. Built once in O(n), then every query is answered with
 * one array lookup and at most 32 word popcounts.
 *
 * <p>The structure stores one prefix sum per block of 1024 bits, so it costs
 * 32·n/1024 = n/32 bits, inside the ceil(n/25) + 3200 the sheet allows. Storing
 * the answer for every position would be exact and O(1) as well, but it would
 * cost 32n bits: thirty-two times the vector it is supposed to help.
 *
 * <p>Static by design: the sheet allows it, and the samples would all be stale
 * after a single {@code set} on the underlying vector.
 */
public class BitVectorRank {

    /** Bits per sampled block. A power of two, so the division is a shift. */
    private static final int BLOCK = 1024;

    private final BitVector bitVector;
    private final int[] samples;

    public BitVectorRank(BitVector bitVector) {
        this.bitVector = bitVector;

        int blocks = bitVector.size() / BLOCK + 1;
        this.samples = new int[blocks];

        int running = 0;
        int wordsPerBlock = BLOCK / 32;

        for (int block = 0; block < blocks; block++) {
            samples[block] = running;
            int firstWord = block * wordsPerBlock;
            int lastWord = Math.min(firstWord + wordsPerBlock, bitVector.wordCount());
            for (int word = firstWord; word < lastWord; word++) {
                running += Integer.bitCount(bitVector.word(word));
            }
        }
    }

    public int size() {
        return bitVector.size();
    }

    /**
     * How many 1-bits lie in positions 0 to index−1.
     *
     * <p>The bit at the query position is not counted, which makes rank(0) = 0
     * and rank(n) the total, and makes {@link #count} a plain subtraction.
     *
     * <p>Start from the nearest sample, add whole words with
     * {@code Integer.bitCount}, then mask off the tail of the last word. Every
     * step is a fixed number of machine operations, and popcount is a single
     * instruction on any processor from the last fifteen years.
     */
    public int rank(int index) {
        if (index <= 0) {
            return 0;
        }
        if (index > bitVector.size()) {
            index = bitVector.size();
        }

        int block = index / BLOCK;
        int total = samples[block];

        int firstWord = block * (BLOCK / 32);
        int lastFullWord = index >>> 5;

        for (int word = firstWord; word < lastFullWord; word++) {
            total += Integer.bitCount(bitVector.word(word));
        }

        int remainingBits = index & 31;
        if (remainingBits > 0) {
            int mask = (1 << remainingBits) - 1;
            total += Integer.bitCount(bitVector.word(lastFullWord) & mask);
        }

        return total;
    }

    /** How many 1-bits lie in positions start to end−1. */
    public int count(int start, int end) {
        return rank(end) - rank(start);
    }

    BitVector vector() {
        return bitVector;
    }
}
