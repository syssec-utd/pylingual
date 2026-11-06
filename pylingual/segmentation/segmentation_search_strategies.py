from __future__ import annotations
import heapq
import itertools

from typing import TYPE_CHECKING, List, Tuple, Dict, Callable, Generator, Iterable
from pylingual.utils.lazy import lazy_import

if TYPE_CHECKING:
    import numpy as np

    BitMap = List[bool]
    SearchStrategy = Callable[[List[float]], List[BitMap]]
    PriorityFunction = Callable[[List[float]], np.array]
else:
    lazy_import("numpy", "np")

#############
# UTILITIES #
#############


def filter_subwords(results, text):
    """Keep the first token prediction overlapping each encoded instruction."""
    results = iter(results)
    current = next(results, None)
    filtered, start = [], 0
    for instruction in text.split(" <SEP> "):
        end = start + len(instruction)
        while current is not None and current["end"] <= start:
            current = next(results, None)
        if current is None or current["start"] >= end:
            raise ValueError("Segmentation does not cover every instruction")
        filtered.append(current)
        start = end + len(" <SEP> ")
    return filtered


# incrementally generates the index-representation of bitstrings of length length and with num_ones ones
def bitstring_index_generator(length: int, num_ones: int) -> Generator[Tuple[int], None, None]:
    if num_ones > length:
        return

    if num_ones == 0:
        yield tuple()
        return

    # start by having ones in all the smallest positions
    bit_indices = list(range(num_ones))
    yield tuple(bit_indices)
    while bit_indices[0] < length - num_ones:
        # increment the least significant bit and handle cascading effects
        bit_indices[0] += 1
        for i in range(num_ones - 1):
            # when you overlap with the next bit, increase it and set yourself back
            if bit_indices[i] == bit_indices[i + 1]:
                bit_indices[i + 1] += 1
                bit_indices[i] = bit_indices[i - 1] + 1 if i > 0 else 0
        yield tuple(bit_indices)


# convert bitstring indices to numeric representation
def indices_to_num(indices: List[int]) -> int:
    return sum(2 ** int(digit) for digit in indices)


# https://docs.python.org/3/library/itertools.html#itertools.pairwise not introduced until 3.10
# sliding_window('ABCDEFG') --> AB BC CD DE EF FG
def sliding_window(iterable: Iterable, window=2) -> Iterable:
    if window < 1:
        raise ValueError("Window size must be at least 1")

    iterators = [iterable]

    for _ in range(window - 1):
        iterators[-1], next_window_member = itertools.tee(iterators[-1])
        next(next_window_member, None)
        iterators.append(next_window_member)

    return zip(*iterators)


def bitmap_to_entities(bitmap: BitMap) -> List[str]:
    # map of (current, next) pairs in the bitstring to segmentation entities
    entity_map = {
        (True, True): "B",
        (True, False): "B",
        (False, True): "E",
        (False, False): "I",
    }

    entities = [entity_map[pair] for pair in sliding_window(bitmap)]
    entities += "B" if bitmap[-1] else "E"
    return entities


def entities_to_bitmap(entities) -> BitMap:
    return np.array([entity == "B" for entity in entities], dtype=bool)


########################
# STRATEGY DEFINITIONS #
########################


# a general m_deep_top_k implementation that takes the priority function as a parameter
def m_deep_top_k(scores: List[float], m: int, k: int, priority_function: PriorityFunction) -> List[BitMap]:
    # flip_candidate_lists[i] is an iterator over all length l bitstrings with i ones; each list is sorted numerically
    length = len(scores)
    flip_candidate_lists = [bitstring_index_generator(length, num_flips) for num_flips in range(m + 1)]

    # generate a sorted list of the flip candidates (lazily evaluated) and collect the top k elements
    sorted_flip_candidates = heapq.merge(*flip_candidate_lists, key=indices_to_num)
    top_k_candidates = list(itertools.islice(sorted_flip_candidates, k))

    # convert the feature-space indices into problem-space indices
    # the priority map is a list of indices in order of their estimated uncertainty
    priority_map = priority_function(scores)
    flip_sets = [priority_map[list(candidate_flips)] for candidate_flips in top_k_candidates]

    # to match the formalization, build the error strings
    error_strings = []
    for flip_set in flip_sets:
        error_string = np.full(length, False)
        error_string[flip_set] = True
        error_strings.append(list(error_string))

    return error_strings


def get_top_k_predictions(strategy: SearchStrategy, predicted_boundary: List[Dict]) -> List[List[str]]:
    entities = [prediction["entity"] for prediction in predicted_boundary]
    initial_segmentation = entities_to_bitmap(entities)

    scores = [prediction["score"] for prediction in predicted_boundary]
    transformations = strategy(scores)

    candidate_segmentations = [np.logical_xor(initial_segmentation, transformation) for transformation in transformations]

    # convert to entities for compatibility with the pipeline
    top_k_boundaries = [bitmap_to_entities(segmentation) for segmentation in candidate_segmentations]
    return top_k_boundaries


######################
# PRIORITY FUNCTIONS #
######################


# this strategy simply flips predictions in order of least confidence
def naive_confidence_priority(scores: List[float]) -> np.array:
    return np.argsort(scores)
