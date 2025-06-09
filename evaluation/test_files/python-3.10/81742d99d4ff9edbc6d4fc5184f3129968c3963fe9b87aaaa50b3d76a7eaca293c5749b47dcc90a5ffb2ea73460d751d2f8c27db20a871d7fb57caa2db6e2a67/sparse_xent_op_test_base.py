"""Tests for SparseSoftmaxCrossEntropyWithLogits op."""
import numpy as np
from tensorflow.python.eager import backprop as backprop_lib
from tensorflow.python.eager import context
from tensorflow.python.framework import config
from tensorflow.python.framework import constant_op
from tensorflow.python.framework import dtypes
from tensorflow.python.framework import errors_impl
from tensorflow.python.framework import ops as ops_lib
from tensorflow.python.framework import test_util
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import gradient_checker_v2
from tensorflow.python.ops import nn_ops
import tensorflow.python.ops.nn_grad
from tensorflow.python.platform import test

class SparseXentOpTestBase(test.TestCase):

    def _opFwdBwd(self, labels, logits):
        """Runs the op-under-test both forwards and backwards"""
        logits = ops_lib.convert_to_tensor(logits)
        with backprop_lib.GradientTape() as tape:
            tape.watch(logits)
            loss = nn_ops.sparse_softmax_cross_entropy_with_logits_v2(labels=labels, logits=logits)
        return (loss, tape.gradient(loss, logits))

    def _npXent(self, labels, logits):
        logits = np.reshape(logits, [-1, logits.shape[-1]])
        labels = np.reshape(labels, [-1])
        batch_dim = 0
        class_dim = 1
        batch_size = logits.shape[batch_dim]
        e = np.exp(logits - np.reshape(np.amax(logits, axis=class_dim), [batch_size, 1]))
        probs = e / np.reshape(np.sum(e, axis=class_dim), [batch_size, 1])
        labels_mat = np.zeros_like(probs).astype(probs.dtype)
        labels_mat[np.arange(batch_size), labels] = 1.0
        gradient = probs - labels_mat
        loss = -np.sum(labels_mat * np.log(probs + 1e-20), axis=1)
        return (loss, gradient)

    def _testXent(self, np_labels, np_logits):
        (np_loss, np_gradient) = self._npXent(labels=np_labels, logits=np_logits)
        (tf_loss, tf_gradient) = self._opFwdBwd(labels=np_labels, logits=np_logits)
        self.assertAllCloseAccordingToType(np_loss, tf_loss)
        self.assertAllCloseAccordingToType(np_gradient, tf_gradient)

    def testSingleClass(self):
        for label_dtype in (np.int32, np.int64):
            (tf_loss, tf_gradient) = self._opFwdBwd(labels=np.array([0, 0, 0]).astype(label_dtype), logits=np.array([[1.0], [-1.0], [0.0]]).astype(np.float32))
            self.assertAllClose([0.0, 0.0, 0.0], tf_loss)
            self.assertAllClose([[0.0], [0.0], [0.0]], tf_gradient)

    @test_util.run_gpu_only()
    def _testInvalidLabelGPU(self, invalid_label_gradient=np.nan):
        labels = [4, 3, 0, -1]
        logits = [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 2.0, 3.0, 4.0], [1.0, 2.0, 3.0, 4.0]]
        (loss, gradient) = self._opFwdBwd(labels=labels, logits=logits)
        self.assertAllClose([np.nan, 1.3862, 3.442, np.nan], loss, rtol=0.001, atol=0.001)
        self.assertAllClose([[invalid_label_gradient] * 4, [0.25, 0.25, 0.25, -0.75], [-0.968, 0.087, 0.237, 0.6439], [invalid_label_gradient] * 4], gradient, rtol=0.001, atol=0.001)

    def testInvalidLabelGPU(self):
        """This method is structured to be easily overridden by a child class."""
        self._testInvalidLabelGPU()

    @test_util.run_in_graph_and_eager_modes(use_gpu=False)
    @test_util.disable_xla('XLA cannot assert inside of a kernel.')
    def _testInvalidLabelCPU(self, expected_regex='Received a label value of'):
        labels = [4, 3, 0, -1]
        logits = [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 2.0, 3.0, 4.0], [1.0, 2.0, 3.0, 4.0]]
        with self.assertRaisesRegex((errors_impl.InvalidArgumentError, errors_impl.UnknownError), expected_regex):
            self.evaluate(nn_ops.sparse_softmax_cross_entropy_with_logits_v2(labels=labels, logits=logits))

    def testInvalidLabelCPU(self):
        """This method is structured to be easily overridden by a child class."""
        self._testInvalidLabelCPU()

    def testNpXent(self):
        labels = [3, 0]
        logits = [[1.0, 1.0, 1.0, 1.0], [1.0, 2.0, 3.0, 4.0]]
        (np_loss, np_gradient) = self._npXent(labels=np.array(labels), logits=np.array(logits))
        self.assertAllClose(np.array([[0.25, 0.25, 0.25, -0.75], [-0.968, 0.087, 0.237, 0.6439]]), np_gradient, rtol=0.001, atol=0.001)
        self.assertAllClose(np.array([1.3862, 3.442]), np_loss, rtol=0.001, atol=0.001)

    def testShapeMismatch(self):
        with self.assertRaisesRegex(ValueError, '`labels.shape.rank` must equal `logits.shape.rank - 1`'):
            nn_ops.sparse_softmax_cross_entropy_with_logits_v2(labels=[[0, 2]], logits=[[0.0, 1.0], [2.0, 3.0], [2.0, 3.0]])

    def testScalar(self):
        with self.assertRaisesRegex(ValueError, '`logits` cannot be a scalar'):
            nn_ops.sparse_softmax_cross_entropy_with_logits_v2(labels=constant_op.constant(0), logits=constant_op.constant(1.0))

    def _testLabelsPlaceholderScalar(self, expected_error_message):
        with ops_lib.Graph().as_default(), self.session():
            labels = array_ops.placeholder(np.int32)
            y = nn_ops.sparse_softmax_cross_entropy_with_logits_v2(labels=labels, logits=[[7.0]])
            with self.assertRaisesOpError(expected_error_message):
                y.eval(feed_dict={labels: 0})

    def testLabelsPlaceholderScalar(self):
        """This method is structured to be easily overridden by a child class."""
        self._testLabelsPlaceholderScalar(expected_error_message='labels must be 1-D')

    def testVector(self):
        loss = nn_ops.sparse_softmax_cross_entropy_with_logits_v2(labels=constant_op.constant(0), logits=constant_op.constant([1.0]))
        self.assertAllClose(0.0, loss)

    def testFloat(self):
        for label_dtype in (np.int32, np.int64):
            self._testXent(np_labels=np.array([3, 0]).astype(label_dtype), np_logits=np.array([[1.0, 1.0, 1.0, 1.0], [1.0, 2.0, 3.0, 4.0]]).astype(np.float32))

    def testDouble(self):
        for label_dtype in (np.int32, np.int64):
            self._testXent(np_labels=np.array([0, 3]).astype(label_dtype), np_logits=np.array([[1.0, 1.0, 1.0, 1.0], [1.0, 2.0, 3.0, 4.0]]).astype(np.float64))

    def testHalf(self):
        for label_dtype in (np.int32, np.int64):
            self._testXent(np_labels=np.array([3, 0]).astype(label_dtype), np_logits=np.array([[1.0, 1.0, 1.0, 1.0], [1.0, 2.0, 3.0, 4.0]]).astype(np.float16))

    def testEmpty(self):
        self._testXent(np_labels=np.zeros((0,), dtype=np.int32), np_logits=np.zeros((0, 3)))

    @test_util.run_in_graph_and_eager_modes()
    def testGradient(self):
        with self.session() as sess:
            labels = constant_op.constant([3, 0, 1], name='labels')
            logits = constant_op.constant([0.1, 0.2, 0.3, 0.4, 0.1, 0.4, 0.9, 1.6, 0.1, 0.8, 2.7, 6.4], shape=[3, 4], dtype=dtypes.float64, name='logits')

            def xent(logits):
                return nn_ops.sparse_softmax_cross_entropy_with_logits_v2(labels=labels, logits=logits, name='xent')
            (analytical, numerical) = gradient_checker_v2.compute_gradient(xent, [logits])
            if not context.executing_eagerly():
                op_names = [op.op_def.name for op in sess.graph.get_operations() if op.op_def]
                self.assertNotIn('BatchMatMul', op_names)
                self.assertNotIn('BatchMatMulV2', op_names)
        tol = 5e-08
        self.assertAllClose(analytical, numerical, atol=tol, rtol=tol)

    @test_util.run_in_graph_and_eager_modes()
    def testSecondGradient(self):
        with self.session() as sess:
            labels = constant_op.constant([3, 0, 1], name='labels')
            logits = constant_op.constant([0.3, 0.4, 0.1, 1.2, 0.1, 1.9, 0.1, 0.7, 0.8, 0.2, 1.3, 1.3], shape=[3, 4], dtype=dtypes.float64, name='logits')

            def xent_grad(logits):
                with backprop_lib.GradientTape() as tape:
                    tape.watch(logits)
                    return tape.gradient(nn_ops.sparse_softmax_cross_entropy_with_logits_v2(labels=labels, logits=logits, name='xent'), [logits])[0]
            (analytical, numerical) = gradient_checker_v2.compute_gradient(xent_grad, [logits])
            if not context.executing_eagerly() and (not config.is_op_determinism_enabled()):
                op_names = [op.op_def.name for op in sess.graph.get_operations() if op.op_def]
                self.assertIn('BatchMatMulV2', op_names)
        tol = 5e-08
        self.assertAllClose(analytical, numerical, atol=tol, rtol=tol)

    @test_util.run_in_graph_and_eager_modes()
    def _testHighDim(self, labels, logits):
        (np_loss, np_gradient) = self._npXent(labels=np.array(labels), logits=np.array(logits))
        np_loss = np.reshape(np_loss, np.array(labels).shape)
        tf_loss = nn_ops.sparse_softmax_cross_entropy_with_logits_v2(labels=labels, logits=logits)
        with backprop_lib.GradientTape() as tape:
            logits = constant_op.constant(logits)
            tape.watch(logits)
            tf_gradient = tape.gradient(nn_ops.sparse_softmax_cross_entropy_with_logits_v2(labels=labels, logits=logits), [logits])[0]
            tf_gradient = array_ops.reshape(tf_gradient, np_gradient.shape)
        self.assertAllCloseAccordingToType(np_loss, tf_loss)
        self.assertAllCloseAccordingToType(np_gradient, tf_gradient)

    def testHighDim(self):
        labels = [[3], [0]]
        logits = [[[1.0, 1.0, 1.0, 1.0]], [[1.0, 2.0, 3.0, 4.0]]]
        self._testHighDim(labels, logits)

    def testHighDim2(self):
        labels = [[3, 2], [0, 3]]
        logits = [[[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]], [[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0]]]
        self._testHighDim(labels, logits)

    def _testScalarHandling(self, expected_regex):
        with ops_lib.Graph().as_default(), self.session(use_gpu=False) as sess:
            with self.assertRaisesRegex(errors_impl.InvalidArgumentError, expected_regex):
                labels = array_ops.placeholder(dtypes.int32, shape=[None, 1])
                logits = array_ops.placeholder(dtypes.float32, shape=[None, 3])
                ce = nn_ops.sparse_softmax_cross_entropy_with_logits_v2(labels=array_ops.squeeze(labels), logits=logits)
                labels_v2 = np.zeros((1, 1), dtype=np.int32)
                logits_v2 = np.random.randn(1, 3)
                sess.run([ce], feed_dict={labels: labels_v2, logits: logits_v2})

    def testScalarHandling(self):
        """This method is structured to be easily overridden by a child class."""
        self._testScalarHandling(expected_regex='.*labels must be 1-D.*')