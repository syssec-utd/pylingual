import numpy as np
from pytorchrl.envs.generative_chemistry.diversity_filter.base_diversity_filter import BaseDiversityFilter

class NoFilterWithPenalty(BaseDiversityFilter):
    """Penalize repeatedly generated compounds."""

    def __init__(self, minscore=0.4, bucket_size=25, minsimilarity=0.0):
        super().__init__(minscore, bucket_size, minsimilarity)

    def update_score(self, score, smile) -> np.array:
        if smile is not None:
            smile = self._chemistry.convert_to_rdkit_smiles(smile)
            score = 0.5 * score if self._smiles_exists(smile) else score
        if score >= self.minscore:
            self._add_to_memory(smile)
        return score