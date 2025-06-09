"""
Tests scikit-learn's PLSRegression.
"""
import unittest
import numpy
from sklearn.cross_decomposition import PLSRegression
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType, Int64TensorType, DoubleTensorType
from test_utils import dump_data_and_model, TARGET_OPSET

class TestSklearnPLSRegressionConverters(unittest.TestCase):

    def test_model_pls_regression(self):
        X = numpy.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [2.0, 2.0, 2.0], [2.0, 5.0, 4.0]], numpy.float32)
        Y = numpy.array([[0.1, -0.2], [0.9, 1.1], [6.2, 5.9], [11.9, 12.3]], numpy.float32)
        pls2 = PLSRegression(n_components=2)
        pls2.fit(X, Y)
        model_onnx = convert_sklearn(pls2, 'scikit-learn pls', [('input', FloatTensorType([None, X.shape[1]]))], target_opset=TARGET_OPSET)
        self.assertTrue(model_onnx is not None)
        dump_data_and_model(X, pls2, model_onnx, methods=['predict'], basename='SklearnPLSRegression')

    def test_model_pls_regression64(self):
        X = numpy.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [2.0, 2.0, 2.0], [2.0, 5.0, 4.0]], numpy.float64)
        Y = numpy.array([[0.1, -0.2], [0.9, 1.1], [6.2, 5.9], [11.9, 12.3]], numpy.float64)
        pls2 = PLSRegression(n_components=2)
        pls2.fit(X, Y)
        model_onnx = convert_sklearn(pls2, 'scikit-learn pls64', [('input', DoubleTensorType([None, X.shape[1]]))], target_opset=TARGET_OPSET)
        self.assertTrue(model_onnx is not None)
        dump_data_and_model(X, pls2, model_onnx, methods=['predict'], basename='SklearnPLSRegression64')

    def test_model_pls_regressionInt64(self):
        X = numpy.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [2.0, 2.0, 2.0], [2.0, 5.0, 4.0]], numpy.int64)
        Y = numpy.array([[0.1, -0.2], [0.9, 1.1], [6.2, 5.9], [11.9, 12.3]], numpy.int64)
        pls2 = PLSRegression(n_components=2)
        pls2.fit(X, Y)
        model_onnx = convert_sklearn(pls2, 'scikit-learn plsint64', [('input', Int64TensorType([None, X.shape[1]]))], target_opset=TARGET_OPSET)
        self.assertTrue(model_onnx is not None)
        dump_data_and_model(X, pls2, model_onnx, methods=['predict'], basename='SklearnPLSRegressionInt64')
if __name__ == '__main__':
    unittest.main()