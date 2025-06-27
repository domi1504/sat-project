from itertools import product


"""
Module for generating and manipulating covering codes for use in SAT solving strategies.

Covering codes are used in local search algorithms (see Dantsin's algorithm.)
to efficiently explore the search space by guaranteeing that all possible assignments fall within a
bounded Hamming radius of at least one codeword.

References:
    - Schöning, p.99
"""


# todo. bessere cover codes.

# check. does this fulfill property? (p. 100 schoening)
COVER_CODE_N4_R1 = [
    {1: False, 2: False, 3: False, 4: False},
    {1: False, 2: True, 3: True, 4: True},
    {1: True, 2: False, 3: False, 4: False},
    {1: True, 2: True, 3: True, 4: True},
]


def self_concatenate(assignment: list[dict[int, bool]], k: int) -> list[dict[int, bool]]:
    """
    Concatenates the given codewords with themselves k times to create longer codewords.

    Used to extend a base covering code to higher n_high, preserving the structure
    of the original code in blocks of size n.

    Returns A x A x ... x A (k times) of input assignment A.

    :param assignment: List of codewords, each a dict mapping variable indices (1-based) to boolean values.
    :param k: Number of times to concatenate the codewords.
    :return: A new list of extended codewords of length k·n.
    """

    # Assert that all codewords in cover cove have same length
    assert all(len(cw) == len(assignment[0]) for cw in assignment)
    n = len(assignment[0])

    if k < 1:
        raise ValueError("k must be at least 1")
    if k == 1:
        return assignment

    result = []
    # Generate all k-tuples of codewords
    for tuple_of_codewords in product(assignment, repeat=k):
        new_codeword = {}
        for i, codeword in enumerate(tuple_of_codewords):
            # From 1 to n, not 0 to n-1
            for j in range(1, n+1):
                new_codeword[i * n + j] = codeword.get(j, False)
        result.append(new_codeword)
    return result


def adapt_code(extended_code: list[dict[int, bool]], target_n: int, radius: int) -> list[dict[int, bool]]:
    """
    Truncates and adjusts a covering code to match a target dimension, maintaining the covering property.

    This function ensures that the truncated code still covers all vectors within the given radius
    in Hamming space. If coverage is lost during truncation, additional codewords are added greedily.

    :param extended_code: Original code with length greater than target_n.
    :param target_n: Desired length of the final codewords.
    :param radius: Covering radius in Hamming distance.
    :return: List of adjusted codewords of length target_n, preserving the covering radius.
    """
    assert target_n < len(extended_code)

    # Step 1: Truncate codewords
    truncated_code = []
    for codeword in extended_code:
        # Only keep first target_n bits
        new_codeword = {i: codeword[i] for i in range(1, target_n + 1)}
        truncated_code.append(new_codeword)

    # Step 2: Verify covering property
    all_vectors = list(product([False, True], repeat=target_n))
    covered = set()
    for vec in all_vectors:
        for codeword in truncated_code:
            dist = sum(codeword[i] != vec[i - 1] for i in range(1, target_n + 1))
            if dist <= radius:
                covered.add(vec)
                break

    # Step 3: Add codewords if needed
    uncovered = [vec for vec in all_vectors if vec not in covered]
    while uncovered:
        # Greedily cover the most uncovered vectors with a new codeword
        # (Here: just pick the first uncovered vector as new codeword)
        new_codeword = {i + 1: bit for i, bit in enumerate(uncovered[0])}
        truncated_code.append(new_codeword)
        # Update covered set
        for vec in all_vectors:
            dist = sum(new_codeword[i] != vec[i - 1] for i in range(1, target_n + 1))
            if dist <= radius:
                covered.add(vec)
        uncovered = [vec for vec in all_vectors if vec not in covered]
    return truncated_code


def generate_cover_code_greedy(n: int, delta: float) -> list[dict[int, bool]]:
    """
    Perplexity. https://www.perplexity.ai/search/with-the-following-definition-Ss0ILK06RjC7ENvp5THXCQ.
    Constructs a covering code using a greedy algorithm.

    Iteratively selects codewords that cover the most remaining uncovered vectors in Hamming space
    of dimension n. The radius is derived from delta as r = ⌊δ·n⌋.

    :param n: Dimension of the Hamming space (codeword length).
    :param delta: Relative covering radius (e.g., 0.25 for r = n/4).
    :return: A list of covering codewords as dictionaries with 1-based indices.
    """

    # Shift, so that indices start from 1 for each assignment
    # [{1: v, 2: v, ...}, ...] instead of [{0: v, 1: v, ...}, ...]
    def shift_codeword_indices(codewords: list[dict[int, bool]]) -> list[dict[int, bool]]:
        shifted_codewords = []
        for cw in codewords:
            shifted_cw = {index + 1: value for index, value in cw.items()}
            shifted_codewords.append(shifted_cw)
        return shifted_codewords

    # Convert delta to radius (assuming delta is relative distance)
    radius = int(delta * n)

    # Generate all possible binary vectors of length n (H_n)
    all_vectors = []
    for bits in product([0, 1], repeat=n):
        vector_dict = {i: bool(bit) for i, bit in enumerate(bits)}
        all_vectors.append(vector_dict)

    uncovered = set(range(len(all_vectors)))  # Indices of uncovered vectors
    covering_code = []

    def hamming_distance(v1, v2):
        """Calculate Hamming distance between two vectors."""
        return sum(1 for i in range(n) if v1[i] != v2[i])

    def get_ball_coverage(center_idx):
        """Get all vectors within radius of the center vector."""
        center = all_vectors[center_idx]
        covered = []
        for i, vector in enumerate(all_vectors):
            if hamming_distance(center, vector) <= radius:
                covered.append(i)
        return covered

    # Greedy algorithm: at each step, choose ball covering most uncovered elements
    while uncovered:
        best_center = None
        best_coverage = []
        max_new_coverage = 0

        # Try each possible center
        for center_idx in range(len(all_vectors)):
            ball_coverage = get_ball_coverage(center_idx)
            new_coverage = [idx for idx in ball_coverage if idx in uncovered]

            # Choose center that covers the most uncovered elements
            if len(new_coverage) > max_new_coverage:
                max_new_coverage = len(new_coverage)
                best_center = center_idx
                best_coverage = new_coverage

        if best_center is not None:
            # Add the best center to our covering code
            covering_code.append(all_vectors[best_center])

            # Remove covered elements from uncovered set
            for idx in best_coverage:
                uncovered.discard(idx)

    return shift_codeword_indices(covering_code)


def generate_cover_code(n: int, delta: float = 0.25) -> list[dict[int, bool]]:
    """
    Generates a covering code of length n using greedy construction.

    For small n (< 8), a greedy construction is used. For larger n and δ = 0.25, the base
    covering code for n=4 is extended via self-concatenation. If n is not a multiple of 4,
    the extended code is adapted by truncation and adjustment.

    :param n: Desired codeword length.
    :param delta: Relative covering radius (default is 0.25).
    :return: A list of covering codewords, each a dict mapping 1-based indices to boolean values.
    """

    if n < 8:
        return generate_cover_code_greedy(n, delta)
    else:

        if delta != 0.25:
            raise NotImplementedError()

        if n % 4 == 0:
            return self_concatenate(COVER_CODE_N4_R1, n // 4)
        else:
            cover_code_next_4 = self_concatenate(COVER_CODE_N4_R1, (n // 4) + 1)
            return adapt_code(cover_code_next_4, n, n // 4)
