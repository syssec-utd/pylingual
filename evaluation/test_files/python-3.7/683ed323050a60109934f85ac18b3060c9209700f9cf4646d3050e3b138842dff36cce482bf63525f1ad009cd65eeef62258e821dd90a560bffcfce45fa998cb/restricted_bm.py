from sklearn.neural_network import BernoulliRBM
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from chembee_config.benchmark.BenchmarkAlgorithm import BenchmarkAlgorithm

class RBMClassifier(BenchmarkAlgorithm):
    name = 'restritce-bm'
    algorithms = (BernoulliRBM(n_components=256, learning_rate=0.0001), BernoulliRBM(n_components=612, learning_rate=0.0001), BernoulliRBM(n_components=256, learning_rate=1e-06), BernoulliRBM(n_components=612, learning_rate=1e-06))
    titles = ('256 units, 0.01 lr', '612 units, 0.01 lr', '256 units, 0.001 lr', '612 units, 0.001 lr')
    _response_method = 'transform'