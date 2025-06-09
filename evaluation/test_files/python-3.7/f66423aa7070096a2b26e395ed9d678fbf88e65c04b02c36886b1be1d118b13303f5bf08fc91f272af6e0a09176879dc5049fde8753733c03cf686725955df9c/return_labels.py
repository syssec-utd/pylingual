from __future__ import annotations
import numpy as np
import scipy.stats as st
from sklearn.cluster import OPTICS
from sklearn.cluster import Birch
from collections import defaultdict

def predict_labels(xflatten, n_clusters=1):
    brc = Birch(n_clusters=n_clusters)
    brc.fit(xflatten)
    return brc.predict(xflatten)

def make_table(labels):
    count = defaultdict(int)
    for label in labels:
        count[label] += 1
    table = list(count.values())
    table.sort(reverse=True)
    return table

def chistatistic(prev_table, current_table, threshold=0.05) -> float:
    (chisq_value, _, ddof, _) = st.chi2_contingency([prev_table, current_table])
    delta = sum(prev_table + current_table) * threshold ** 2
    pval = 1 - st.ncx2.cdf(chisq_value, ddof, delta)
    return pval

def return_labels(scores: list[list[float]]) -> list[int]:
    scores_flatten = np.reshape(scores, (len(scores), -1))
    labels = OPTICS(min_samples=0.001).fit_predict(scores_flatten)
    labels[labels == -1] = np.max(labels) + 1
    return labels.tolist()