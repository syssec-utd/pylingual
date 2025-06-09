from math import floor, ceil, log, log2

def calc_round_numbers(prime_bit_len, security_level, t, alpha, security_margin):
    """
    The round numbers are calculated via brute-force by iterating over all reasonable values for full_round
    and partial_round and choosing the pair that satisfies the security inequalities while minimizing
    the number of S-boxes which equal t * full_round + partial_round.

    :param float prime_bit_len: The number of bits of the Poseidon prime field modulus.
        Float is used because it is important for safety checks
    :param int security_level: The security level measured in bits
    :param int t: The size of Poseidon's inner state
    :param int alpha: The power of S-box.
    :param bool security_margin: If `True` increase number of rounds to provide security against all attacks
        known in the literature.
    :return: full_round - number of full rounds, partial_round - number of partial rounds,
        full_round / 2 - half the number of full rounds
    :rtype int, int, int:
    """
    partial_round = 0
    full_round = 0
    min_cost = float('inf')
    max_cost_rf = 0
    for rp_i in range(1, 500):
        for rf_i in range(4, 100, 2):
            if security_check(prime_bit_len, t, rf_i, rp_i, alpha, security_level):
                if security_margin:
                    rf_i += 2
                    rp_i = int(ceil(float(rp_i) * 1.075))
                cost = int(t * rf_i + rp_i)
                if cost < min_cost or (cost == min_cost and rf_i < max_cost_rf):
                    partial_round = ceil(rp_i)
                    full_round = ceil(rf_i)
                    min_cost = cost
                    max_cost_rf = full_round
    return (int(full_round), int(partial_round), int(full_round / 2))

def security_check(prime_bit_len, t, full_round, partial_round, alpha, security_level):
    """
    The round numbers are chosen such that providing security against known attacks:

    - Statistical attack(Eq.2 Section 5.5.1 in the Poseidon paper),
    - Interpolation attack (Eq. 3 and Eq.4 Section 5.5.2 of the Poseidon paper) and
    - Gröbner basis attack (Eq. 5 and Eq.6 from Section 5.5.2 of the Poseidon paper).

    Given the minimum number of rounds necessary to provide security against all attacks known in the literature,
    we should add two more rounds with full S-box layers, and 7.5% more rounds with partial S-box layers.

    :param float prime_bit_len: The number of bits of the Poseidon prime field modulus.
        Float is used because it is important for safety checks
    :param int t: The size of Poseidon's inner state
    :param int full_round: Number of full rounds
    :param int partial_round: Number of partial rounds
    :param int alpha: The power of S-box.
    :param int security_level: The security level measured in bits
    :return: Return `True` if the  full_round, partial_round pair matches the security checks
    :rtype bool:
    """
    c = log2(alpha - 1) if alpha > 0 else 2
    full_round_stat = 6 if security_level <= (floor(prime_bit_len) - c) * (t + 1) else 10
    if alpha > 0:
        full_round_inter = ceil(log(2, alpha) * min(security_level, ceil(prime_bit_len))) + ceil(log(t, alpha)) - partial_round + 1
        full_round_GR_1 = log(2, alpha) * min(security_level / float(3), prime_bit_len / float(2)) - partial_round + 1
        full_round_GR_2 = min(log(2, alpha) * security_level / float(t + 1), log(2, alpha) * prime_bit_len / float(2)) - partial_round + t - 1
        full_round_max = max(ceil(full_round_stat), ceil(full_round_inter), ceil(full_round_GR_1), ceil(full_round_GR_2))
        return full_round >= full_round_max
    elif alpha == -1:
        partial_round_inter = ceil(0.5 * min(security_level, ceil(prime_bit_len))) + ceil(log2(t)) - floor(full_round * log2(t)) + 1
        partial_round_GR_2 = ceil(0.5 * min(ceil(security_level / (t + 1)), ceil(0.5 * prime_bit_len))) + ceil(log2(t)) + t - 1 - floor(full_round * log2(t))
        full_round_max = ceil(full_round_stat)
        partial_round_max = max(ceil(partial_round_inter), ceil(partial_round_GR_2))
        return full_round >= full_round_max and partial_round >= partial_round_max
    else:
        print(f'Invalid value for alpha = {alpha}. Required alpha > 0 or alpha = -1')
        exit(1)