import inspect
from itertools import product
import os
import sys
import unittest
import logging
import pathlib
import platform
import shutil
import numpy as np
from typing import Callable, List
try:
    import cuda
except:
    CUDA_AVAILABLE = False
else:
    CUDA_AVAILABLE = True
if sys.platform == 'linux':
    try:
        LIBHIB_LIBNAME = 'libamdhip64.so'
        import ctypes
        ROCM_AVAILABLE = bool(ctypes.cdll.LoadLibrary(LIBHIB_LIBNAME))
    except:
        ROCM_AVAILABLE = False
else:
    ROCM_AVAILABLE = False
print(f'ROCM_AVAILABLE: {ROCM_AVAILABLE}')
print(f'CUDA_AVAILABLE: {CUDA_AVAILABLE}')
DEV_MODE = False
if '@CMAKE_INSTALL_PREFIX@'[1:-1] != 'CMAKE_INSTALL_PREFIX':
    sys.path.insert(1, '@CMAKE_INSTALL_PREFIX@')
else:
    DEV_MODE = True
    sys.path.insert(1, os.getcwd())
INTERNAL_FUNCTION_OPTS = {'no_inline_into': True, 'public': False}
from accera import Package, ScalarType, Nest, Array, Constants, Scalar, fuse, create_parameters, cast, Target, Role
from accera._lang_python._lang import _MemorySpace, _MMAShape, Dimension
from accera import min as accmin
from accera.samples import MatrixMultiplication
from accera.test import verifiers
from accera.test.test_utils import expectedFailure, FailedReason
from accera.Targets import KNOWN_DEVICES
TEST_PACKAGE_DIR = 'test_acccgen'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class SmokeTest(unittest.TestCase):
    PACKAGE_FORMAT = Package.Format.MLIR_DYNAMIC if DEV_MODE else Package.Format.HAT_DYNAMIC
    PACKAGE_MODE = Package.Mode.RELEASE

    def test_full_fusion_trivial(self) -> None:
        A = Array(role=Role.INPUT, shape=(16, 16))
        B = Array(role=Role.INPUT, shape=(16, 16))
        C = Array(role=Role.INPUT_OUTPUT, shape=(16, 16))
        nest0 = Nest(shape=(16, 16))
        i0, j0 = nest0.get_indices()

        @nest0.iteration_logic
        def _():
            C[i0, j0] += A[i0, j0]
        schedule0 = nest0.create_schedule()
        nest1 = Nest(shape=(16, 16))
        i1, j1 = nest1.get_indices()

        @nest1.iteration_logic
        def _():
            C[i1, j1] *= B[i1, j1]
        schedule1 = nest1.create_schedule()
        schedule = fuse(schedule0, schedule1)
        plan = schedule.create_plan()
        package_name = 'test_full_fusion_trivial'
        package = Package()
        package.add(plan, args=(A, B, C), base_name='test_full_fusion_trivial')
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def test_full_fusion_reordered(self) -> None:
        A = Array(role=Role.INPUT, shape=(16, 16))
        B = Array(role=Role.INPUT, shape=(16, 16))
        C = Array(role=Role.INPUT_OUTPUT, shape=(16, 16))
        nest0 = Nest(shape=(16, 16))
        i0, j0 = nest0.get_indices()

        @nest0.iteration_logic
        def _():
            C[i0, j0] += A[i0, j0]
        schedule0 = nest0.create_schedule()
        nest1 = Nest(shape=(16, 16))
        i1, j1 = nest1.get_indices()

        @nest1.iteration_logic
        def _():
            C[i1, j1] *= B[i1, j1]
        schedule1 = nest1.create_schedule()
        schedule = fuse(schedule0, schedule1)
        plan = schedule.create_plan()
        package_name = 'test_full_fusion_reordered'
        package = Package()
        package.add(plan, args=(A, B, C), base_name='test_full_fusion_reordered')
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def test_partial_fusion_trivial(self) -> None:
        A = Array(role=Role.INPUT, shape=(16, 11))
        B = Array(role=Role.INPUT, shape=(11, 10))
        C = Array(role=Role.INPUT_OUTPUT, shape=(16, 10))
        nest0 = Nest(shape=(16, 10, 11))
        i0, j0, k0 = nest0.get_indices()

        @nest0.iteration_logic
        def _():
            C[i0, j0] += A[i0, k0] * B[k0, j0]
        schedule0 = nest0.create_schedule()
        nest1 = Nest(shape=(16, 10))
        i1, j1 = nest1.get_indices()

        @nest1.iteration_logic
        def _():
            C[i1, j1] = C[i1, j1] * Scalar(0.2)
        schedule1 = nest1.create_schedule()
        schedule = fuse((schedule0, schedule1), partial=2)
        plan = schedule.create_plan()
        package_name = 'test_partial_fusion_trivial'
        package = Package()
        package.add(plan, args=(A, B, C), base_name='test_partial_fusion_trivial')
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def test_partial_fusion_reordered(self) -> None:
        A = Array(role=Role.INPUT, shape=(16, 11))
        B = Array(role=Role.INPUT, shape=(11, 10))
        C = Array(role=Role.INPUT_OUTPUT, shape=(16, 10))
        nest0 = Nest(shape=(16, 10, 11))
        i0, j0, k0 = nest0.get_indices()

        @nest0.iteration_logic
        def _():
            C[i0, j0] += A[i0, k0] * B[k0, j0]
        schedule0 = nest0.create_schedule()
        nest1 = Nest(shape=(16, 10))
        i1, j1 = nest1.get_indices()

        @nest1.iteration_logic
        def _():
            C[i1, j1] = C[i1, j1] * Scalar(0.2)
        schedule1 = nest1.create_schedule()
        schedule = fuse((schedule0, schedule1), partial=2)
        plan = schedule.create_plan()
        package_name = 'test_partial_fusion_reordered'
        package = Package()
        package.add(plan, args=(A, B, C), base_name='test_partial_fusion_reordered')
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def test_differently_split_fused_schedules(self) -> None:
        M = 256
        N = 128
        K = 512
        A = Array(role=Role.INPUT, shape=(M, K))
        B = Array(role=Role.INPUT, shape=(K, N))
        C = Array(role=Role.INPUT_OUTPUT, shape=(M, N))
        nest0 = Nest(shape=(M, N, K))
        i0, j0, k0 = nest0.get_indices()

        @nest0.iteration_logic
        def _():
            C[i0, j0] += A[i0, k0] * B[k0, j0]
        schedule0 = nest0.create_schedule()
        ii0 = schedule0.split(i0, 16)
        iii0 = schedule0.split(ii0, 8)
        schedule0.reorder(i0, j0, ii0, k0, iii0)
        nest1 = Nest(shape=(M, N))
        i1, j1 = nest1.get_indices()

        @nest1.iteration_logic
        def _():
            C[i1, j1] = C[i1, j1] * Scalar(0.2)
        schedule1 = nest1.create_schedule()
        ii1 = schedule1.split(i1, 16)
        schedule1.reorder(i1, j1, ii1)
        schedule = fuse((schedule0, schedule1), partial=2)
        plan = schedule.create_plan()
        package_name = 'test_differently_split_fused_schedules'
        package = Package()
        package.add(plan, args=(A, B, C), base_name='test_differently_split_fused_schedules')
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def test_partial_fusion_matmul3_naive(self) -> None:
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(16, 11))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(11, 10))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(16, 10))
        D = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(10, 7))
        E = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(16, 7))
        nest0 = Nest(shape=(16, 10, 11))
        i0, j0, k0 = nest0.get_indices()

        @nest0.iteration_logic
        def _():
            C[i0, j0] += A[i0, k0] * B[k0, j0]
        schedule0 = nest0.create_schedule()
        nest1 = Nest(shape=(16, 7, 10))
        i1, j1, k1 = nest1.get_indices()

        @nest1.iteration_logic
        def _():
            E[i1, j1] += C[i1, k1] * D[k1, j1]
        schedule1 = nest1.create_schedule()
        schedule1.reorder(i1, k1, j1)
        schedule = fuse((schedule0, schedule1), partial=2)
        plan = schedule.create_plan()
        package_name = 'test_partial_fusion_matmul3_naive'
        package = Package()
        package.add(plan, args=(A, B, C, D, E), base_name='test_partial_fusion_matmul3_naive')
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def test_partial_fusion_matmul3_fancy(self) -> None:
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(16, 11))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(11, 10))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(16, 10))
        D = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(10, 7))
        E = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(16, 7))
        nest0 = Nest(shape=(16, 10, 11))
        i0, j0, k0 = nest0.get_indices()

        @nest0.iteration_logic
        def _():
            C[i0, j0] += A[i0, k0] * B[k0, j0]
        schedule0 = nest0.create_schedule()
        nest1 = Nest(shape=(16, 7, 10))
        i1, j1, k1 = nest1.get_indices()

        @nest1.iteration_logic
        def _():
            E[i1, j1] += C[i1, k1] * D[k1, j1]
        schedule1 = nest1.create_schedule()
        schedule1.reorder(i1, k1, j1)
        schedule = fuse((schedule0, schedule1), partial=2)
        i, j, f, k, l = schedule.get_indices()
        ii, jj = schedule.tile({i: 4, j: 4})
        schedule.reorder(i, j, f, ii, jj, k, l)
        plan = schedule.create_plan()
        package_name = 'test_partial_fusion_matmul3_fancy'
        package = Package()
        package.add(plan, args=(A, B, C, D, E), base_name='test_partial_fusion_matmul3_fancy')
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def test_multischedule_fusion1(self) -> None:
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(4, 8))
        B = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(4,))
        accum = Array(role=Role.TEMP, element_type=ScalarType.float32, shape=(1,))
        nest0 = Nest(shape=(4,))
        nest1 = Nest(shape=(4, 8))
        nest2 = Nest(shape=(4,))
        i0 = nest0.get_indices()
        i1, j1 = nest1.get_indices()
        i2 = nest2.get_indices()

        @nest0.iteration_logic
        def _():
            accum[0] = 0.0
            B[i0] *= 2.1

        @nest1.iteration_logic
        def _():
            accum[0] += A[i1, j1]

        @nest2.iteration_logic
        def _():
            B[i2] += accum[0] * 1.2
        fused = fuse((n.create_schedule() for n in [nest0, nest1, nest2]), partial=1)
        plan = fused.create_plan()
        package_name = 'test_multischedule_fusion1'
        package = Package()
        package.add(plan, args=(A, B), base_name='test_multischedule_fusion1')
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def test_multischedule_fusion2(self) -> None:
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(4, 8, 12))
        B = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(4, 8))
        accum = Array(role=Role.TEMP, element_type=ScalarType.float32, shape=(1,))
        nest0 = Nest(shape=(4,))
        nest1 = Nest(shape=(4, 8, 12))
        nest2 = Nest(shape=(4, 8))
        i0, = nest0.get_indices()
        i1, j1, k1 = nest1.get_indices()
        i2, j2 = nest2.get_indices()

        @nest0.iteration_logic
        def _():
            accum[0] = B[i0, 0] * A[i0, 0, 0]

        @nest1.iteration_logic
        def _():
            accum[0] += A[i1, j1, k1] * 0.2

        @nest2.iteration_logic
        def _():
            B[i2, j2] *= accum[0]
        fused0 = fuse((nest1.create_schedule(), nest2.create_schedule()), partial=2)
        fused1 = fuse((nest0.create_schedule(), fused0), partial=1)
        plan = fused1.create_plan()
        package_name = 'test_multischedule_fusion2'
        package = Package()
        package.add(plan, args=(A, B), base_name='test_multischedule_fusion2')
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def test_naive_matmul(self) -> None:
        M = 128
        N = 256
        K = 256
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N))
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        sched = nest.create_schedule()
        kk = sched.split(k, 4)
        plan = sched.create_plan()
        plan.unroll(kk)
        package_name = 'test_naive_matmul'
        package = Package()
        package.add(plan, args=(A, B, C), base_name='hello_matmul_py')
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def test_mlas_matmul(self) -> None:
        from itertools import combinations_with_replacement
        from accera.samples.MatrixMultiplication import MLAS
        domains = combinations_with_replacement([1, 31, 63, 127], 3)
        package = Package()
        opts = MatrixMultiplication.Options(UseAlphaScalingFusion=False)
        for domain in domains:
            M, N, K = domain
            A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K))
            B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N))
            C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N))
            package.add(*MLAS(A, B, C, alpha=0.2, zero_C=True, opts=opts), base_name=f'mlas_py_{M}_{N}_{K}')
        package_name = 'test_mlas_matmul'
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def _test_transpose_MxN(self, M: int, N: int):
        In = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, N))
        Out = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(N, M))
        nest = Nest(shape=(M, N))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _():
            Out[j, i] = In[i, j]
        sched = nest.create_schedule()
        ii = sched.split(i, 8)
        jj = sched.split(j, 4)
        sched.reorder(i, j, ii, jj)
        plan = sched.create_plan()
        plan.vectorize(ii)
        plan.vectorize(jj)
        In_test = np.arange(stop=M * N, dtype=np.float32).reshape(M, N)
        Out_test = np.random.rand(N, M).astype(np.float32)
        Out_ref = In_test.T
        package_name = f'test_transpose_{M}x{N}'
        package = Package()
        function = package.add(plan, args=(In, Out), base_name=f'test_transpose_{M}x{N}')
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR) as v:
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR, _quiet=False)
            v.check_correctness(function.name, before=(In_test, Out_test), after=(In_test, Out_ref))

    def test_transpose_8x4(self):
        self._test_transpose_MxN(8, 4)

    def test_transpose_16x4(self):
        self._test_transpose_MxN(16, 4)

    def test_transpose_32x32(self):
        self._test_transpose_MxN(32, 32)

    def test_transpose_31x31(self):
        self._test_transpose_MxN(31, 31)

    def test_transpose_16x4_packed(self):
        In = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(16, 4))
        Out = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(4, 2, 8))
        nest = Nest(shape=(16, 4))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _():
            Out[j, i / 8 % 2, i % 8] = In[i, j]
        sched = nest.create_schedule()
        ii = sched.split(i, 8)
        plan = sched.create_plan()
        plan.unroll(i)
        plan.vectorize(ii)
        plan.vectorize(j)
        In_test = np.arange(stop=16 * 4, dtype=np.float32).reshape(16, 4)
        Out_test = np.random.rand(4, 2, 8).astype(np.float32)
        Out_ref = np.ndarray(shape=Out_test.shape, dtype=Out_test.dtype)
        for i_ in range(16):
            for j_ in range(4):
                Out_ref[j_, i_ // 8 % 2, i_ % 8] = In_test[i_, j_]
        package_name = 'test_transpose_16x4_packed'
        package = Package()
        function = package.add(plan, args=(In, Out), base_name='test_transpose_16x4_packed')
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR) as v:
            package.build(package_name, format=self.PACKAGE_FORMAT | Package.Format.MLIR_VERBOSE, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR, _quiet=False)
            v.check_correctness(function.name, before=(In_test, Out_test), after=(In_test, Out_ref))

    def _test_fast_exp_mlas(self, func_level_precision: bool):
        from accera import fast_exp_mlas, fast_exp
        M = 64
        N = 64
        In = Array(role=Role.INPUT, element_type=float, shape=(M, N))
        Out = Array(role=Role.INPUT_OUTPUT, element_type=float, shape=(M, N))
        nest = Nest((M, N))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _():
            Out[i, j] = fast_exp_mlas(In[i, j])
        sched = nest.create_schedule()
        jj = sched.split(j, 8)
        plan = sched.create_plan(Target('Intel 6700'))
        plan.vectorize(jj)
        In_test = np.random.rand(M, N).astype(np.float32)
        Out_test = np.random.rand(M, N).astype(np.float32)
        Out_ref = np.exp(In_test)
        func_opt = {'high_precision_fp': True} if func_level_precision else {}
        pkg_opt = Package._Options.NONE if func_level_precision else Package._Options.HIGH_PRECISION_FLOATING_POINT_OPS
        package_name = 'test_fast_exp_mlas'
        package = Package()
        function = package.add(plan, args=(In, Out), base_name='test_fast_exp_mlas', function_opts=func_opt)
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR) as v:
            package.build(package_name, format=self.PACKAGE_FORMAT | Package.Format.MLIR_VERBOSE, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR, _opts=pkg_opt, _quiet=False)
            v.check_correctness(function.name, before=(In_test, Out_test), after=(In_test, Out_ref))

    @expectedFailure(FailedReason.INVALID, 'avx2 instructions not supported on MacOS arm64', sys.platform == 'darwin' and platform.machine() == 'arm64')
    def test_fast_exp_mlas_w_func_level_precision(self):
        self._test_fast_exp_mlas(True)

    @expectedFailure(FailedReason.INVALID, 'avx2 instructions not supported on MacOS arm64', sys.platform == 'darwin' and platform.machine() == 'arm64')
    def test_fast_exp_mlas_w_pkg_level_precision(self):
        self._test_fast_exp_mlas(False)

    def test_emittime_cache_mlas_matmul(self) -> None:
        from accera.samples.OfflineCacheMatrixMultiplication import EmitTimeCacheMLAS
        package = Package()
        M, N, K = [31, 63, 127]
        B_data = np.array([float(x) for x in range(K * N)]).reshape(K, N).astype(np.float32)
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K))
        B = Array(role=Role.CONST, element_type=ScalarType.float32, data=B_data)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N))
        function = package.add(*EmitTimeCacheMLAS(A, B, C), base_name=f'mlas_py_{M}_{N}_{K}')
        A_test = np.ones(A.shape, dtype=np.float32) * 3.14
        B_test = np.ones(B.shape, dtype=np.float32) * 0.42
        C_test = np.ones(C.shape, dtype=np.float32) * -1.27
        C_ref = C_test + A_test @ B_test
        package_name = 'emittime_cache_mlas'
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(package_name, output_dir=output_dir, mode=self.PACKAGE_MODE, format=self.PACKAGE_FORMAT)
            v.check_correctness(function.name, before=(A_test, B_test, C_test), after=(A_test, B_test, C_ref))

    def test_runtime_init_cache_mlas_matmul(self) -> None:
        from accera.samples.OfflineCacheMatrixMultiplication import RuntimeInitCacheMLAS
        package = Package()
        M, N, K = [31, 63, 127]
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N))
        package.add(*RuntimeInitCacheMLAS(A, B, C, pack_fn_name='pack', packed_buffer_size_fn_name='packed_size'), base_name=f'mlas_py_{M}_{N}_{K}')
        package_name = 'runtime_init_cache_mlas'
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def test_const_array_shared_across_functions(self) -> None:
        package = Package()
        M = 256
        N = 256
        K = 256
        const_matrix_shape = (K, N)
        data = np.random.random(const_matrix_shape).astype(np.float32)
        const_matrix = Array(role=Role.CONST, element_type=ScalarType.float32, data=data)
        matmul_input_matrix = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K))
        matmul_output_matrix = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N))
        matmul_nest = Nest(shape=(M, N, K))
        i, j, k = matmul_nest.get_indices()

        @matmul_nest.iteration_logic
        def _():
            matmul_output_matrix[i, j] += matmul_input_matrix[i, k] * const_matrix[k, j]
        matmul_schedule = matmul_nest.create_schedule()
        matmul_plan = matmul_schedule.create_plan()
        package.add(matmul_plan, args=(matmul_input_matrix, matmul_output_matrix), base_name='matmul_fn')
        ew_add_input_matrix = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N))
        ew_add_output_matrix = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(K, N))
        ew_add_nest = Nest(shape=(K, N))
        x, y = ew_add_nest.get_indices()

        @ew_add_nest.iteration_logic
        def _():
            ew_add_output_matrix[x, y] = ew_add_input_matrix[x, y] + const_matrix[x, y]
        ew_add_schedule = ew_add_nest.create_schedule()
        ew_add_plan = ew_add_schedule.create_plan()
        package.add(ew_add_plan, args=(ew_add_input_matrix, ew_add_output_matrix), base_name='ew_add_fn')
        package_name = 'const_matrix_shared_between_functions'
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def _make_vulkan_gpu_matmul_plan(self, M, N, K):
        import math
        from accera import Target
        from accera._lang_python._lang import _If, as_index

        def get_clamped_block_dimensions(M, N, base_block_dim_M=16, base_block_dim_N=16):
            return (min(M, base_block_dim_M), min(N, base_block_dim_N))

        def compute_grid_dimensions(M, N, blockdim_M, blockdim_N):
            return (math.ceil(M / blockdim_M), math.ceil(N / blockdim_N))

        def round_up(number, multiple):
            return math.ceil(number / multiple) * multiple
        block_x, block_y = get_clamped_block_dimensions(M, N)
        grid_x, grid_y = compute_grid_dimensions(M, N, block_x, block_y)
        self.assertEqual(16, block_x)
        self.assertEqual(16, block_y)
        self.assertEqual(8, grid_x)
        self.assertEqual(16, grid_y)
        M_ = round_up(M, block_x)
        N_ = round_up(N, block_y)
        self.assertEqual(M_, M)
        self.assertEqual(N_, N)
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M_, K))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N_))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M_, N_))
        nest = Nest(shape=(M_, N_, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():

            def if_block():
                C[i, j] += A[i, k] * B[k, j]
            _If(i < as_index(M) and j < as_index(N), if_block)
        schedule = nest.create_schedule()
        ii = schedule.split(i, block_x)
        jj = schedule.split(j, block_y)
        schedule.reorder(i, j, ii, jj, k)
        target = Target(category=Target.Category.GPU, runtime=Target.Runtime.VULKAN)
        plan = schedule.create_plan(target)
        plan.bind(mapping={i: target.GridUnit.BLOCK_X, j: target.GridUnit.BLOCK_Y, ii: target.GridUnit.THREAD_X, jj: target.GridUnit.THREAD_Y})
        return (plan, (A, B, C))

    def test_vulkan_gpu_matmul(self) -> None:
        M = 128
        N = 256
        K = 256
        plan, args = self._make_vulkan_gpu_matmul_plan(M, N, K)
        package = Package()
        package.add(plan, args=args, base_name='test_vulkan_gpu_matmul')
        format = self.PACKAGE_FORMAT if 'VULKAN_SDK' in os.environ else Package.Format.HAT_STATIC
        with verifiers.VerifyPackage(self, 'test_vulkan_gpu_matmul', TEST_PACKAGE_DIR):
            package.build(name='test_vulkan_gpu_matmul', format=format, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    @expectedFailure(FailedReason.BUG, 'More than 1 Nest function cannot be added to the same GPU package for Vulkan')
    def test_two_vulkan_gpu_matmul(self) -> None:
        package = Package()
        M = 128
        N = 256
        K = 256
        plan, args = self._make_vulkan_gpu_matmul_plan(M, N, K)
        package.add(plan, args=args, base_name=f'test_two_vulkan_gpu_matmul_{M}_{N}_{K}')
        M = 256
        N = 256
        K = 256
        plan, args = self._make_vulkan_gpu_matmul_plan(M, N, K)
        package.add(plan, args=args, base_name=f'test_two_vulkan_gpu_matmul_{M}_{N}_{K}')
        format = self.PACKAGE_FORMAT if 'VULKAN_SDK' in os.environ else Package.Format.HAT_STATIC
        with verifiers.VerifyPackage(self, 'test_two_vulkan_gpu_matmul', TEST_PACKAGE_DIR):
            package.build(name='test_two_vulkan_gpu_matmul', format=format, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    @expectedFailure(FailedReason.NOT_IN_CORE, 'function that contains multiple nests')
    def test_int8_matmul(self) -> None:
        from accera import cast
        M = 128
        N = 256
        K = 256
        A = Array(role=Role.INPUT, element_type=ScalarType.int8, shape=(M, K))
        B = Array(role=Role.INPUT, element_type=ScalarType.int8, shape=(K, N))
        zero_point_A = Array(role=Role.INPUT, element_type=ScalarType.int32, shape=(1,))
        zero_point_B = Array(role=Role.INPUT, element_type=ScalarType.int32, shape=(1,))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.int32, shape=(M, N))
        col_sums = Array(role=Role.TEMP, element_type=ScalarType.int32, shape=(N,))
        row_sums = Array(role=Role.TEMP, element_type=ScalarType.int32, shape=(M,))

        def get_compute_col_sums_schedule():
            compute_col_sums_nest = Nest(shape=(K, N))
            k, j = compute_col_sums_nest.get_indices()

            @compute_col_sums_nest.iteration_logic
            def _():
                b = cast(B[k, j], ScalarType.int32)
                col_sums[j] += b
            return compute_col_sums_nest.create_schedule()

        def get_scale_col_sums_schedule():
            scale_col_sums_nest = Nest(shape=(N,))
            j = scale_col_sums_nest.get_indices()

            @scale_col_sums_nest.iteration_logic
            def _():
                col_sums[j] *= -zero_point_A
            return scale_col_sums_nest.create_schedule()

        def get_compute_row_sums_schedule():
            compute_row_sums_nest = Nest(shape=(M, K))
            i, k = compute_row_sums_nest.get_indices()

            @compute_row_sums_nest.iteration_logic
            def _():
                a = cast(A[i, k], ScalarType.int32)
                row_sums[i] += a
            return compute_row_sums_nest.create_schedule()

        def get_offset_row_sums_schedule():
            offset_row_sums_nest = Nest(shape=(M,))
            i = offset_row_sums_nest.get_indices()

            @offset_row_sums_nest.iteration_logic
            def _():
                row_sums[i] -= zero_point_A
            return offset_row_sums_nest.create_schedule()

        def get_scale_row_sums_schedule():
            scale_row_sums_nest = Nest(shape=(M,))
            i = scale_row_sums_nest.get_indices()

            @scale_row_sums_nest.iteration_logic
            def _():
                row_sums[i] *= -zero_point_B
            return scale_row_sums_nest.create_schedule()

        def get_init_c_array_schedule():
            init_c_array_nest = Nest(shape=(M, N))
            i, j = init_c_array_nest.get_indices()

            @init_c_array_nest.iteration_logic
            def _():
                C[i, j] = row_sums[i] + col_sums[j]
            return init_c_array_nest.create_schedule()

        def get_matmul_schedule():
            matmul_nest = Nest(shape=(M, N, K))
            i, j, k = matmul_nest.get_indices()

            @matmul_nest.iteration_logic
            def _():
                a = cast(A[i, k], ScalarType.int32)
                b = cast(B[k, j], ScalarType.int32)
                C[i, j] += a * b
            return matmul_nest.create_schedule()
        compute_col_sums_schedule = get_compute_col_sums_schedule()
        scale_col_sums_schedule = get_scale_col_sums_schedule()
        compute_row_sums_schedule = get_compute_row_sums_schedule()
        offset_row_sums_schedule = get_offset_row_sums_schedule()
        scale_row_sums_schedule = get_scale_row_sums_schedule()
        init_c_array_schedule = get_init_c_array_schedule()
        matmul_schedule = get_matmul_schedule()
        subschedules = (compute_col_sums_schedule, scale_col_sums_schedule, compute_row_sums_schedule, offset_row_sums_schedule, scale_row_sums_schedule, init_c_array_schedule, matmul_schedule)
        package_name = 'int8_matmul'
        package = Package()
        subfunctions = [package.add(sched, args=(A, B, C, zero_point_A, zero_point_B), base_name=package_name + '_sched_' + str(index)) for index, sched in enumerate(subschedules)]

        def main():
            for function in subfunctions:
                function(A, B, C, zero_point_A, zero_point_B)
        main_function = package.add(main, args=(A, B, C, zero_point_A, zero_point_B), base_name=package_name)
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def _verify_three_matrix_multiplication_function(self, function: 'accera.Function', package: Package, package_name: str) -> None:
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(name=package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir)
            A_test, B_test, D_test, E_test = (np.random.random(p.shape).astype(np.float32) for p in function.args)
            E_ref = E_test + A_test @ B_test @ D_test
            v.check_correctness(function.name, before=(A_test, B_test, D_test, E_test), after=(A_test, B_test, D_test, E_ref))

    def test_three_matrix_multiplication_case_study_part1(self) -> None:
        import accera as acc
        A = acc.Array(role=acc.Role.INPUT, shape=(256, 32))
        B = acc.Array(role=acc.Role.INPUT, shape=(32, 256))
        C = acc.Array(role=acc.Role.TEMP, shape=(256, 256))
        D = acc.Array(role=acc.Role.INPUT, shape=(256, 32))
        E = acc.Array(role=acc.Role.INPUT_OUTPUT, shape=(256, 32))
        nest0 = acc.Nest(shape=(256, 256, 32))
        i0, j0, k0 = nest0.get_indices()

        @nest0.iteration_logic
        def _():
            C[i0, j0] += A[i0, k0] * B[k0, j0]
        schedule0 = nest0.create_schedule()
        nest1 = acc.Nest(shape=(256, 32, 256))
        i1, j1, k1 = nest1.get_indices()

        @nest1.iteration_logic
        def _():
            E[i1, j1] += C[i1, k1] * D[k1, j1]
        schedule1 = nest1.create_schedule()
        schedule0.reorder(i0, j0, k0)
        schedule1.reorder(i1, k1, j1)
        schedule = acc.fuse((schedule0, schedule1), partial=2)
        i, j, f, k0, j1 = schedule.get_indices()
        ii, jj = schedule.tile({i: 16, j: 32})
        schedule.reorder(i, j, f, jj, k0, j1, ii)
        plan = schedule.create_plan()
        plan.cache(A, index=f, layout=acc.Array.Layout.LAST_MAJOR)
        plan.cache(B, index=f)
        plan.cache(C, index=f, layout=acc.Array.Layout.LAST_MAJOR)
        plan.cache(D, index=f)
        plan.cache(E, index=f, layout=acc.Array.Layout.LAST_MAJOR)
        plan.vectorize(ii)
        package = Package()
        function = package.add(plan, args=(A, B, D, E), base_name='fused_three_matrix_multiplication')
        self._verify_three_matrix_multiplication_function(function, package, 'three_matrix_multiplication_case_study_part1')

    def test_three_matrix_multiplication_case_study_part2(self) -> None:
        import accera as acc
        A = acc.Array(role=acc.Role.INPUT, shape=(256, 32))
        B = acc.Array(role=acc.Role.INPUT, shape=(32, 256))
        C = acc.Array(role=acc.Role.TEMP, shape=(256, 256))
        D = acc.Array(role=acc.Role.INPUT, shape=(256, 32))
        E = acc.Array(role=acc.Role.INPUT_OUTPUT, shape=(256, 32))
        nest0 = acc.Nest(shape=(256, 256, 32))
        i0, j0, k0 = nest0.get_indices()

        @nest0.iteration_logic
        def _():
            C[i0, j0] += A[i0, k0] * B[k0, j0]
        schedule0 = nest0.create_schedule()
        nest1 = acc.Nest(shape=(256, 32, 256))
        i1, j1, k1 = nest1.get_indices()

        @nest1.iteration_logic
        def _():
            E[i1, j1] += C[i1, k1] * D[k1, j1]
        schedule1 = nest1.create_schedule()
        jj0 = schedule0.split(j0, 8)
        kk1 = schedule1.split(k1, 8)
        schedule0.reorder(i0, j0, jj0, k0)
        schedule1.reorder(i1, k1, j1, kk1)
        schedule = acc.fuse((schedule0, schedule1), partial=2)
        i, j, f, jj0, k0, j1, kk1 = schedule.get_indices()
        ii, jj1 = schedule.tile({i: 64, j1: 8})
        schedule.reorder(i, j, f, j1, ii, k0, jj0, kk1, jj1)
        plan = schedule.create_plan()
        plan.cache(A, index=f)
        plan.cache(B, index=f, layout=acc.Array.Layout.FIRST_MAJOR)
        plan.cache(C, index=f, layout=acc.Array.Layout.FIRST_MAJOR)
        plan.cache(D, index=f, layout=acc.Array.Layout.FIRST_MAJOR)
        plan.cache(E, index=f, layout=acc.Array.Layout.FIRST_MAJOR)
        plan.vectorize(jj0)
        plan.vectorize(jj1)
        package = Package()
        function = package.add(plan, args=(A, B, D, E), base_name='fused_three_matrix_multiplication_part2')
        self._verify_three_matrix_multiplication_function(function, package, 'three_matrix_multiplication_case_study_part2')

    def test_three_matrix_multiplication_case_study_part3(self) -> None:
        import accera as acc
        A = acc.Array(role=acc.Role.INPUT, shape=(256, 32))
        B = acc.Array(role=acc.Role.INPUT, shape=(32, 256))
        C = acc.Array(role=acc.Role.TEMP, shape=(256, 256))
        D = acc.Array(role=acc.Role.INPUT, shape=(256, 32))
        E = acc.Array(role=acc.Role.INPUT_OUTPUT, shape=(256, 32))
        nest0 = acc.Nest(shape=(256, 256, 32))
        i0, j0, k0 = nest0.get_indices()

        @nest0.iteration_logic
        def _():
            C[i0, j0] += A[i0, k0] * B[k0, j0]
        schedule0 = nest0.create_schedule()
        nest1 = acc.Nest(shape=(256, 32, 256))
        i1, j1, k1 = nest1.get_indices()

        @nest1.iteration_logic
        def _():
            E[i1, j1] += C[i1, k1] * D[k1, j1]
        schedule1 = nest1.create_schedule()
        jj0 = schedule0.split(j0, 8)
        kk1 = schedule1.split(k1, 8)
        schedule0.reorder(i0, j0, jj0, k0)
        schedule1.reorder(i1, k1, j1, kk1)
        schedule = acc.fuse((schedule0, schedule1), partial=2)
        i, j, f, jj0, k0, j1, kk1 = schedule.get_indices()
        ii, kk0 = schedule.tile({i: 64, k0: 8})
        schedule.reorder(i, j, f, ii, jj0, k0, kk0, j1, kk1)
        plan = schedule.create_plan()
        plan.cache(A, index=f, layout=acc.Array.Layout.FIRST_MAJOR)
        plan.cache(B, index=f, layout=acc.Array.Layout.LAST_MAJOR)
        plan.cache(C, index=f, layout=acc.Array.Layout.FIRST_MAJOR)
        plan.cache(D, index=f, layout=acc.Array.Layout.LAST_MAJOR)
        plan.cache(E, index=f)
        package = Package()
        function = package.add(plan, args=(A, B, D, E), base_name='fused_three_matrix_multiplication_part3')
        self._verify_three_matrix_multiplication_function(function, package, 'three_matrix_multiplication_case_study_part3')

    def test_naive_conv2d_skew(self) -> None:
        N = 224
        Fi = 3
        Fo = 5
        K = 2
        M = N - K + 1
        Input = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N, N, Fi))
        Kernel = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, K, Fi, Fo))
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, M, Fo))
        nest = Nest(shape=(Fo, M, M, Fi, K, K))
        out_ch, out_r, out_c, in_ch, k_r, k_c = nest.get_indices()

        @nest.iteration_logic
        def _():
            Output[out_r, out_c, out_ch] += Input[out_r + k_r, out_c + k_c, in_ch] * Kernel[k_r, k_c, in_ch, out_ch]
        schedule = nest.create_schedule()
        schedule.skew(out_r, k_r)
        schedule.skew(out_c, k_c, unroll_loops_smaller_than=3)
        schedule.reorder(out_ch, in_ch, out_r, out_c, k_r, k_c)
        package = Package()
        function = package.add(schedule, args=(Input, Kernel, Output), base_name='naive_conv2d_skew')
        package_name = 'test_naive_conv2d_skew'
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(name=package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir)

            def naive_convolution_ref(input, kernel, output, row_stride=1, column_stride=1, row_padding=0, column_padding=0):
                input_rows, input_columns, input_channels = input.shape
                output_rows, output_columns, out_filters = output.shape
                kernel_rows, kernel_columns, _, _ = kernel.shape
                output_ref = output.copy()
                for out_f in range(out_filters):
                    for out_r in range(output_rows):
                        for out_c in range(output_columns):
                            for in_ch in range(input_channels):
                                for k_r in range(kernel_rows):
                                    for k_c in range(kernel_columns):
                                        in_r = out_r * row_stride + k_r - row_padding
                                        in_c = out_c * column_stride + k_c - column_padding
                                        if in_r >= 0 and in_r < input_rows and (in_c >= 0) and (in_c < input_columns):
                                            output_ref[out_r, out_c, out_f] += input[in_r, in_c, in_ch] * kernel[k_r, k_c, in_ch, out_f]
                return output_ref
            Input_test, Kernel_test, Output_test = (np.random.random(p.shape).astype(np.float32) for p in function.args)
            Output_ref = naive_convolution_ref(Input_test, Kernel_test, Output_test)
            v.check_correctness(function.name, before=(Input_test, Kernel_test, Output_test), after=(Input_test, Kernel_test, Output_ref))

    def test_strided_sub_array(self) -> None:
        N = 5
        subArrayNumRows = 2
        subArrayNumCols = 3
        Input = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(N, N))
        out_nest = Nest(shape=(subArrayNumRows, subArrayNumCols))
        i, j = out_nest.get_indices()

        @out_nest.iteration_logic
        def _():
            Output = Input.sub_array([1, 1], [subArrayNumRows, subArrayNumCols], [2, 1])
            Output[i, j] = 0.0
        schedule = out_nest.create_schedule()
        package = Package()
        function = package.add(schedule, args=(Input,), base_name='strided_sub_array')
        package_name = 'test_strided_sub_array'
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(name=package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir)
            Data = np.random.random([N, N]).astype(np.float32)
            DataStrided = Data.copy()
            DataStrided[1, 1] = 0.0
            DataStrided[1, 2] = 0.0
            DataStrided[1, 3] = 0.0
            DataStrided[3, 1] = 0.0
            DataStrided[3, 2] = 0.0
            DataStrided[3, 3] = 0.0
            v.check_correctness(function.name, before=(Data,), after=(DataStrided,))

    def test_offset_sub_array_packing_flat(self) -> None:
        test_name = 'test_offset_sub_array_packing_flat'
        N = 8
        output_size = N * N + N
        Input = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N, N))
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(output_size,))
        package = Package()
        diagonal_fetch_nest = Nest(shape=(N,))
        diagonal_idx, = diagonal_fetch_nest.get_indices()

        @diagonal_fetch_nest.iteration_logic
        def _diag_fetch():
            diag_vec = Output.sub_array(offsets=(0,), shape=(N,))
            diag_vec[diagonal_idx] = Input[diagonal_idx, diagonal_idx]
        diag_fn = package.add(diagonal_fetch_nest, args=(Input, Output), base_name='diagonal_fetch_fn')
        transpose_nest = Nest(shape=(N, N))
        transpose_i, transpose_j = transpose_nest.get_indices()

        @transpose_nest.iteration_logic
        def _transpose():
            packed_output = Output.sub_array(offsets=(N,), shape=(N * N,))
            packed_output[transpose_j * N + transpose_i] = Input[transpose_i, transpose_j]
        transpose_fn = package.add(transpose_nest, args=(Input, Output), base_name='transpose_fn')
        outer_nest = Nest(shape=(1,))

        @outer_nest.iteration_logic
        def _():
            diag_fn(Input, Output)
            transpose_fn(Input, Output)
        function = package.add(outer_nest, args=(Input, Output), base_name=test_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(name=test_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir)
            test_input = np.random.random([N, N]).astype(np.float32)
            test_output = np.random.random([N * N + N]).astype(np.float32)
            test_output_ref = np.random.random([N * N + N]).astype(np.float32)
            for i in range(N):
                test_output_ref[i] = test_input[i, i]
                for j in range(N):
                    test_output_ref[N + (i * N + j)] = test_input[j, i]
            v.check_correctness(function.name, before=(test_input, test_output), after=(test_input, test_output_ref))

    def test_offset_sub_array_packing_split_dim(self) -> None:
        test_name = 'test_offset_sub_array_packing_split_dim'
        N = 4
        output_size = N * N + N
        Input = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N, N))
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(output_size,))
        package = Package()
        diagonal_fetch_nest = Nest(shape=(N,))
        diagonal_idx, = diagonal_fetch_nest.get_indices()

        @diagonal_fetch_nest.iteration_logic
        def _diag_fetch():
            diag_vec = Output.sub_array(offsets=(0,), shape=(N,))
            diag_vec[diagonal_idx] = Input[diagonal_idx, diagonal_idx]
        diag_fn = package.add(diagonal_fetch_nest, args=(Input, Output), base_name='diagonal_fetch_fn')
        transpose_nest = Nest(shape=(N, N))
        transpose_i, transpose_j = transpose_nest.get_indices()

        @transpose_nest.iteration_logic
        def _transpose():
            packed_output = Output.sub_array(offsets=(N,), shape=(N * N,))
            packed_output_split = packed_output._split_dimension(0, cast(N, ScalarType.index))
            packed_output_split[transpose_j, transpose_i] = Input[transpose_i, transpose_j]
        transpose_fn = package.add(transpose_nest, args=(Input, Output), base_name='transpose_fn')
        outer_nest = Nest(shape=(1,))

        @outer_nest.iteration_logic
        def _():
            diag_fn(Input, Output)
            transpose_fn(Input, Output)
        function = package.add(outer_nest, args=(Input, Output), base_name=test_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(name=test_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir)
            test_input = np.random.random([N, N]).astype(np.float32)
            test_output = np.random.random([N * N + N]).astype(np.float32)
            test_output_ref = np.random.random([N * N + N]).astype(np.float32)
            for i in range(N):
                test_output_ref[i] = test_input[i, i]
                for j in range(N):
                    test_output_ref[N + (i * N + j)] = test_input[j, i]
            v.check_correctness(function.name, before=(test_input, test_output), after=(test_input, test_output_ref))

    def test_offset_sub_array_packing_multiple_split_dim(self) -> None:
        test_name = 'test_offset_sub_array_packing_multiple_split_dim'
        N = 4
        N_inner = 2
        output_size = N * N + N
        Input = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N, N))
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(output_size,))
        package = Package()
        diagonal_fetch_nest = Nest(shape=(N,))
        diagonal_idx, = diagonal_fetch_nest.get_indices()

        @diagonal_fetch_nest.iteration_logic
        def _diag_fetch():
            diag_vec = Output.sub_array(offsets=(0,), shape=(N,))
            diag_vec[diagonal_idx] = Input[diagonal_idx, diagonal_idx]
        diag_fn = package.add(diagonal_fetch_nest, args=(Input, Output), base_name='diagonal_fetch_fn')
        transpose_nest = Nest(shape=(N // N_inner, N // N_inner, N_inner, N_inner))
        transpose_i, transpose_j, transpose_ii, transpose_jj = transpose_nest.get_indices()

        @transpose_nest.iteration_logic
        def _transpose():
            packed_output = Output.sub_array(offsets=(N,), shape=(N * N,))
            packed_output_split_0 = packed_output._split_dimension(0, cast(N, ScalarType.index))
            packed_output_split_1 = packed_output_split_0._split_dimension(1, cast(N_inner, ScalarType.index))
            packed_output_split_2 = packed_output_split_1._split_dimension(0, cast(N_inner, ScalarType.index))
            i = transpose_i * N_inner + transpose_ii
            j = transpose_j * N_inner + transpose_jj
            packed_output_split_2[transpose_i, transpose_j, transpose_jj, transpose_ii] = Input[i, j]
        transpose_fn = package.add(transpose_nest, args=(Input, Output), base_name='transpose_fn')
        outer_nest = Nest(shape=(1,))

        @outer_nest.iteration_logic
        def _():
            diag_fn(Input, Output)
            transpose_fn(Input, Output)
        function = package.add(outer_nest, args=(Input, Output), base_name=test_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(name=test_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir)
            test_input = np.random.random([N, N]).astype(np.float32)
            test_output = np.random.random([N * N + N]).astype(np.float32)
            test_output_ref = np.random.random([N * N + N]).astype(np.float32)
            for i in range(0, N, N_inner):
                for j in range(0, N, N_inner):
                    for ii in range(N_inner):
                        test_output_ref[i + ii] = test_input[i + ii, i + ii]
                        for jj in range(N_inner):
                            test_output_ref[N + (i * (N // N_inner * N_inner) + j * N_inner + jj * N_inner + ii)] = test_input[i + ii, j + jj]
            v.check_correctness(function.name, before=(test_input, test_output), after=(test_input, test_output_ref))

    def test_shifting_shrinking_sub_array(self) -> None:
        N = 64
        test_name = 'test_shifting_shrinking_sub_array'
        Input = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N,))
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(N,))
        package = Package()
        nest = Nest(shape=(N,))
        idx, = nest.get_indices()

        @nest.iteration_logic
        def _fn():
            size = N - idx
            sub_arr = Input.sub_array(offsets=(idx,), shape=(size,))
            Output[0] = sub_arr[0]
        function = package.add(nest, args=(Input, Output), base_name=test_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(name=test_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir)
            test_input = np.random.random([N]).astype(np.float32)
            test_output = test_input.copy()
            test_output_ref = test_input.copy()
            test_output_ref[0] = test_input[-1]
            v.check_correctness(function.name, before=(test_input, test_output), after=(test_input, test_output_ref))

    def test_dynamic_sub_array_split_dim_subfunction(self) -> None:
        from accera import create_dimensions
        test_name = 'test_dynamic_sub_array_split_dim_subfunction'
        N = 64
        tile_size = 20
        inner_split_size = 2
        package = Package()
        Input = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N,))
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(N,))
        current_outer_idx, extent = create_dimensions()
        inner_nest = Nest(shape=(extent,))
        inner_idx, = inner_nest.get_indices()

        @inner_nest.iteration_logic
        def _inner_fn():
            full_idx = current_outer_idx + inner_idx
            tile_remaining_elts = accmin(N - current_outer_idx, cast(tile_size, ScalarType.index))
            sub_arr = Output.sub_array(offsets=(current_outer_idx,), shape=(tile_remaining_elts,))
            split_arr = sub_arr._split_dimension(0, cast(inner_split_size, ScalarType.index))
            split_arr[inner_idx / inner_split_size, inner_idx % inner_split_size] = Input[full_idx]
        inner_fn = package.add(inner_nest, args=(extent, Input, Output, current_outer_idx), base_name=f'{test_name}_inner_fn', function_opts=INTERNAL_FUNCTION_OPTS)
        outer_nest = Nest(shape=(N,))
        outer_idx, = outer_nest.get_indices()

        @outer_nest.iteration_logic
        def _outer_fn():
            extent_val = accmin(N - outer_idx, cast(tile_size, ScalarType.index))
            inner_fn(extent_val, Input, Output, outer_idx)
        outer_sched = outer_nest.create_schedule()
        outer_idx_inner = outer_sched.split(outer_idx, tile_size)
        outer_sched.reorder(outer_idx, outer_idx_inner)
        outer_plan = outer_sched.create_plan()
        outer_plan._erase_loops([outer_idx_inner])
        function = package.add(outer_plan, args=(Input, Output), base_name=test_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(name=test_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir, _quiet=False)
            test_input = np.random.random([N]).astype(np.float32)
            test_output = np.random.random([N]).astype(np.float32)
            test_output_ref = test_input.copy()
            v.check_correctness(function.name, before=(test_input, test_output), after=(test_input, test_output_ref))

    def test_dynamic_sub_array_multi_split_dim_subfunction(self) -> None:
        from accera import create_dimensions
        test_name = 'test_dynamic_sub_array_multi_split_dim_subfunction'
        M = 76
        N = 92
        m_tile_outer = 16
        m_tile_inner = 2
        n_tile_outer = 32
        n_tile_inner = 4
        package = Package()
        Input = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, N))
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M * N,))
        current_outer_i, current_outer_j = create_dimensions()
        extent_i, extent_j = create_dimensions()
        inner_nest = Nest(shape=(extent_i, extent_j))
        inner_i, inner_j = inner_nest.get_indices()

        @inner_nest.iteration_logic
        def _inner_fn():
            full_i = current_outer_i + inner_i
            full_j = current_outer_j + inner_j
            remaining_m_tile = accmin(M - current_outer_i, cast(m_tile_outer, ScalarType.index))
            remaining_n_tile = accmin(N - current_outer_j, cast(n_tile_outer, ScalarType.index))
            output_offset_pos = current_outer_i * N + current_outer_j * remaining_m_tile
            remaining_mn_tile = accmin(remaining_m_tile * remaining_n_tile, cast(m_tile_outer * n_tile_outer, ScalarType.index))
            sub_arr = Output.sub_array(offsets=(output_offset_pos,), shape=(remaining_mn_tile,))
            split_arr_1 = sub_arr._split_dimension(0, cast(n_tile_inner, ScalarType.index))
            split_arr_2 = split_arr_1._split_dimension(0, cast(m_tile_inner, ScalarType.index))
            dynamic_j_split = remaining_n_tile / n_tile_inner
            split_arr_3 = split_arr_2._split_dimension(0, cast(dynamic_j_split, ScalarType.index))
            split_arr_3[inner_i / m_tile_inner, inner_j / n_tile_inner, inner_i % m_tile_inner, inner_j % n_tile_inner] = Input[full_i, full_j]
        inner_fn = package.add(inner_nest, args=(extent_i, extent_j, Input, Output, current_outer_i, current_outer_j), base_name=f'{test_name}_inner_fn', function_opts=INTERNAL_FUNCTION_OPTS)
        outer_nest = Nest(shape=(M, N))
        outer_i, outer_j = outer_nest.get_indices()

        @outer_nest.iteration_logic
        def _outer_fn():
            extent_i_val = accmin(M - outer_i, cast(m_tile_outer, ScalarType.index))
            extent_j_val = accmin(N - outer_j, cast(n_tile_outer, ScalarType.index))
            inner_fn(extent_i_val, extent_j_val, Input, Output, outer_i, outer_j)
        outer_sched = outer_nest.create_schedule()
        outer_ii, outer_jj = outer_sched.tile(dict(zip([outer_i, outer_j], [m_tile_outer, n_tile_outer])))
        outer_sched.reorder(outer_i, outer_j, outer_ii, outer_jj)
        outer_plan = outer_sched.create_plan()
        outer_plan._erase_loops([outer_ii, outer_jj])
        function = package.add(outer_plan, args=(Input, Output), base_name=test_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(name=test_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir, _quiet=False)
            test_input = np.random.random([M, N]).astype(np.float32)
            test_output = np.random.random([M * N]).astype(np.float32)
            test_output_ref = np.random.random([M * N]).astype(np.float32)

            def partition_value(range_val, split):
                return range_val // split * split
            M_pv = partition_value(M, m_tile_outer)
            N_pv = partition_value(N, n_tile_outer)
            m_tile_outer_cleanup = M - M_pv
            n_tile_outer_cleanup = N - N_pv

            def packed_index(i_outer, i_middle, i_inner, j_outer, j_middle, j_inner, tile_offset, n_tile_outer_clamped):
                return tile_offset + i_middle * n_tile_outer_clamped + j_middle * m_tile_inner + i_inner * n_tile_inner + j_inner
            for i_outer in range(0, M_pv, m_tile_outer):
                for j_outer in range(0, N_pv, n_tile_outer):
                    tile_offset = i_outer * N + j_outer * m_tile_outer
                    for i_middle in range(0, m_tile_outer, m_tile_inner):
                        for j_middle in range(0, n_tile_outer, n_tile_inner):
                            for i_inner in range(m_tile_inner):
                                for j_inner in range(n_tile_inner):
                                    test_output_ref[packed_index(i_outer, i_middle, i_inner, j_outer, j_middle, j_inner, tile_offset, n_tile_outer)] = test_input[i_outer + i_middle + i_inner, j_outer + j_middle + j_inner]
                for j_outer in range(N_pv, N, n_tile_outer):
                    tile_offset = i_outer * N + j_outer * m_tile_outer
                    for i_middle in range(0, m_tile_outer, m_tile_inner):
                        for j_middle in range(0, n_tile_outer_cleanup, n_tile_inner):
                            for i_inner in range(m_tile_inner):
                                for j_inner in range(n_tile_inner):
                                    test_output_ref[packed_index(i_outer, i_middle, i_inner, j_outer, j_middle, j_inner, tile_offset, n_tile_outer_cleanup)] = test_input[i_outer + i_middle + i_inner, j_outer + j_middle + j_inner]
            for i_outer in range(M_pv, M, m_tile_outer):
                for j_outer in range(0, N_pv, n_tile_outer):
                    tile_offset = i_outer * N + j_outer * m_tile_outer_cleanup
                    for i_middle in range(0, m_tile_outer_cleanup, m_tile_inner):
                        for j_middle in range(0, n_tile_outer, n_tile_inner):
                            for i_inner in range(m_tile_inner):
                                for j_inner in range(n_tile_inner):
                                    test_output_ref[packed_index(i_outer, i_middle, i_inner, j_outer, j_middle, j_inner, tile_offset, n_tile_outer)] = test_input[i_outer + i_middle + i_inner, j_outer + j_middle + j_inner]
                for j_outer in range(N_pv, N, n_tile_outer):
                    tile_offset = i_outer * N + j_outer * m_tile_outer_cleanup
                    for i_middle in range(0, m_tile_outer_cleanup, m_tile_inner):
                        for j_middle in range(0, n_tile_outer_cleanup, n_tile_inner):
                            for i_inner in range(m_tile_inner):
                                for j_inner in range(n_tile_inner):
                                    test_output_ref[packed_index(i_outer, i_middle, i_inner, j_outer, j_middle, j_inner, tile_offset, n_tile_outer_cleanup)] = test_input[i_outer + i_middle + i_inner, j_outer + j_middle + j_inner]
            v.check_correctness(function.name, before=(test_input, test_output), after=(test_input, test_output_ref))

    @expectedFailure(FailedReason.BUG, '_split_dimension of a dynamically sized dimension with a dynamic size is not working')
    def test_dynamic_split_dim_dynamic_size(self) -> None:
        from accera import create_dimensions
        test_name = 'test_dynamic_split_dim_dynamic_size'
        M, N, MN = create_dimensions()
        package = Package()
        Input = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(MN,))
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N))
        nest = Nest(shape=(M, N))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _():
            split_input = Input._split_dimension(0, N)
            Output[i, j] = split_input[i, j]
        fn = package.add(nest, args=(MN, M, N, Input, Output), base_name=f'{test_name}_fn')
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(name=test_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir, _quiet=False)
            test_M = 64
            test_N = 16
            test_MN = test_M * test_N
            test_input = np.random.random([test_M * test_N]).astype(np.float32)
            test_output = np.random.random([test_M, test_N]).astype(np.float32)
            test_output_ref = test_input.copy().reshape((test_M, test_N))
            v.check_correctness(function.name, before=(test_MN, test_M, test_N, test_input, test_output), after=(test_MN, test_M, test_N, test_input, test_output_ref))

    @expectedFailure(FailedReason.BUG, '_split_dimension of a dynamically sized dimension with a static size is not working')
    def test_dynamic_split_dim_static_size(self) -> None:
        from accera import create_dimensions
        test_name = 'test_dynamic_split_dim_static_size'
        M, MN = create_dimensions()
        N = 16
        package = Package()
        Input = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(MN,))
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N))
        nest = Nest(shape=(M, N))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _():
            split_input = Input._split_dimension(0, cast(16, ScalarType.index))
            Output[i, j] = split_input[i, j]
        fn = package.add(nest, args=(MN, M, Input, Output), base_name=f'{test_name}_fn')
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(name=test_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir, _quiet=False)
            test_M = 64
            test_N = N
            test_MN = test_M * test_N
            test_input = np.random.random([test_M * test_N]).astype(np.float32)
            test_output = np.random.random([test_M, test_N]).astype(np.float32)
            test_output_ref = test_input.copy().reshape((test_M, test_N))
            v.check_correctness(function.name, before=(test_MN, test_M, test_input, test_output), after=(test_MN, test_M, test_input, test_output_ref))

    def test_padded_nchwc_conv2d_manual_cache(self) -> None:
        input_channels = 64
        base_input_shape = (input_channels, 28, 28)
        buffer_padding = (0, 1, 1)
        conv_padding = (0, 1, 1)
        stride = (2, 2)
        kernel_shape = (3, 3)
        output_filters = 64
        import math
        unpadded_output_rows = math.floor((base_input_shape[1] + 2 * conv_padding[1] - (kernel_shape[0] - 1) - 1) / stride[0] + 1)
        unpadded_output_columns = math.floor((base_input_shape[2] + 2 * conv_padding[2] - (kernel_shape[1] - 1) - 1) / stride[1] + 1)
        base_output_shape = (output_filters, unpadded_output_rows, unpadded_output_columns)
        padded_input_shape = [base_input_shape[i] + 2 * buffer_padding[i] for i in range(len(base_input_shape))]
        padded_output_shape = [base_output_shape[i] + 2 * buffer_padding[i] for i in range(len(base_output_shape))]
        channels_per_block = 8
        input_channel_blocks = padded_input_shape[0] // channels_per_block
        output_filter_blocks = padded_output_shape[0] // channels_per_block
        nchwc_padded_input_shape = (input_channel_blocks, padded_input_shape[1], padded_input_shape[2], channels_per_block)
        nchwc_weights_shape = (kernel_shape[0], kernel_shape[1], input_channels, output_filters)
        nchwc_padded_output_shape = (output_filter_blocks, padded_output_shape[1], padded_output_shape[2], channels_per_block)
        Input = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=nchwc_padded_input_shape)
        Kernel = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=nchwc_weights_shape)
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=nchwc_padded_output_shape)
        nest = Nest(shape=(output_filter_blocks, input_channel_blocks, unpadded_output_rows, kernel_shape[0], kernel_shape[1], channels_per_block, unpadded_output_columns, channels_per_block))
        out_f, in_ch, out_r, k_r, k_c, in_ch_b, out_c, out_f_b = nest.get_indices()
        row_stride, column_stride = stride
        channel_padding, row_padding, column_padding = conv_padding
        channel_buffer_padding, row_buffer_padding, column_buffer_padding = buffer_padding

        @nest.iteration_logic
        def _():
            in_r = out_r * row_stride - row_padding + k_r
            in_c = out_c * column_stride - column_padding + k_c
            Output[out_f, out_r + row_buffer_padding, out_c + column_buffer_padding, out_f_b] += Input[in_ch, in_r + row_buffer_padding, in_c + column_buffer_padding, in_ch_b] * Kernel[k_r, k_c, in_ch * channels_per_block + in_ch_b, out_f * channels_per_block + out_f_b]
        schedule = nest.create_schedule()
        out_c2 = schedule.split(out_c, 3)
        out_f2 = schedule.split(out_f, 4)
        schedule.reorder(out_f, in_ch, out_r, out_c, k_r, k_c, in_ch_b, out_f2, out_c2, out_f_b)
        plan = schedule.create_plan()
        plan.cache(Input, index=in_ch_b, layout=Array.Layout.FIRST_MAJOR)
        plan.cache(Output, index=out_f2, layout=Array.Layout.FIRST_MAJOR)
        plan.cache(Kernel, index=in_ch_b, layout=Array.Layout.FIRST_MAJOR)
        plan.kernelize(unroll_indices=(in_ch_b, out_f2, out_c2), vectorize_indices=out_f_b)
        package = Package()
        function = package.add(plan, args=(Input, Kernel, Output), base_name='nchwc_conv2d_manual_cache')
        package_name = 'test_nchwc_conv2d_manual_cache'
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(name=package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir)

            def naive_nchwc_convolution_ref(input, kernel, output):
                input_channel_blocks, input_rows, input_columns, input_channels = input.shape
                out_filter_blocks, output_rows, output_columns, out_filters = output.shape
                kernel_rows, kernel_columns, _, _ = kernel.shape
                output_ref = output.copy()
                for out_f_block in range(out_filter_blocks):
                    for out_f in range(out_filters):
                        for out_r in range(output_rows - 2 * row_buffer_padding):
                            for out_c in range(output_columns - 2 * column_buffer_padding):
                                for in_ch_block in range(input_channel_blocks):
                                    for in_ch in range(input_channels):
                                        for k_r in range(kernel_rows):
                                            for k_c in range(kernel_columns):
                                                in_r = out_r * row_stride + k_r - row_padding
                                                in_c = out_c * column_stride + k_c - column_padding
                                                output_ref[out_f_block, out_r + row_buffer_padding, out_c + column_buffer_padding, out_f] += input[in_ch_block, in_r + row_buffer_padding, in_c + column_buffer_padding, in_ch] * kernel[k_r, k_c, in_ch_block * channels_per_block + in_ch, out_f_block * channels_per_block + out_f]
                return output_ref
            Input_test, Kernel_test, Output_test = (np.random.random(p.shape).astype(np.float32) for p in function.args)
            Output_ref = naive_nchwc_convolution_ref(Input_test, Kernel_test, Output_test)
            v.check_correctness(function.name, before=(Input_test, Kernel_test, Output_test), after=(Input_test, Kernel_test, Output_ref))

    def test_large_cache_vectorized(self) -> None:
        M = 1024
        N = 1024
        S = 1024
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, S))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(S, N))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N))
        nest = Nest(shape=(M, N, S))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii = schedule.split(i, 512)
        jj = schedule.split(j, 512)
        kk = schedule.split(k, 512)
        schedule.reorder(i, j, k, ii, jj, kk)
        plan = schedule.create_plan()
        plan.cache(B, index=ii, layout=Array.Layout.FIRST_MAJOR)
        plan.vectorize(kk)
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name='test_large_cache_vectorized')
        package_name = 'test_large_cache_vectorized'
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir):
            package.build(name=package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir)

    def test_cross_compile(self) -> None:
        from accera import Target
        M = 128
        N = 256
        K = 256
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N))
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        sched = nest.create_schedule()
        kk = sched.split(k, 4)
        pi3 = Target(Target.Model.RASPBERRY_PI_3B, category=Target.Category.CPU)
        plan = sched.create_plan(pi3)
        plan.unroll(kk)
        package = Package()
        package.add(plan, args=(A, B, C), base_name='hello_matmul_pi3_py')
        with verifiers.VerifyPackage(self, 'hello_matmul_pi3', TEST_PACKAGE_DIR):
            package.build(name='hello_matmul_pi3', format=Package.Format.HAT_STATIC, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR, platform=Package.Platform.RASPBIAN)

    def test_parameter_grid_no_regression(self) -> None:
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(16, 16))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(16, 16))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(16, 16))
        nest = Nest(shape=[16, 16, 16])
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii = schedule.split(i, size=4)
        plan = schedule.create_plan()
        package = Package()
        package.add(plan, args=(A, B, C), base_name='alternative_matmul_16_16_16')
        package.build('hello_matmul_parameter_grid1', output_dir=TEST_PACKAGE_DIR)
        self.assertTrue(os.path.isdir(TEST_PACKAGE_DIR))

    def test_parameter_grid(self) -> None:
        P0, P1, P2, P3, P4, P5 = create_parameters()
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(P0, P2))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(P2, P1))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(P0, P1))
        nest = Nest(shape=[P0, P1, P2])
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii = schedule.split(i, size=P3)
        schedule.reorder(order=P5)
        plan = schedule.create_plan()
        plan.cache(A, level=P4)
        package = Package()
        package.add(plan, args=(A, B, C), parameters={P0: 16, P1: 16, P2: 16, P3: 4, P4: 2, P5: (j, k, i, ii)}, base_name='alternative_matmul_16_16_16')
        package.build('hello_matmul_parameter_grid', output_dir=TEST_PACKAGE_DIR)
        self.assertTrue(os.path.isdir(TEST_PACKAGE_DIR))

    def _verify_matrix_multiplication_function(self, function: 'accera.Function', package: Package, package_name: str, file_check_fn: Callable=None, check_correctness: bool=True, tolerance: float=1e-05, file_list: List[str]=None, package_format: Package.Format=None, package_mode: Package.Mode=None, fail_on_error: bool=True, quiet=True) -> None:
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        package_format = package_format or self.PACKAGE_FORMAT
        package_mode = package_mode or self.PACKAGE_MODE
        if file_check_fn:
            package_format |= Package.Format.MLIR
        with verifiers.VerifyPackage(self, package_name, output_dir, file_list=file_list) as v:
            package.build(name=package_name, format=package_format, mode=package_mode, output_dir=output_dir, fail_on_error=fail_on_error, _quiet=quiet)
            if check_correctness:
                A_test, B_test, C_test = (np.ndarray(p.shape, dtype=np.dtype(p.element_type.name), order=p.requested_layout.to_numpy_order()) for p in function.requested_args)
                A_test_data, B_test_data, C_test_data = (np.random.random(p.shape).astype(np.dtype(p.element_type.name)) for p in function.requested_args)
                A_test[:] = A_test_data
                B_test[:] = B_test_data
                C_test[:] = C_test_data
                C_ref = C_test + A_test @ B_test
                v.check_correctness(function.name, before=(A_test, B_test, C_test), after=(A_test, B_test, C_ref), tolerance=tolerance)
            if file_check_fn:
                file_check_fn(v)

    def test_matmul_last_major_vectorized_cache(self) -> None:
        test_name = 'test_matmul_last_major_vectorized_cache'
        M = 256
        N = 256
        K = 256
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K), layout=Array.Layout.LAST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N), layout=Array.Layout.LAST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N), layout=Array.Layout.LAST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii = schedule.split(i, 16)
        jj = schedule.split(j, 32)
        kk = schedule.split(k, 64)
        order = [j, k, i, kk, jj, ii]
        schedule.reorder(order)
        plan = schedule.create_plan()
        BB = plan.cache(B, index=kk, vectorize=True, layout=Array.Layout.LAST_MAJOR)
        CC = plan.cache(C, index=jj, vectorize=True, layout=Array.Layout.LAST_MAJOR)
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        self._verify_matrix_multiplication_function(function, package, test_name)

    def _verify_convolution_function(self, function: 'accera.Function', package: Package, package_name: str, buffer_padding: List[int], conv_padding: List[int], stride: List[int]) -> None:
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        row_stride, column_stride = stride
        channel_padding, row_padding, column_padding = conv_padding
        channel_buffer_padding, row_buffer_padding, column_buffer_padding = buffer_padding

        def naive_convolution_ref(input, kernel, output):
            input_channels, input_rows, input_columns = input.shape
            out_filters, output_rows, output_columns = output.shape
            _, _, kernel_rows, kernel_columns = kernel.shape
            output_ref = output.copy()
            for out_f in range(out_filters):
                for out_r in range(output_rows - 2 * row_buffer_padding):
                    for out_c in range(output_columns - 2 * column_buffer_padding):
                        for in_ch in range(input_channels):
                            for k_r in range(kernel_rows):
                                for k_c in range(kernel_columns):
                                    in_r = out_r * row_stride + k_r - row_padding
                                    in_c = out_c * column_stride + k_c - column_padding
                                    output_ref[out_f, out_r + row_buffer_padding, out_c + column_buffer_padding] += input[in_ch, in_r + row_buffer_padding, in_c + column_buffer_padding] * kernel[out_f, in_ch, k_r, k_c]
            return output_ref
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(name=package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir)
            Input_test, Kernel_test, Output_test = (np.random.random(p.shape).astype(np.float32) for p in function.args)
            Output_ref = naive_convolution_ref(Input_test, Kernel_test, Output_test)
            v.check_correctness(function.name, before=(Input_test, Kernel_test, Output_test), after=(Input_test, Kernel_test, Output_ref))

    def _multicache_matmul_common(self, M, N, K, name_suffix, jjj_split=16) -> None:
        import accera as acc
        A = acc.Array(role=acc.Role.INPUT, shape=(M, K))
        B = acc.Array(role=acc.Role.INPUT, shape=(K, N))
        C = acc.Array(role=acc.Role.INPUT_OUTPUT, shape=(M, N))
        nest = acc.Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        jj = schedule.split(j, 128)
        kk = schedule.split(k, 256)
        kkk = schedule.split(kk, 4)
        jjj = schedule.split(jj, jjj_split)
        jjjj = schedule.split(jjj, 8)
        ii = schedule.split(i, 6)
        schedule.reorder(j, k, i, jj, kk, kkk, ii, jjj, jjjj)
        plan = schedule.create_plan()
        plan.cache(B, index=kk, trigger_index=jj)
        plan.cache(C, index=ii)
        plan.unroll(jjj)
        plan.unroll(ii)
        plan.vectorize(jjjj)
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=f'multicache_matmul_{name_suffix}')
        self._verify_matrix_multiplication_function(function, package, f'multicache_matmul_{name_suffix}')

    def test_multicache_matmul_no_boundary(self) -> None:
        self._multicache_matmul_common(1020, 1024, 1024, 'no_boundary')

    def test_multicache_matmul_all_boundary(self) -> None:
        self._multicache_matmul_common(1023, 1023, 1023, 'all_boundary')

    def test_multicache_matmul_internal_boundary(self) -> None:
        self._multicache_matmul_common(1020, 1024, 1024, 'internal_boundary', jjj_split=24)

    def _hierarchical_cache_matmul_common(self, M, N, K, A_cache_infos=[], B_cache_infos=[], C_cache_infos=[], force_boundary_conditions=False, cache_by_level=True) -> None:
        import accera as acc
        A = acc.Array(role=acc.Role.INPUT, shape=(M, K))
        B = acc.Array(role=acc.Role.INPUT, shape=(K, N))
        C = acc.Array(role=acc.Role.INPUT_OUTPUT, shape=(M, N))
        nest = acc.Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        if force_boundary_conditions:
            jj = schedule.split(j, 127)
            kk = schedule.split(k, 251)
            kkk = schedule.split(kk, 11)
            jjj = schedule.split(jj, 17)
            jjjj = schedule.split(jjj, 7)
            ii = schedule.split(i, 5)
        else:
            jj = schedule.split(j, 128)
            kk = schedule.split(k, 256)
            kkk = schedule.split(kk, 4)
            jjj = schedule.split(jj, 16)
            jjjj = schedule.split(jjj, 8)
            ii = schedule.split(i, 6)
        order = [j, k, i, jj, kk, kkk, ii, jjj, jjjj]
        schedule.reorder(order)
        plan = schedule.create_plan()
        current_A_caches = [A]
        current_B_caches = [B]
        current_C_caches = [C]
        for cache_level, cache_trigger_level, layout in A_cache_infos:
            prev_cache = current_A_caches[len(current_A_caches) - 1]
            if cache_by_level:
                new_cache = plan.cache(prev_cache, level=cache_level, trigger_level=cache_trigger_level, layout=layout)
            else:
                cache_index = order[-cache_level]
                trigger_index = order[-cache_trigger_level]
                new_cache = plan.cache(prev_cache, index=cache_index, trigger_index=trigger_index, layout=layout)
            current_A_caches.append(new_cache)
        for cache_level, cache_trigger_level, layout in B_cache_infos:
            prev_cache = current_B_caches[len(current_B_caches) - 1]
            if cache_by_level:
                new_cache = plan.cache(prev_cache, level=cache_level, trigger_level=cache_trigger_level, layout=layout)
            else:
                cache_index = order[-cache_level]
                trigger_index = order[-cache_trigger_level]
                new_cache = plan.cache(prev_cache, index=cache_index, trigger_index=trigger_index, layout=layout)
            current_B_caches.append(new_cache)
        for cache_level, layout in C_cache_infos:
            prev_cache = current_C_caches[len(current_C_caches) - 1]
            if cache_by_level:
                new_cache = plan.cache(prev_cache, level=cache_level, layout=layout)
            else:
                cache_index = order[-cache_level]
                new_cache = plan.cache(prev_cache, index=cache_index, layout=layout)
            current_C_caches.append(new_cache)
        return (plan, (A, B, C))

    def test_hierarchical_cache_matmul_2_caches_simple_boundaries_cache_by_index(self) -> None:
        import accera as acc
        M = 1024
        N = 1024
        K = 1024
        a_caches = [(5, 7, acc.Array.Layout.FIRST_MAJOR), (3, 5, acc.Array.Layout.LAST_MAJOR)]
        b_caches = [(4, 6, acc.Array.Layout.FIRST_MAJOR), (2, 4, acc.Array.Layout.LAST_MAJOR)]
        c_caches = [(8, acc.Array.Layout.LAST_MAJOR), (6, acc.Array.Layout.FIRST_MAJOR)]
        package = Package()
        plan, args = self._hierarchical_cache_matmul_common(M, N, K, A_cache_infos=a_caches, B_cache_infos=b_caches, C_cache_infos=c_caches, force_boundary_conditions=False, cache_by_level=False)
        function = package.add(plan, args=args, base_name=f'hierarchical_cache_matmul_2_caches_simple_index')
        self._verify_matrix_multiplication_function(function, package, f'hierarchical_cache_matmul_2_caches_simple_index')

    def test_hierarchical_cache_matmul_2_caches_simple_boundaries(self) -> None:
        import accera as acc
        M = 1024
        N = 1024
        K = 1024
        a_caches = [(5, 7, acc.Array.Layout.FIRST_MAJOR), (3, 5, acc.Array.Layout.LAST_MAJOR)]
        b_caches = [(4, 6, acc.Array.Layout.FIRST_MAJOR), (2, 4, acc.Array.Layout.LAST_MAJOR)]
        c_caches = [(8, acc.Array.Layout.LAST_MAJOR), (6, acc.Array.Layout.FIRST_MAJOR)]
        package = Package()
        plan, args = self._hierarchical_cache_matmul_common(M, N, K, A_cache_infos=a_caches, B_cache_infos=b_caches, C_cache_infos=c_caches, force_boundary_conditions=False)
        function = package.add(plan, args=args, base_name=f'hierarchical_cache_matmul_2_caches_simple')
        self._verify_matrix_multiplication_function(function, package, f'hierarchical_cache_matmul_2_caches_simple')

    def test_hierarchical_cache_matmul_2_caches_complicated_boundaries(self) -> None:
        import accera as acc
        M = 1024
        N = 1024
        K = 1024
        a_caches = [(5, 7, acc.Array.Layout.FIRST_MAJOR), (3, 5, acc.Array.Layout.LAST_MAJOR)]
        b_caches = [(4, 6, acc.Array.Layout.FIRST_MAJOR), (2, 4, acc.Array.Layout.LAST_MAJOR)]
        c_caches = [(8, acc.Array.Layout.LAST_MAJOR), (6, acc.Array.Layout.FIRST_MAJOR)]
        package = Package()
        plan, args = self._hierarchical_cache_matmul_common(M, N, K, A_cache_infos=a_caches, B_cache_infos=b_caches, C_cache_infos=c_caches, force_boundary_conditions=True)
        function = package.add(plan, args=args, base_name=f'hierarchical_cache_matmul_2_caches_complicated')
        self._verify_matrix_multiplication_function(function, package, f'hierarchical_cache_matmul_2_caches_complicated')

    def test_hierarchical_cache_matmul_3_caches_simple_boundaries(self) -> None:
        import accera as acc
        M = 1024
        N = 1024
        K = 1024
        a_caches = [(5, 7, acc.Array.Layout.FIRST_MAJOR), (4, 5, acc.Array.Layout.LAST_MAJOR), (3, 3, acc.Array.Layout.FIRST_MAJOR)]
        b_caches = [(5, 6, acc.Array.Layout.FIRST_MAJOR), (3, 5, acc.Array.Layout.LAST_MAJOR), (2, 3, acc.Array.Layout.FIRST_MAJOR)]
        c_caches = [(8, acc.Array.Layout.LAST_MAJOR), (6, acc.Array.Layout.FIRST_MAJOR), (3, acc.Array.Layout.LAST_MAJOR)]
        package = Package()
        plan, args = self._hierarchical_cache_matmul_common(M, N, K, A_cache_infos=a_caches, B_cache_infos=b_caches, C_cache_infos=c_caches, force_boundary_conditions=False)
        function = package.add(plan, args=args, base_name=f'hierarchical_cache_matmul_3_caches_simple')
        self._verify_matrix_multiplication_function(function, package, f'hierarchical_cache_matmul_3_caches_simple')

    def test_hierarchical_cache_matmul_3_caches_complicated_boundaries(self) -> None:
        import accera as acc
        M = 1024
        N = 1024
        K = 1024
        a_caches = [(5, 7, acc.Array.Layout.FIRST_MAJOR), (4, 5, acc.Array.Layout.LAST_MAJOR), (3, 3, acc.Array.Layout.FIRST_MAJOR)]
        b_caches = [(5, 6, acc.Array.Layout.FIRST_MAJOR), (3, 5, acc.Array.Layout.LAST_MAJOR), (2, 3, acc.Array.Layout.FIRST_MAJOR)]
        c_caches = [(8, acc.Array.Layout.LAST_MAJOR), (6, acc.Array.Layout.FIRST_MAJOR), (3, acc.Array.Layout.LAST_MAJOR)]
        package = Package()
        plan, args = self._hierarchical_cache_matmul_common(M, N, K, A_cache_infos=a_caches, B_cache_infos=b_caches, C_cache_infos=c_caches, force_boundary_conditions=True)
        function = package.add(plan, args=args, base_name=f'hierarchical_cache_matmul_3_caches_complicated')
        self._verify_matrix_multiplication_function(function, package, f'hierarchical_cache_matmul_3_caches_complicated')

    def test_hierarchical_cache_parameterized(self) -> None:
        import accera as acc
        M = 1024
        N = 1024
        K = 1024
        a_level_1, a_level_2, a_trigger_1, a_trigger_2 = acc.create_parameters()
        b_level_1, b_level_2, b_trigger_1, b_trigger_2 = acc.create_parameters()
        c_level_1, c_level_2 = acc.create_parameters()
        a_caches = [(a_level_1, a_trigger_1, acc.Array.Layout.FIRST_MAJOR), (a_level_2, a_trigger_2, acc.Array.Layout.LAST_MAJOR)]
        b_caches = [(b_level_1, b_trigger_1, acc.Array.Layout.FIRST_MAJOR), (b_level_2, b_trigger_2, acc.Array.Layout.LAST_MAJOR)]
        c_caches = [(c_level_1, acc.Array.Layout.FIRST_MAJOR), (c_level_2, acc.Array.Layout.LAST_MAJOR)]
        package = Package()
        plan, args = self._hierarchical_cache_matmul_common(M, N, K, A_cache_infos=a_caches, B_cache_infos=b_caches, C_cache_infos=c_caches)
        function = package.add(plan, args=args, parameters={a_level_1: 5, a_trigger_1: 7, a_level_2: 3, a_trigger_2: 5, b_level_1: 5, b_trigger_1: 6, b_level_2: 3, b_trigger_2: 5, c_level_1: 8, c_level_2: 6}, base_name=f'parameterized_hierarchical_cache_matmul')
        self._verify_matrix_multiplication_function(function, package, f'parameterized_hierarchical_cache_matmul')

    def _max_element_cache_matmul_common(self, M, N, K, A_cache_infos=[], B_cache_infos=[], C_cache_infos=[], force_boundary_conditions=False) -> None:
        import accera as acc
        A = acc.Array(role=acc.Role.INPUT, shape=(M, K))
        B = acc.Array(role=acc.Role.INPUT, shape=(K, N))
        C = acc.Array(role=acc.Role.INPUT_OUTPUT, shape=(M, N))
        nest = acc.Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        if force_boundary_conditions:
            jj = schedule.split(j, 127)
            kk = schedule.split(k, 251)
            kkk = schedule.split(kk, 11)
            jjj = schedule.split(jj, 17)
            jjjj = schedule.split(jjj, 7)
            ii = schedule.split(i, 5)
        else:
            jj = schedule.split(j, 128)
            kk = schedule.split(k, 256)
            kkk = schedule.split(kk, 4)
            jjj = schedule.split(jj, 16)
            jjjj = schedule.split(jjj, 8)
            ii = schedule.split(i, 6)
        order = [j, k, i, jj, kk, kkk, ii, jjj, jjjj]
        schedule.reorder(order)
        plan = schedule.create_plan()
        current_A_caches = [A]
        current_B_caches = [B]
        current_C_caches = [C]
        for cache_budget, layout in A_cache_infos:
            prev_cache = current_A_caches[len(current_A_caches) - 1]
            new_cache = plan.cache(prev_cache, max_elements=cache_budget, layout=layout)
            current_A_caches.append(new_cache)
        for cache_budget, layout in B_cache_infos:
            prev_cache = current_B_caches[len(current_B_caches) - 1]
            new_cache = plan.cache(prev_cache, max_elements=cache_budget, layout=layout)
            current_B_caches.append(new_cache)
        for cache_budget, layout in C_cache_infos:
            prev_cache = current_C_caches[len(current_C_caches) - 1]
            new_cache = plan.cache(prev_cache, max_elements=cache_budget, layout=layout)
            current_C_caches.append(new_cache)
        return (plan, (A, B, C))

    def test_simple_single_budget_cache(self) -> None:
        import accera as acc
        M = 1024
        N = 1024
        K = 1024
        a_caches = [(128, acc.Array.Layout.LAST_MAJOR)]
        b_caches = []
        c_caches = []
        package = Package()
        plan, args = self._max_element_cache_matmul_common(M, N, K, A_cache_infos=a_caches, B_cache_infos=b_caches, C_cache_infos=c_caches)
        function = package.add(plan, args=args, base_name=f'test_simple_single_budget_cache')
        self._verify_matrix_multiplication_function(function, package, f'test_simple_single_budget_cache')

    def test_multiple_single_budget_caches(self) -> None:
        import accera as acc
        M = 1024
        N = 1024
        K = 1024
        a_caches = [(128, acc.Array.Layout.LAST_MAJOR)]
        b_caches = [(K * N // 128, acc.Array.Layout.FIRST_MAJOR)]
        c_caches = [(6 * 16, acc.Array.Layout.FIRST_MAJOR)]
        package = Package()
        plan, args = self._max_element_cache_matmul_common(M, N, K, A_cache_infos=a_caches, B_cache_infos=b_caches, C_cache_infos=c_caches)
        function = package.add(plan, args=args, base_name=f'test_multiple_single_budget_caches')
        self._verify_matrix_multiplication_function(function, package, f'test_multiple_single_budget_caches')

    def test_hierarchical_budget_caches(self) -> None:
        import accera as acc
        M = 1024
        N = 1024
        K = 1024
        a_caches = [(128, acc.Array.Layout.LAST_MAJOR), (6, acc.Array.Layout.FIRST_MAJOR)]
        b_caches = [(K * N // 128, acc.Array.Layout.FIRST_MAJOR), (K * N // (128 * 256), acc.Array.Layout.LAST_MAJOR)]
        c_caches = [(6 * 128, acc.Array.Layout.FIRST_MAJOR), (6 * 16, acc.Array.Layout.LAST_MAJOR)]
        package = Package()
        plan, args = self._max_element_cache_matmul_common(M, N, K, A_cache_infos=a_caches, B_cache_infos=b_caches, C_cache_infos=c_caches)
        function = package.add(plan, args=args, base_name=f'test_hierarchical_budget_caches')
        self._verify_matrix_multiplication_function(function, package, f'test_hierarchical_budget_caches')

    def test_hierarchical_budget_caches_boundary_conditions(self) -> None:
        import accera as acc
        M = 1024
        N = 1024
        K = 1024
        a_caches = [(128, acc.Array.Layout.LAST_MAJOR), (6, acc.Array.Layout.FIRST_MAJOR)]
        b_caches = [(K * N // 128, acc.Array.Layout.FIRST_MAJOR), (K * N // (128 * 256), acc.Array.Layout.LAST_MAJOR)]
        c_caches = [(6 * 128, acc.Array.Layout.FIRST_MAJOR), (6 * 16, acc.Array.Layout.LAST_MAJOR)]
        package = Package()
        plan, args = self._max_element_cache_matmul_common(M, N, K, A_cache_infos=a_caches, B_cache_infos=b_caches, C_cache_infos=c_caches, force_boundary_conditions=True)
        function = package.add(plan, args=args, base_name=f'test_hierarchical_budget_caches_boundary_conditions')
        self._verify_matrix_multiplication_function(function, package, f'test_hierarchical_budget_caches_boundary_conditions')

    def test_small_budget_cache(self) -> None:
        import accera as acc
        M = 1024
        N = 1024
        K = 1024
        a_caches = [(1, acc.Array.Layout.LAST_MAJOR)]
        b_caches = [(1, acc.Array.Layout.LAST_MAJOR)]
        c_caches = [(1, acc.Array.Layout.FIRST_MAJOR)]
        package = Package()
        plan, args = self._max_element_cache_matmul_common(M, N, K, A_cache_infos=a_caches, B_cache_infos=b_caches, C_cache_infos=c_caches)
        function = package.add(plan, args=args, base_name=f'test_small_budget_cache')
        self._verify_matrix_multiplication_function(function, package, f'test_small_budget_cache')

    def test_max_budget_cache(self) -> None:
        import accera as acc
        M = 1024
        N = 1024
        K = 1024
        a_caches = [(M * K, acc.Array.Layout.LAST_MAJOR)]
        b_caches = [(K * N, acc.Array.Layout.FIRST_MAJOR)]
        c_caches = [(M * N, acc.Array.Layout.FIRST_MAJOR)]
        package = Package()
        plan, args = self._max_element_cache_matmul_common(M, N, K, A_cache_infos=a_caches, B_cache_infos=b_caches, C_cache_infos=c_caches)
        function = package.add(plan, args=args, base_name=f'test_max_budget_cache')
        self._verify_matrix_multiplication_function(function, package, f'test_max_budget_cache')

    def test_overmax_budget_cache(self) -> None:
        import accera as acc
        M = 1024
        N = 1024
        K = 1024
        a_caches = [(2 * M * K, acc.Array.Layout.LAST_MAJOR)]
        b_caches = [(2 * K * N, acc.Array.Layout.FIRST_MAJOR)]
        c_caches = [(2 * M * N, acc.Array.Layout.FIRST_MAJOR)]
        package = Package()
        plan, args = self._max_element_cache_matmul_common(M, N, K, A_cache_infos=a_caches, B_cache_infos=b_caches, C_cache_infos=c_caches)
        function = package.add(plan, args=args, base_name=f'test_overmax_budget_cache')
        self._verify_matrix_multiplication_function(function, package, f'test_overmax_budget_cache')

    def test_boundary_differently_shaped_budget_cache(self) -> None:
        import accera as acc
        M = 1024
        N = 1024
        K = 1024
        a_caches = [(5 * 256, acc.Array.Layout.LAST_MAJOR)]
        b_caches = []
        c_caches = []
        package = Package()
        plan, args = self._max_element_cache_matmul_common(M, N, K, A_cache_infos=a_caches, B_cache_infos=b_caches, C_cache_infos=c_caches)
        function = package.add(plan, args=args, base_name=f'test_boundary_differently_shaped_budget_cache')
        self._verify_matrix_multiplication_function(function, package, f'test_boundary_differently_shaped_budget_cache')

    def test_gpu_vec_add(self):
        from accera import Array, Nest, Package, ScalarType, Target
        N = 2 ** 16
        block_x = 256
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N,))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N,))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(N,))
        nest = Nest(shape=(N,))
        i, = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i] = A[i] + B[i]
        schedule = nest.create_schedule()
        ii = schedule.split(i, block_x)
        schedule.reorder(i, ii)
        target = Target(category=Target.Category.GPU, runtime=Target.Runtime.CUDA)
        plan = schedule.create_plan(target)
        plan.bind(mapping={i: target.GridUnit.BLOCK_X, ii: target.GridUnit.THREAD_X})
        test_name = 'test_gpu_vec_add'
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(name=test_name, format=Package.Format.MLIR | Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            if CUDA_AVAILABLE:
                before = [np.random.rand(*p.shape).astype(np.float32) for p in function.args]
                after = [before[0], before[1]] + [before[0] + before[1]]
                v.check_correctness(function.name, before=before, after=after)

    def _test_gpu_vec_add_boundary(self, N, splits, test_name):
        from accera import Array, Nest, Package, ScalarType, Target
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N,))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N,))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(N,))
        nest = Nest(shape=(N,))
        i, = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i] = A[i] + B[i]
        schedule = nest.create_schedule()
        indices = [i]
        for split in splits:
            indices.append(schedule.split(indices[-1], split))
        schedule.reorder(*indices)
        target = Target(Target.Model.AMD_MI100)
        if CUDA_AVAILABLE:
            target = Target(Target.Model.NVIDIA_RTX_A6000)
        plan = schedule.create_plan(target)
        plan.bind(mapping={indices[0]: target.GridUnit.BLOCK_X, indices[1]: target.GridUnit.THREAD_X})
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir, file_list=[f'{test_name}.cu', f'{test_name}.hat']) as v:
            package.build(name=test_name, format=Package.Format.MLIR_VERBOSE | Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            checker = v.file_checker(f'*_LoopNestToValueFunc.mlir')
            checker.check_label('accv.func nested @' + test_name)
            pairs = zip([N] + list(splits), splits)
            has_bad_split = any((c % n for c, n in pairs))
            if has_bad_split:
                checker.check('affine.if')
            else:
                checker.check_not('affine.if')
            checker.run()
            if CUDA_AVAILABLE or ROCM_AVAILABLE:
                before = [np.random.rand(*p.shape).astype(np.float32) for p in function.args]
                after = [before[0], before[1]] + [before[0] + before[1]]
                v.check_correctness(function.name, before=before, after=after)

    def _test_cpu_vec_add_boundary(self, N, splits, test_name):
        from accera import Array, Nest, Package, ScalarType, Target
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N,))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N,))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(N,))
        nest = Nest(shape=(N,))
        i, = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i] = A[i] + B[i]
        schedule = nest.create_schedule()
        indices = [i]
        for split in splits:
            indices.append(schedule.split(indices[-1], split))
        schedule.reorder(*indices)
        target = Target(category=Target.Category.CPU)
        plan = schedule.create_plan(target)
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(name=test_name, format=Package.Format.MLIR | Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            before = [np.random.rand(*p.shape).astype(np.float32) for p in function.args]
            after = [before[0], before[1]] + [before[0] + before[1]]
            v.check_correctness(function.name, before=before, after=after)

    def test_gpu_vec_add_gpu_boundary_nosplit(self):
        self._test_gpu_vec_add_boundary(1024, [512], inspect.currentframe().f_code.co_name)

    def test_gpu_vec_add_gpu_boundary_split_small(self):
        self._test_gpu_vec_add_boundary(128, [512], inspect.currentframe().f_code.co_name)

    def test_gpu_vec_add_gpu_boundary_split(self):
        self._test_gpu_vec_add_boundary(1280, [512], inspect.currentframe().f_code.co_name)

    def test_gpu_vec_add_gpu_boundary_split_cpuonly(self):
        self._test_cpu_vec_add_boundary(1280, [512], inspect.currentframe().f_code.co_name)

    def test_gpu_vec_add_gpu_boundary_2_splits(self):
        self._test_gpu_vec_add_boundary(1280, [512, 64], inspect.currentframe().f_code.co_name)

    def test_gpu_vec_add_gpu_boundary_2_splits_cpuonly(self):
        self._test_cpu_vec_add_boundary(1280, [512, 64], inspect.currentframe().f_code.co_name)

    def _add_cuda_copy_kernel(self, package, N, block_x, block_y, target, basename='cuda_copy_kernel'):
        from accera import Array, Nest, ScalarType
        from accera._lang_python._lang import _MemorySpace
        In = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N, N))
        Out = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(N, N))
        nest = Nest(shape=(N, N))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _():
            Out[i, j] = In[i, j]
        schedule = nest.create_schedule()
        ii, jj = schedule.tile({i: block_x, j: block_y})
        schedule.reorder(i, j, ii, jj)
        plan = schedule.create_plan(target=target)
        plan.bind(mapping={i: target.GridUnit.BLOCK_X, j: target.GridUnit.BLOCK_Y, ii: target.GridUnit.THREAD_X, jj: target.GridUnit.THREAD_Y})
        plan.cache(In, index=ii, location=_MemorySpace.SHARED, layout=Array.Layout.LAST_MAJOR)
        function = package.add(plan, args=(In, Out), base_name=f'{basename}_{N}_{block_x}_{block_y}')
        return function

    def test_cuda_module_output(self) -> None:
        from accera import Package, Target
        N = 2048
        block_x = 16
        block_y = block_x
        target = Target(Target.Model.NVIDIA_V100)
        test_name = 'test_cuda_module_output'
        package = Package()
        function = self._add_cuda_copy_kernel(package, N, block_x, block_y, target, test_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir, file_list=[f'{test_name}.cu', f'{test_name}.hat']) as v:
            package.build(name=test_name, format=Package.Format.MLIR | Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            if CUDA_AVAILABLE:
                Input_test, Output_test = (np.random.uniform(-1, 1, p.shape).astype(np.float32) for p in function.args)
                Input_ref = Output_ref = Input_test
                v.check_correctness(function.name, before=(Input_test, Output_test), after=(Input_ref, Output_ref))

    def test_cuda_multiple_funcs(self) -> None:
        from accera import Package, Target
        Ns = [1024, 2048]
        block_x = 16
        block_y = block_x
        target = Target(Target.Model.NVIDIA_V100)
        test_name = 'test_cuda_multiple_funcs'
        package = Package()
        fs = [self._add_cuda_copy_kernel(package, n, block_x, block_y, target, test_name) for n in Ns]
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir, file_list=[f'{test_name}.cu', f'{test_name}.hat']) as v:
            package.build(name=test_name, format=Package.Format.MLIR | Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            if CUDA_AVAILABLE:
                for function in fs:
                    Input_test, Output_test = (np.random.uniform(-1, 1, p.shape).astype(np.float32) for p in function.args)
                    Input_ref = Output_ref = Input_test
                    v.check_correctness(function.name, before=(Input_test, Output_test), after=(Input_ref, Output_ref))

    def _add_rocm_copy_kernel(self, package, N, block_x, block_y, target, basename='rocm_copy_kernel'):
        from accera import Array, Nest, ScalarType
        from accera._lang_python._lang import _MemorySpace
        In = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N, N))
        Out = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(N, N))
        nest = Nest(shape=(N, N))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _():
            Out[i, j] = In[i, j]
        schedule = nest.create_schedule()
        ii, jj = schedule.tile({i: block_x, j: block_y})
        schedule.reorder(i, j, ii, jj)
        plan = schedule.create_plan(target=target)
        plan.bind(mapping={i: target.GridUnit.BLOCK_X, j: target.GridUnit.BLOCK_Y, ii: target.GridUnit.THREAD_X, jj: target.GridUnit.THREAD_Y})
        plan.cache(In, index=ii, location=_MemorySpace.SHARED, layout=Array.Layout.LAST_MAJOR)
        function = package.add(plan, args=(In, Out), base_name=f'{basename}_{N}_{block_x}_{block_y}')
        return function

    def test_rocm_module_output(self) -> None:
        from accera import Package, Target
        N = 32
        block_x = 16
        block_y = block_x
        target = Target(Target.Model.AMD_MI100)
        test_name = 'test_rocm_module_output'
        package = Package()
        function = self._add_rocm_copy_kernel(package, N, block_x, block_y, target, test_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir, file_list=[f'{test_name}.cu', f'{test_name}.hat']) as v:
            package.build(name=test_name, format=Package.Format.MLIR | Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            if ROCM_AVAILABLE:
                before = [np.random.rand(*p.shape).astype(np.float32) for p in function.args]
                after = [before[0], before[0]]
                v.check_correctness(function.name, before=before, after=after)

    def test_rocm_multiple_funcs(self) -> None:
        from accera import Package, Target
        Ns = [1024, 2048]
        block_x = 16
        block_y = block_x
        target = Target(Target.Model.AMD_MI100)
        test_name = 'test_rocm_multiple_funcs'
        package = Package()
        fs = [self._add_rocm_copy_kernel(package, n, block_x, block_y, target, test_name) for n in Ns]
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir, file_list=[f'{test_name}.cu', f'{test_name}.hat']) as v:
            package.build(name=test_name, format=Package.Format.MLIR | Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            if ROCM_AVAILABLE:
                for function in fs:
                    Input_test, Output_test = (np.random.uniform(-1, 1, p.shape).astype(np.float32) for p in function.args)
                    Input_ref = Output_ref = Input_test
                    v.check_correctness(function.name, before=(Input_test, Output_test), after=(Input_ref, Output_ref))

    def _gpu_cache(self, M, N, K, m_tile_size, n_tile_size, k_tile_size, test_name, double_buffer=False, double_buffer_location=Constants.AUTO) -> None:
        from accera import Array, Nest, Package, ScalarType, Target
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N), layout=Array.Layout.FIRST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: m_tile_size, j: n_tile_size, k: k_tile_size})
        schedule.reorder(i, j, k, ii, jj, kk)
        target = Target(Target.Model.AMD_MI100)
        plan = schedule.create_plan(target=target)
        plan.bind(mapping={i: target.GridUnit.BLOCK_X, j: target.GridUnit.BLOCK_Y, ii: target.GridUnit.THREAD_X, jj: target.GridUnit.THREAD_Y})
        plan.cache(A, index=ii, double_buffer=double_buffer, location=_MemorySpace.SHARED, double_buffer_location=double_buffer_location, layout=Array.Layout.FIRST_MAJOR)
        plan.cache(B, index=ii, double_buffer=double_buffer, location=_MemorySpace.SHARED, double_buffer_location=double_buffer_location, layout=Array.Layout.FIRST_MAJOR)
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        self._verify_matrix_multiplication_function(function, package, test_name, check_correctness=ROCM_AVAILABLE, file_list=[f'{test_name}.cu', f'{test_name}.hat'], package_format=Package.Format.DEFAULT)

    def test_gpu_cache_simple(self) -> None:
        self._gpu_cache(1024, 1024, 1024, 16, 16, 32, 'test_gpu_cache_simple')

    def test_gpu_cache_double_buffering(self) -> None:
        self._gpu_cache(2560, 1536, 2048, 16, 16, 32, 'test_gpu_cache_double_buffering', True)

    def test_gpu_cache_double_buffering_trigger_index(self) -> None:
        from accera import Array, Nest, Package, ScalarType, Target
        from accera._lang_python._lang import _MemorySpace
        M = 2560
        N = 1536
        K = 2048
        block_x = 16
        block_y = block_x
        k_outer_tile_size = 512
        k_inner_tile_size = 32
        m_tile_size = block_x
        n_tile_size = block_y
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N), layout=Array.Layout.FIRST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: m_tile_size, j: n_tile_size, k: k_outer_tile_size})
        kkk = schedule.split(kk, k_inner_tile_size)
        schedule.reorder(i, j, k, kk, ii, jj, kkk)
        target = Target(Target.Model.AMD_MI100)
        plan = schedule.create_plan(target=target)
        plan.bind(mapping={i: target.GridUnit.BLOCK_X, j: target.GridUnit.BLOCK_Y, ii: target.GridUnit.THREAD_X, jj: target.GridUnit.THREAD_Y})
        plan.cache(A, index=ii, trigger_index=kk, double_buffer=True, location=_MemorySpace.SHARED, layout=Array.Layout.FIRST_MAJOR)
        plan.cache(B, index=ii, trigger_index=kk, double_buffer=True, location=_MemorySpace.SHARED, layout=Array.Layout.FIRST_MAJOR)
        test_name = 'test_gpu_cache_double_buffering_trigger_index'
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        self._verify_matrix_multiplication_function(function, package, test_name, check_correctness=ROCM_AVAILABLE, file_list=[f'{test_name}.cu', f'{test_name}.hat'], package_format=Package.Format.DEFAULT)

    def test_gpu_cache_double_buffering_mem_space(self) -> None:
        self._gpu_cache(2560, 1536, 2048, 16, 16, 32, 'test_gpu_cache_double_buffering_mem_space', True, _MemorySpace.PRIVATE)

    def test_cpu_cache_double_buffering_trigger_index(self) -> None:
        from accera import Array, Nest, Package, ScalarType
        M = 1024
        N = 1024
        K = 1024
        m_tile_size = 16
        n_tile_size = 16
        k_outer_tile_size = 256
        k_inner_tile_size = 32
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N), layout=Array.Layout.FIRST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: m_tile_size, j: n_tile_size, k: k_outer_tile_size})
        kkk = schedule.split(kk, k_inner_tile_size)
        schedule.reorder(i, j, k, kk, ii, jj, kkk)
        plan = schedule.create_plan()
        plan.cache(A, index=ii, trigger_index=kk, double_buffer=True, layout=Array.Layout.FIRST_MAJOR)
        plan.cache(B, index=ii, trigger_index=kk, double_buffer=True, layout=Array.Layout.FIRST_MAJOR)
        test_name = 'test_cpu_cache_double_buffering_trigger_index'
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        self._verify_matrix_multiplication_function(function, package, test_name)

    def _matmul_cache_element_type_common(self, test_name, array_element_types, cache_element_types, check_correctness=True) -> None:
        M = 256
        N = 256
        K = 256
        A = Array(role=Role.INPUT, element_type=array_element_types[0], shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=array_element_types[1], shape=(K, N), layout=Array.Layout.FIRST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=array_element_types[2], shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii = schedule.split(i, 16)
        jj = schedule.split(j, 32)
        kk = schedule.split(k, 64)
        order = [i, j, k, ii, jj, kk]
        schedule.reorder(order)
        plan = schedule.create_plan()
        plan.cache(A, index=ii, element_type=cache_element_types[0])
        plan.cache(B, index=ii, element_type=cache_element_types[1])
        plan.cache(C, index=ii, element_type=cache_element_types[2])
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        self._verify_matrix_multiplication_function(function, package, test_name, check_correctness=check_correctness)

    def test_signextend_int16_matmul_vpmaddwd(self):
        from accera import AllocateFlags, create_dimensions
        test_name = 'test_signextend_int16_matmul_vpmaddwd'

        def inout_array(arr: Array):
            return Array(role=Role.INPUT_OUTPUT, element_type=arr.element_type, shape=arr.shape)
        M = 240
        N = 256
        K = 256
        M_tile = 24
        N_tile = 128
        K_tile = 128
        M_kernel_tile = 6
        N_kernel_tile = 16
        N_vector_tile = 8
        K_vector_tile = 2
        A = Array(role=Role.INPUT, element_type=ScalarType.int16, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.uint8, shape=(K, N), layout=Array.Layout.FIRST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.int32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        A_cache = Array(role=Role.TEMP, element_type=ScalarType.int16, shape=(M_tile, K_tile), layout=Array.Layout.FIRST_MAJOR, flags=AllocateFlags.HEAP)
        B_cache = Array(role=Role.TEMP, element_type=ScalarType.uint8, shape=(N_tile // N_kernel_tile, K_tile // K_vector_tile, N_kernel_tile, K_vector_tile), layout=Array.Layout.FIRST_MAJOR, flags=AllocateFlags.HEAP)
        C_cache = Array(role=Role.TEMP, element_type=ScalarType.int32, shape=(M_kernel_tile, N_kernel_tile), layout=Array.Layout.FIRST_MAJOR, flags=AllocateFlags.STACK)
        io_A_cache = inout_array(A_cache)
        io_B_cache = inout_array(B_cache)
        io_C_cache = inout_array(C_cache)
        B_ext = Array(role=Role.TEMP, element_type=ScalarType.int16, shape=(N_kernel_tile, K_vector_tile), layout=Array.Layout.FIRST_MAJOR, flags=AllocateFlags.STACK)
        io_B_ext = inout_array(B_ext)
        m_tile_dim, n_tile_dim, k_tile_dim = create_dimensions()
        m_kernel_dim, n_kernel_dim, k_kernel_dim = create_dimensions()
        i_tile_idx, j_tile_idx, k_tile_idx = create_dimensions()
        i_kernel_idx, j_kernel_idx, k_kernel_idx, i_vector_idx = create_dimensions()
        package = Package()
        mmi_nest = Nest(shape=(n_kernel_dim, k_kernel_dim))
        mmi_j, mmi_k = mmi_nest.get_indices()

        @mmi_nest.iteration_logic
        def _matmul_inner():
            mmi_i = i_vector_idx
            tile_i = i_kernel_idx + mmi_i
            tile_j = j_kernel_idx + mmi_j
            tile_k = k_kernel_idx + mmi_k
            io_C_cache[mmi_i, mmi_j] += io_A_cache[tile_i, tile_k] * io_B_ext[mmi_j, mmi_k]
        mmi_sched = mmi_nest.create_schedule()
        mmi_jj, mmi_kk = mmi_sched.tile(dict(zip([mmi_j, mmi_k], [N_kernel_tile, K_vector_tile])))
        mmi_jjj = mmi_sched.split(mmi_jj, N_vector_tile)
        mmi_sched.reorder(mmi_j, mmi_k, mmi_jj, mmi_jjj, mmi_kk)
        mmi_plan = mmi_sched.create_plan()
        mmi_plan.vectorize(mmi_jjj)
        mmi_fn = package.add(mmi_plan, args=(n_kernel_dim, k_kernel_dim, io_A_cache, io_B_ext, io_C_cache, i_kernel_idx, j_kernel_idx, k_kernel_idx, i_vector_idx), base_name='matmul_kernel', function_opts=INTERNAL_FUNCTION_OPTS)
        bext_nest = Nest((n_kernel_dim, k_kernel_dim))
        bext_j, bext_k = bext_nest.get_indices()

        @bext_nest.iteration_logic
        def _bext():
            tile_j = j_kernel_idx
            tile_k = k_kernel_idx
            io_B_ext[bext_j, bext_k] = io_B_cache[tile_j / N_kernel_tile, tile_k / K_vector_tile, bext_j, bext_k]
        bext_sched = bext_nest.create_schedule()
        bext_jj, bext_kk = bext_sched.tile(dict(zip([bext_j, bext_k], [N_kernel_tile, K_vector_tile])))
        bext_jjj = bext_sched.split(bext_jj, N_vector_tile)
        bext_sched.reorder(bext_j, bext_k, bext_jj, bext_jjj, bext_kk)
        bext_plan = bext_sched.create_plan()
        bext_plan.vectorize(bext_jjj)
        bext_fn = package.add(bext_plan, args=(n_kernel_dim, k_kernel_dim, io_B_cache, io_B_ext, j_kernel_idx, k_kernel_idx), base_name='b_ext_kernel', function_opts=INTERNAL_FUNCTION_OPTS)
        mmo_nest = Nest(shape=(m_kernel_dim, k_tile_dim))
        mmo_i, mmo_k = mmo_nest.get_indices()

        @mmo_nest.iteration_logic
        def _matmul():
            k_kernel_extent = accmin(k_tile_dim - mmo_k, cast(K_vector_tile, ScalarType.index))
            bext_fn(n_kernel_dim, k_kernel_extent, io_B_cache, B_ext, j_kernel_idx, mmo_k)
            mmi_fn(n_kernel_dim, k_kernel_extent, io_A_cache, B_ext, io_C_cache, i_kernel_idx, j_kernel_idx, mmo_k, mmo_i)
        mmo_sched = mmo_nest.create_schedule()
        mmo_ii, mmo_kk = mmo_sched.tile(dict(zip([mmo_i, mmo_k], [M_kernel_tile, K_tile])))
        mmo_kkk = mmo_sched.split(mmo_kk, K_vector_tile)
        mmo_sched.reorder(mmo_k, mmo_i, mmo_kk, mmo_ii, mmo_kkk)
        mmo_plan = mmo_sched.create_plan()
        mmo_plan._erase_loops([mmo_kkk])
        mmo_fn = package.add(mmo_plan, args=(m_kernel_dim, n_kernel_dim, k_tile_dim, io_A_cache, io_B_cache, io_C_cache, i_kernel_idx, j_kernel_idx), base_name='matmul_kernel', function_opts=INTERNAL_FUNCTION_OPTS)
        cci_nest = Nest(shape=(M_kernel_tile, N_kernel_tile))
        cci_i, cci_j = cci_nest.get_indices()

        @cci_nest.iteration_logic
        def _cci():
            io_C_cache[cci_i, cci_j] = 0
        cci_sched = cci_nest.create_schedule()
        cci_plan = cci_sched.create_plan()
        cci_fn = package.add(cci_plan, args=(io_C_cache,), base_name='c_cache_init_kernel', function_opts=INTERNAL_FUNCTION_OPTS)
        ccr_nest = Nest(shape=(m_kernel_dim, n_kernel_dim))
        ccr_i, ccr_j = ccr_nest.get_indices()

        @ccr_nest.iteration_logic
        def _ccr():
            global_i = i_tile_idx + i_kernel_idx + ccr_i
            global_j = j_tile_idx + j_kernel_idx + ccr_j
            C[global_i, global_j] += io_C_cache[ccr_i, ccr_j]
        ccr_sched = ccr_nest.create_schedule()
        ccr_ii, ccr_jj = ccr_sched.tile(dict(zip([ccr_i, ccr_j], [M_kernel_tile, N_kernel_tile])))
        ccr_sched.reorder(ccr_i, ccr_j, ccr_ii, ccr_jj)
        ccr_plan = ccr_sched.create_plan()
        ccr_plan.vectorize(ccr_ii)
        ccr_fn = package.add(ccr_plan, args=(m_kernel_dim, n_kernel_dim, C, io_C_cache, i_tile_idx, j_tile_idx, i_kernel_idx, j_kernel_idx), base_name='c_cache_reduce_kernel', function_opts=INTERNAL_FUNCTION_OPTS)
        pa_nest = Nest(shape=(m_tile_dim, k_tile_dim))
        pa_i, pa_k = pa_nest.get_indices()

        @pa_nest.iteration_logic
        def _pack_a():
            global_i = i_tile_idx + pa_i
            global_k = k_tile_idx + pa_k
            io_A_cache[pa_i, pa_k] = A[global_i, global_k]
        pa_sched = pa_nest.create_schedule()
        pa_ii, pa_kk = pa_sched.tile(dict(zip([pa_i, pa_k], [M_tile, K_tile])))
        pa_sched.reorder(pa_i, pa_k, pa_ii, pa_kk)
        pa_plan = pa_sched.create_plan()
        pa_fn = package.add(pa_plan, args=(m_tile_dim, k_tile_dim, A, io_A_cache, i_tile_idx, k_tile_idx), base_name='pack_a', function_opts=INTERNAL_FUNCTION_OPTS)
        pb_nest = Nest(shape=(n_tile_dim, k_tile_dim))
        pb_j, pb_k = pb_nest.get_indices()

        @pb_nest.iteration_logic
        def _pack_b():
            global_j = j_tile_idx + pb_j
            global_k = k_tile_idx + pb_k
            io_B_cache[pb_j / N_kernel_tile, pb_k / K_vector_tile, pb_j % N_kernel_tile, pb_k % K_vector_tile] = B[global_k, global_j]
        pb_sched = pb_nest.create_schedule()
        pb_jj, pb_kk = pb_sched.tile(dict(zip([pb_j, pb_k], [N_tile, K_tile])))
        pb_jjj, pb_kkk = pb_sched.tile(dict(zip([pb_jj, pb_kk], [N_vector_tile, K_vector_tile])))
        pb_sched.reorder(pb_j, pb_k, pb_jj, pb_kk, pb_jjj, pb_kkk)
        pb_plan = pb_sched.create_plan()
        pb_plan.vectorize(pb_jjj)
        pb_fn = package.add(pb_plan, args=(n_tile_dim, k_tile_dim, B, io_B_cache, j_tile_idx, k_tile_idx), base_name='pack_b', function_opts=INTERNAL_FUNCTION_OPTS)
        compute_kernel_nest = Nest(shape=(1,))

        @compute_kernel_nest.iteration_logic
        def _hack():
            cci_fn(C_cache)
            mmo_fn(m_kernel_dim, n_kernel_dim, k_tile_dim, io_A_cache, io_B_cache, C_cache, i_kernel_idx, j_kernel_idx)
            ccr_fn(m_kernel_dim, n_kernel_dim, C, C_cache, i_tile_idx, j_tile_idx, i_kernel_idx, j_kernel_idx)
        compute_kernel_sched = compute_kernel_nest.create_schedule()
        compute_kernel_plan = compute_kernel_sched.create_plan()
        compute_kernel_fn = package.add(compute_kernel_plan, args=(m_kernel_dim, n_kernel_dim, k_tile_dim, io_A_cache, io_B_cache, C, i_tile_idx, j_tile_idx, k_tile_idx, i_kernel_idx, j_kernel_idx), base_name='compute_kernel_fn', function_opts=INTERNAL_FUNCTION_OPTS)
        tile_nest = Nest(shape=(m_tile_dim, n_tile_dim))
        tile_i, tile_j = tile_nest.get_indices()

        @tile_nest.iteration_logic
        def _tile():
            m_kernel_extent = accmin(m_tile_dim - tile_i, cast(M_kernel_tile, ScalarType.index))
            n_kernel_extent = accmin(n_tile_dim - tile_j, cast(N_kernel_tile, ScalarType.index))
            compute_kernel_fn(m_kernel_extent, n_kernel_extent, k_tile_dim, io_A_cache, io_B_cache, C, i_tile_idx, j_tile_idx, k_tile_idx, tile_i, tile_j)
        tile_sched = tile_nest.create_schedule()
        tile_ii, tile_jj = tile_sched.tile({tile_i: M_tile, tile_j: N_tile})
        tile_iii, tile_jjj = tile_sched.tile({tile_ii: M_kernel_tile, tile_jj: N_kernel_tile})
        tile_sched.reorder(tile_i, tile_j, tile_ii, tile_jj, tile_iii, tile_jjj)
        tile_plan = tile_sched.create_plan()
        tile_plan._erase_loops([tile_iii, tile_jjj])
        tile_fn = package.add(tile_plan, args=(m_tile_dim, n_tile_dim, k_tile_dim, io_A_cache, io_B_cache, C, i_tile_idx, j_tile_idx, k_tile_idx), base_name='tile_fn', function_opts=INTERNAL_FUNCTION_OPTS)
        global_nest = Nest(shape=(M, N, K))
        global_i, global_j, global_k = global_nest.get_indices()

        @global_nest.iteration_logic
        def _tile():
            m_tile_extent = accmin(M - global_i, cast(M_tile, ScalarType.index))
            n_tile_extent = accmin(N - global_j, cast(N_tile, ScalarType.index))
            k_tile_extent = accmin(K - global_k, cast(K_tile, ScalarType.index))
            pa_fn(m_tile_extent, k_tile_extent, A, A_cache, global_i, global_k)
            pb_fn(n_tile_extent, k_tile_extent, B, B_cache, global_j, global_k)
            tile_fn(m_tile_extent, n_tile_extent, k_tile_extent, A_cache, B_cache, C, global_i, global_j, global_k)
        global_sched = global_nest.create_schedule()
        global_ii, global_jj, global_kk = global_sched.tile({global_i: M_tile, global_j: N_tile, global_k: K_tile})
        global_sched.reorder(global_i, global_j, global_k, global_ii, global_jj, global_kk)
        global_plan = global_sched.create_plan()
        global_plan._erase_loops([global_ii, global_jj, global_kk])
        function = package.add(global_plan, args=(A, B, C), base_name=test_name)
        A_test = np.random.random((M, K)).astype(np.int16)
        B_test = np.random.random((K, N)).astype(np.uint8)
        C_test = np.random.random((M, N)).astype(np.int32)
        correctness_check_values = {'pre': (A_test, B_test, C_test), 'post': (A_test, B_test, C_test + A_test @ B_test)}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(test_name, format=Package.Format.DEFAULT | Package.Format.MLIR, mode=Package.Mode.RELEASE, output_dir=output_dir)
            v.check_correctness(function.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    def test_int16_matmul_vpmaddwd(self):
        test_name = 'test_int16_matmul_vpmaddwd'
        M = 240
        N = 256
        K = 256
        A = Array(role=Role.INPUT, element_type=ScalarType.int16, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.int16, shape=(K, N), layout=Array.Layout.FIRST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.int32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: 24, j: 128, k: 128})
        iii, jjj, kkk = schedule.tile({ii: 6, jj: 16, kk: 4})
        jjjj, kkkk = schedule.tile({jjj: 8, kkk: 2})
        schedule.reorder(i, j, k, ii, jj, kk, kkk, iii, jjj, jjjj, kkkk)
        plan = schedule.create_plan()
        plan.cache(A, index=ii, element_type=ScalarType.int16, vectorize=False)
        plan.cache(B, index=jjjj, trigger_index=jj, layout=Array.Layout.LAST_MAJOR, vectorize=False)
        plan.cache(C, iii)
        plan.vectorize(jjjj)
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        A_test = np.random.random((M, K)).astype(np.int16)
        B_test = np.random.random((K, N)).astype(np.int16)
        C_test = np.random.random((M, N)).astype(np.int32)
        correctness_check_values = {'pre': (A_test, B_test, C_test), 'post': (A_test, B_test, C_test + A_test @ B_test)}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(test_name, format=Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            v.check_correctness(function.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    @expectedFailure(FailedReason.INVALID, 'generated x86_64 lib not readable by MacOS arm64 build tools', sys.platform == 'darwin' and platform.machine() == 'arm64')
    def test_int16_matmul_vpmaddwd_16_element_avx512(self):
        test_name = 'test_int16_matmul_vpmaddwd_16_element_avx512'
        M = 240
        N = 256
        K = 256
        A = Array(role=Role.INPUT, element_type=ScalarType.int16, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.int16, shape=(K, N), layout=Array.Layout.FIRST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.int32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: 24, j: 128, k: 128})
        iii, jjj, kkk = schedule.tile({ii: 6, jj: 32, kk: 4})
        jjjj, kkkk = schedule.tile({jjj: 16, kkk: 2})
        schedule.reorder(i, j, k, ii, jj, kk, kkk, iii, jjj, jjjj, kkkk)
        target = KNOWN_DEVICES[Target.Category.CPU]['Intel 8351N']
        plan = schedule.create_plan(target)
        plan.cache(A, index=ii, element_type=ScalarType.int16, vectorize=False)
        plan.cache(B, index=jjjj, trigger_index=jj, layout=Array.Layout.LAST_MAJOR, vectorize=False)
        plan.cache(C, iii)
        plan.vectorize(jjjj)
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(test_name, format=Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)

    def test_int16_matmul_vpmaddwd_16_element_host(self):
        test_name = 'test_int16_matmul_vpmaddwd_16_element_host'
        M = 240
        N = 256
        K = 256
        A = Array(role=Role.INPUT, element_type=ScalarType.int16, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.int16, shape=(K, N), layout=Array.Layout.FIRST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.int32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: 24, j: 128, k: 128})
        iii, jjj, kkk = schedule.tile({ii: 6, jj: 32, kk: 4})
        jjjj, kkkk = schedule.tile({jjj: 16, kkk: 2})
        schedule.reorder(i, j, k, ii, jj, kk, kkk, iii, jjj, jjjj, kkkk)
        plan = schedule.create_plan()
        plan.cache(A, index=ii, element_type=ScalarType.int16, vectorize=False)
        plan.cache(B, index=jjjj, trigger_index=jj, layout=Array.Layout.LAST_MAJOR, vectorize=False)
        plan.cache(C, iii)
        plan.vectorize(jjjj)
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        A_test = np.random.random((M, K)).astype(np.int16)
        B_test = np.random.random((K, N)).astype(np.int16)
        C_test = np.random.random((M, N)).astype(np.int32)
        correctness_check_values = {'pre': (A_test, B_test, C_test), 'post': (A_test, B_test, C_test + A_test @ B_test)}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(test_name, format=Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            v.check_correctness(function.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    def test_int16_matmul_vpmaddwd_cast_input(self):
        test_name = 'test_int16_matmul_vpmaddwd_cast_input'
        M = 240
        N = 256
        K = 256
        A = Array(role=Role.INPUT, element_type=ScalarType.int16, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.int16, shape=(K, N), layout=Array.Layout.FIRST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.int32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += cast(A[i, k], ScalarType.int32) * cast(B[k, j], ScalarType.int32)
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: 24, j: 128, k: 128})
        iii, jjj, kkk = schedule.tile({ii: 6, jj: 16, kk: 4})
        jjjj, kkkk = schedule.tile({jjj: 8, kkk: 2})
        schedule.reorder(i, j, k, ii, jj, kk, kkk, iii, jjj, jjjj, kkkk)
        plan = schedule.create_plan()
        plan.cache(A, index=ii, element_type=ScalarType.int16, vectorize=False)
        plan.cache(B, index=jjjj, trigger_index=jj, layout=Array.Layout.LAST_MAJOR, vectorize=False)
        plan.cache(C, iii)
        plan.vectorize(jjjj)
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        A_test = np.random.random((M, K)).astype(np.int16)
        B_test = np.random.random((K, N)).astype(np.int16)
        C_test = np.random.random((M, N)).astype(np.int32)
        correctness_check_values = {'pre': (A_test, B_test, C_test), 'post': (A_test, B_test, C_test + A_test @ B_test)}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(test_name, format=Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            v.check_correctness(function.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    def test_int32_horizontal_vector_add(self):
        test_name = 'test_int32_horizontal_vector_add'
        M = 256
        N = 16
        A = Array(role=Role.INPUT, element_type=ScalarType.int32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.int32, shape=(M,), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _():
            B[i] += A[i, j]
        schedule = nest.create_schedule()
        plan = schedule.create_plan()
        plan.vectorize(j)
        package = Package()
        function = package.add(plan, args=(A, B), base_name=test_name)
        A_test = np.random.random((M, N)).astype(np.int32)
        B_test = np.random.random((M,)).astype(np.int32)
        B_ref = np.zeros((M,)).astype(np.int32)
        B_ref[:] = B_test[:]
        for j in range(N):
            B_ref[:] += A_test[:, j]
        correctness_check_values = {'pre': (A_test, B_test), 'post': (A_test, B_ref)}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(test_name, format=Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            v.check_correctness(function.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    def test_int16_to_int32_horizontal_vector_add_simple(self):
        test_name = 'test_int16_to_int32_horizontal_vector_add_simple'
        M = 256
        N = 16
        A = Array(role=Role.INPUT, element_type=ScalarType.int16, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.int32, shape=(M,), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _():
            B[i] += A[i, j]
        schedule = nest.create_schedule()
        ii = schedule.split(i, 4)
        schedule.reorder(i, ii, j)
        plan = schedule.create_plan()
        plan.vectorize(ii)
        package = Package()
        function = package.add(plan, args=(A, B), base_name=test_name)
        A_test = np.random.random((M, N)).astype(np.int16)
        B_test = np.random.random((M,)).astype(np.int32)
        B_ref = B_test.copy()
        for j in range(N):
            B_ref[:] += A_test[:, j]
        correctness_check_values = {'pre': (A_test, B_test), 'post': (A_test, B_ref)}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(test_name, format=Package.Format.MLIR | Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            v.check_correctness(function.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    def test_int16_to_int32_horizontal_vector_add_1_row(self):
        test_name = 'test_int16_to_int32_horizontal_vector_add_1_row'
        M = 1
        N = 16
        A = Array(role=Role.INPUT, element_type=ScalarType.int16, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.int32, shape=(M,), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _():
            B[i] += A[i, j]
        schedule = nest.create_schedule()
        plan = schedule.create_plan()
        plan.vectorize(i)
        plan.vectorize(j)
        package = Package()
        function = package.add(plan, args=(A, B), base_name=test_name)
        A_test = np.random.random((M, N)).astype(np.int16)
        B_test = np.random.random((M,)).astype(np.int32)
        B_ref = B_test.copy()
        for j in range(N):
            B_ref[:] += A_test[:, j]
        correctness_check_values = {'pre': (A_test, B_test), 'post': (A_test, B_ref)}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(test_name, format=Package.Format.MLIR | Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            v.check_correctness(function.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    def test_f32_horizontal_vector_add_1_row(self):
        test_name = 'test_f32_horizontal_vector_add_1_row'
        N = 8
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N,), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(1,), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(N,))
        i, = nest.get_indices()

        @nest.iteration_logic
        def _():
            B[0] += A[i]
        schedule = nest.create_schedule()
        plan = schedule.create_plan()
        plan.vectorize(i)
        package = Package()
        function = package.add(plan, args=(A, B), base_name=test_name)
        A_test = np.random.random((N,)).astype(np.float32)
        B_test = np.random.random((1,)).astype(np.float32)
        B_ref = B_test.copy()
        for i in range(N):
            B_ref[0] += A_test[i]
        correctness_check_values = {'pre': (A_test, B_test), 'post': (A_test, B_ref)}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(test_name, format=Package.Format.MLIR | Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            v.check_correctness(function.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    def test_i32_horizontal_vector_add_1_row(self):
        test_name = 'test_i32_horizontal_vector_add_1_row'
        N = 8
        A = Array(role=Role.INPUT, element_type=ScalarType.int32, shape=(N,), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.int32, shape=(1,), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(N,))
        i, = nest.get_indices()

        @nest.iteration_logic
        def _():
            B[0] += A[i]
        schedule = nest.create_schedule()
        plan = schedule.create_plan()
        plan.vectorize(i)
        package = Package()
        function = package.add(plan, args=(A, B), base_name=test_name)
        A_test = np.random.random((N,)).astype(np.int32)
        B_test = np.random.random((1,)).astype(np.int32)
        B_ref = B_test.copy()
        for i in range(N):
            B_ref[0] += A_test[i]
        correctness_check_values = {'pre': (A_test, B_test), 'post': (A_test, B_ref)}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(test_name, format=Package.Format.MLIR | Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            v.check_correctness(function.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    def test_int32_horizontal_vector_add_simple(self):
        test_name = 'test_int32_horizontal_vector_add_simple'
        M = 256
        N = 8
        A = Array(role=Role.INPUT, element_type=ScalarType.int32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.int32, shape=(M,), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _():
            B[i] += A[i, j]
        schedule = nest.create_schedule()
        ii = schedule.split(i, 4)
        schedule.reorder(i, ii, j)
        plan = schedule.create_plan()
        plan.vectorize(ii)
        package = Package()
        function = package.add(plan, args=(A, B), base_name=test_name)
        A_test = np.random.random((M, N)).astype(np.int32)
        B_test = np.random.random((M,)).astype(np.int32)
        B_ref = B_test.copy()
        for j in range(N):
            B_ref[:] += A_test[:, j]
        correctness_check_values = {'pre': (A_test, B_test), 'post': (A_test, B_ref)}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(test_name, format=Package.Format.MLIR | Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            v.check_correctness(function.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    def test_float32_horizontal_vector_add_simple(self):
        test_name = 'test_float32_horizontal_vector_add_simple'
        M = 256
        N = 8
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M,), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _():
            B[i] += A[i, j]
        schedule = nest.create_schedule()
        ii = schedule.split(i, 4)
        schedule.reorder(i, ii, j)
        plan = schedule.create_plan()
        plan.vectorize(ii)
        package = Package()
        function = package.add(plan, args=(A, B), base_name=test_name)
        A_test = np.random.random((M, N)).astype(np.float32)
        B_test = np.random.random((M,)).astype(np.float32)
        B_ref = B_test.copy()
        for j in range(N):
            B_ref[:] += A_test[:, j]
        correctness_check_values = {'pre': (A_test, B_test), 'post': (A_test, B_ref)}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        with verifiers.VerifyPackage(self, test_name, output_dir) as v:
            package.build(test_name, format=Package.Format.MLIR | Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            v.check_correctness(function.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    def test_matmul_input_cache_element_type_widen(self) -> None:
        test_name = 'test_matmul_input_cache_element_type_widen'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.int16, ScalarType.int16, ScalarType.int16), cache_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.int16))

    def test_matmul_output_cache_element_type_widen(self) -> None:
        test_name = 'test_matmul_output_cache_element_type_widen'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.int16, ScalarType.int16, ScalarType.int16), cache_element_types=(ScalarType.int16, ScalarType.int16, ScalarType.int32))

    def test_matmul_input_output_cache_element_type_widen(self) -> None:
        test_name = 'test_matmul_input_output_cache_element_type_widen'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.int16, ScalarType.int16, ScalarType.int16), cache_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.int32))

    def test_matmul_input_cache_element_type_narrow(self) -> None:
        test_name = 'test_matmul_input_cache_element_type_narrow'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.int32), cache_element_types=(ScalarType.int16, ScalarType.int16, ScalarType.int32))

    def test_matmul_output_cache_element_type_narrow(self) -> None:
        test_name = 'test_matmul_output_cache_element_type_narrow'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.int32), cache_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.int16))

    def test_matmul_input_output_cache_element_type_narrow(self) -> None:
        test_name = 'test_matmul_input_output_cache_element_type_narrow'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.int32), cache_element_types=(ScalarType.int16, ScalarType.int16, ScalarType.int16))

    def test_matmul_input_cache_element_type_int_to_float(self) -> None:
        test_name = 'test_matmul_input_cache_element_type_int_to_float'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.int32), cache_element_types=(ScalarType.float32, ScalarType.float32, ScalarType.int32))

    def test_matmul_output_cache_element_type_int_to_float(self) -> None:
        test_name = 'test_matmul_output_cache_element_type_int_to_float'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.int32), cache_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.float32))

    def test_matmul_input_output_cache_element_type_int_to_float(self) -> None:
        test_name = 'test_matmul_input_output_cache_element_type_int_to_float'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.int32), cache_element_types=(ScalarType.float32, ScalarType.float32, ScalarType.float32))

    def test_matmul_input_cache_element_type_float_to_int(self) -> None:
        test_name = 'test_matmul_input_cache_element_type_float_to_int'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.float32, ScalarType.float32, ScalarType.float32), cache_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.float32), check_correctness=False)

    def test_matmul_output_cache_element_type_float_to_int(self) -> None:
        test_name = 'test_matmul_output_cache_element_type_float_to_int'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.float32, ScalarType.float32, ScalarType.float32), cache_element_types=(ScalarType.float32, ScalarType.float32, ScalarType.int32), check_correctness=False)

    def test_matmul_input_output_cache_element_type_float_to_int(self) -> None:
        test_name = 'test_matmul_input_output_cache_element_type_float_to_int'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.float32, ScalarType.float32, ScalarType.float32), cache_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.int32), check_correctness=False)

    def test_matmul_input_cache_element_type_int_to_uint(self) -> None:
        test_name = 'test_matmul_input_cache_element_type_int_to_uint'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.int32), cache_element_types=(ScalarType.uint32, ScalarType.uint32, ScalarType.int32))

    def test_matmul_output_cache_element_type_int_to_uint(self) -> None:
        test_name = 'test_matmul_output_cache_element_type_int_to_uint'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.int32), cache_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.uint32))

    def test_matmul_input_output_cache_element_type_int_to_uint(self) -> None:
        test_name = 'test_matmul_input_output_cache_element_type_int_to_uint'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.int32), cache_element_types=(ScalarType.uint32, ScalarType.uint32, ScalarType.uint32))

    def test_matmul_input_cache_element_type_uint_to_int(self) -> None:
        test_name = 'test_matmul_input_cache_element_type_uint_to_int'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.uint32, ScalarType.uint32, ScalarType.uint32), cache_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.uint32))

    def test_matmul_output_cache_element_type_uint_to_int(self) -> None:
        test_name = 'test_matmul_output_cache_element_type_uint_to_int'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.uint32, ScalarType.uint32, ScalarType.uint32), cache_element_types=(ScalarType.uint32, ScalarType.uint32, ScalarType.int32))

    def test_matmul_input_output_cache_element_type_uint_to_int(self) -> None:
        test_name = 'test_matmul_input_output_cache_element_type_uint_to_int'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.uint32, ScalarType.uint32, ScalarType.uint32), cache_element_types=(ScalarType.int32, ScalarType.int32, ScalarType.int32))

    def test_matmul_input_cache_element_type_uint_to_int(self) -> None:
        test_name = 'test_matmul_input_cache_element_type_uint8_to_int16'
        self._matmul_cache_element_type_common(test_name, array_element_types=(ScalarType.uint8, ScalarType.uint8, ScalarType.int32), cache_element_types=(ScalarType.int16, ScalarType.int16, ScalarType.int32))

    def test_gpu_barrier_opt(self) -> None:
        from accera import Array, Nest, Package, ScalarType, Target
        from accera._lang_python._lang import Allocate, _MemorySpace, Array as NativeArray
        from accera._lang_python._lang._gpu import Barrier
        from accera._lang_python import _MemoryLayout
        N = 256
        block_x = 16
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N,))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(N,))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(N,))
        nest = Nest(shape=(N,))
        i, = nest.get_indices()

        @nest.iteration_logic
        def _():
            shA = NativeArray(Allocate(type=ScalarType.float32, layout=_MemoryLayout([block_x]).set_memory_space(_MemorySpace.SHARED)))
            shB = NativeArray(Allocate(type=ScalarType.float32, layout=_MemoryLayout([block_x]).set_memory_space(_MemorySpace.SHARED)))
            Barrier()
            shA[i] = A[i]
            Barrier()
            Barrier()
            shA[i] = B[i]
            Barrier()
            C[i] = shA[i] + shB[i]
            Barrier()
        schedule = nest.create_schedule()
        ii = schedule.split(i, block_x)
        schedule.reorder(i, ii)
        target = Target(category=Target.Category.GPU, runtime=Target.Runtime.ROCM)
        plan = schedule.create_plan(target)
        plan.bind(mapping={i: target.GridUnit.BLOCK_X, ii: target.GridUnit.THREAD_X})
        test_name = 'test_gpu_barrier_opt'
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / test_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, test_name, output_dir, file_list=[f'{test_name}.cu']) as v:
            package.build(name=test_name, format=Package.Format.MLIR | Package.Format.DEFAULT, mode=Package.Mode.RELEASE, output_dir=output_dir)
            if ROCM_AVAILABLE:
                before = [np.random.rand(*p.shape).astype(np.float32) for p in function.args]
                after = [before[0], before[1], before[0] + before[1]]
                v.check_correctness(function.name, before=before, after=after)

    def test_rocm_gemm_tiled_output(self) -> None:
        from accera import Array, Nest, Package, ScalarType, Target
        M = 16
        N = M
        K = M
        block_x = 16
        block_y = block_x
        tile_size = 16
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N))
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj = schedule.tile({i: block_x, j: block_y})
        iii, jjj, kk = schedule.tile({ii: tile_size, jj: tile_size, k: tile_size})
        schedule.reorder((i, j, ii, jj, k, iii, jjj, kk))
        target = Target(Target.Model.AMD_MI100)
        plan = schedule.create_plan(target=target)
        plan.bind(mapping={i: target.GridUnit.BLOCK_X, j: target.GridUnit.BLOCK_Y, ii: target.GridUnit.THREAD_X, jj: target.GridUnit.THREAD_Y})
        test_name = 'test_rocm_gemm_tiled_output'
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)

        def file_check_fn(v):
            checker = v.file_checker(f'{test_name}.cu')
            checker.check_label('int32_t affine_map_func_0_i0(int32_t d0, int32_t d1) {')
            checker.check('int32_t idx = ((d0 * 16) + d1);')
            checker.check('return idx;')
            checker.check_label('extern "C" __global__  __launch_bounds__(1) void test_rocm_gemm_tiled_output_{{.+}}__gpu__(float *arg0, float *arg1, float *arg2')
            checker.check_count('for (int32_t idx{{[0-9]}} = 0; idx{{[0-9]}} < 16; idx{{[0-9]}} += 1) {', 3)
            checker.run()
        self._verify_matrix_multiplication_function(function, package, test_name, file_check_fn=file_check_fn, check_correctness=ROCM_AVAILABLE, file_list=[f'{test_name}.cu', f'{test_name}.hat'], package_format=Package.Format.DEFAULT)

    def test_thrifty_caching_simple_input_cache(self) -> None:
        import accera as acc
        package = Package()
        M = 32
        N = 32
        K = 32
        A = acc.Array(role=acc.Role.INPUT, shape=(M, K), layout=acc.Array.Layout.FIRST_MAJOR)
        B = acc.Array(role=acc.Role.INPUT, shape=(K, N), layout=acc.Array.Layout.FIRST_MAJOR)
        C = acc.Array(role=acc.Role.INPUT_OUTPUT, shape=(M, N), layout=acc.Array.Layout.FIRST_MAJOR)
        nest = acc.Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii = schedule.split(i, 4)
        jj = schedule.split(j, 16)
        kk = schedule.split(k, 32)
        order = [i, j, k, ii, jj, kk]
        schedule.reorder(order)
        plan = schedule.create_plan()
        AA = plan.cache(A, index=ii, thrifty=True, layout=acc.Array.Layout.FIRST_MAJOR)
        BB = plan.cache(B, index=k, thrifty=True, layout=acc.Array.Layout.FIRST_MAJOR)
        function = package.add(plan, args=(A, B, C), base_name=f'test_thrifty_caching_simple_input_cache')

        def run_file_check(verifier):
            checker = verifier.file_checker(f'*_LoopNestToValueFunc.mlir')
            checker.check_label('"accv.lambda"() ({')
            checker.check_not('%{{[0-9]}} = "accv.ref_global"() {global_name = @cache_{{[0-9]}}} : () -> memref<4x32xf32, 3>')
            checker.check('%{{[0-9]}} = "accv.ref_global"() {global_name = @cache_{{[0-9]}}} : () -> memref<32x16xf32, 3>')
            checker.check_not('%{{[0-9]}} = "accv.ref_global"() {global_name = @cache_{{[0-9]}}} : () -> memref<4x32xf32, 3>')
            checker.check('affine.for %arg{{[0-9]}} = 0 to 32 step 4 {')
            checker.run()
        self._verify_matrix_multiplication_function(function, package, f'test_thrifty_caching_simple_input_cache', run_file_check)

    def test_thrifty_caching_simple_output_cache_elide(self) -> None:
        import accera as acc
        package = Package()
        M = 32
        N = 32
        K = 32
        A = acc.Array(role=acc.Role.INPUT, shape=(M, K), layout=acc.Array.Layout.FIRST_MAJOR)
        B = acc.Array(role=acc.Role.INPUT, shape=(K, N), layout=acc.Array.Layout.FIRST_MAJOR)
        C = acc.Array(role=acc.Role.INPUT_OUTPUT, shape=(M, N), layout=acc.Array.Layout.FIRST_MAJOR)
        nest = acc.Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii = schedule.split(i, 4)
        jj = schedule.split(j, 32)
        kk = schedule.split(k, 8)
        order = [i, j, k, ii, jj, kk]
        schedule.reorder(order)
        plan = schedule.create_plan()
        CC = plan.cache(C, index=ii, thrifty=True, layout=acc.Array.Layout.FIRST_MAJOR)

        def run_file_check(verifier):
            checker = verifier.file_checker(f'*_LoopNestToValueFunc.mlir')
            checker.check_label('"accv.lambda"() ({')
            checker.check_not('%{{[0-9]}} = "accv.ref_global"() {global_name = @cache_{{[0-9]}}} : () -> memref<4x32xf32, 3>')
            checker.check('affine.for %arg{{[0-9]}} = 0 to 32 step 4 {')
            checker.run()
        function = package.add(plan, args=(A, B, C), base_name=f'test_thrifty_caching_simple_output_cache_elide')
        self._verify_matrix_multiplication_function(function, package, f'test_thrifty_caching_simple_output_cache_elide', run_file_check)

    def test_gpu_cache_different_input_layouts(self):
        from accera import Array, Nest, Package, ScalarType, Target
        from accera._lang_python._lang import _MemorySpace
        M = 2560
        N = 1536
        K = 2048
        S = 4
        block_x = 16
        block_y = block_x
        k_outer_tile_size = 512
        k_inner_tile_size = 32
        m_tile_size = block_x
        n_tile_size = block_y
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(S, M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(S, K, N), layout=Array.Layout.LAST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(S, M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(S, M, N, K))
        b, i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[b, i, j] += A[b, i, k] * B[b, k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: m_tile_size, j: n_tile_size, k: k_outer_tile_size})
        kkk = schedule.split(kk, k_inner_tile_size)
        schedule.reorder(b, i, j, k, kk, ii, jj, kkk)
        target = Target(category=Target.Category.GPU, runtime=Target.Runtime.CUDA)
        plan = schedule.create_plan(target=target)
        plan.bind(mapping={i: target.GridUnit.BLOCK_X, j: target.GridUnit.BLOCK_Y, ii: target.GridUnit.THREAD_X, jj: target.GridUnit.THREAD_Y})
        plan.cache(A, index=ii, location=_MemorySpace.SHARED, layout=Array.Layout.FIRST_MAJOR)
        plan.cache(B, index=ii, location=_MemorySpace.SHARED, layout=Array.Layout.FIRST_MAJOR)
        package_name = 'test_gpu_cache_different_input_layouts'
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=package_name)

        def file_check_fn(verifier):
            checker = verifier.file_checker(f'*_LoopNestToValueFunc.mlir')
            checker.check_label('accv.func nested @test_gpu_cache_different_input_layouts_')
            checker.check_same('%[[Array_A:[a-z0-9_]+]]: memref<4x2560x2048xf32>')
            checker.check_same('%[[Array_B:[a-z0-9_]+]]: memref<4x2048x1536xf32, affine_map<(d0, d1, d2) -> (d0 + d1 * 4 + d2 * 8192)>>')
            checker.check_same('%[[Array_C:[a-z0-9_]+]]: memref<4x2560x1536xf32>')
            checker.check('%[[Block_Y:[0-9_]+]] = gpu.block_id y')
            checker.check('%[[Block_X:[0-9_]+]] = gpu.block_id x')
            checker.check('%[[Cache_A:[0-9_]+]] = "accv.alloc"() : () -> memref<1x16x32xf32, 3>')
            checker.check('%[[Cache_B:[0-9_]+]] = "accv.alloc"() : () -> memref<1x32x16xf32, 3>')
            checker.check('affine.for %[[b_iv:[a-z0-9_]+]] = 0 to 4 {')
            checker.check('affine.for %[[k_iv:[a-z0-9_]+]] = 0 to 2048 step 512 {')
            checker.check('affine.for %[[kk_iv:[a-z0-9_]+]] = 0 to 512 step 32 {')
            checker.check('"accv.lambda"() ({')
            checker.check('%[[Thread_X:[0-9_]+]] = gpu.thread_id x')
            checker.check('%[[Thread_Y:[0-9_]+]] = gpu.thread_id y')
            checker.check('affine.for %[[lpt_iv:[a-z0-9_]+]] = 0 to 2 {')
            checker.check('%[[Loaded_A_Val:[0-9_]+]] = affine.load %[[Array_A]][%[[b_iv]], symbol(%[[Block_X]]) * 16 + symbol(%[[Thread_X]]) - (symbol(%[[Block_X]]) floordiv 160) * 2560, %[[lpt_iv]] * 16 + %[[k_iv]] + %[[kk_iv]] + symbol(%[[Thread_Y]])] : memref<4x2560x2048xf32>')
            checker.check('affine.store %[[Loaded_A_Val]], %[[Cache_A]][0, symbol(%[[Thread_X]]), %[[lpt_iv]] * 16 + symbol(%[[Thread_Y]])] : memref<1x16x32xf32, 3>')
            checker.check('"accv.lambda"() ({')
            checker.check('%[[Thread_X:[0-9_]+]] = gpu.thread_id x')
            checker.check('%[[Thread_Y:[0-9_]+]] = gpu.thread_id y')
            checker.check('affine.for %[[lpt_iv:[a-z0-9_]+]] = 0 to 2 {')
            checker.check('%[[Loaded_B_Val:[0-9_]+]] = affine.load %[[Array_B]][%[[b_iv]], %[[k_iv]] + %[[kk_iv]] + symbol(%[[Thread_Y]]) * 16 + symbol(%[[Thread_X]]) - (symbol(%[[Thread_Y]]) floordiv 2) * 32, %[[lpt_iv]] * 8 + symbol(%[[Block_Y]]) * 16 - (symbol(%[[Block_Y]]) floordiv 96) * 1536 + symbol(%[[Thread_Y]]) floordiv 2 - ((%[[lpt_iv]] * 8 + symbol(%[[Thread_Y]]) floordiv 2) floordiv 16) * 16] : memref<4x2048x1536xf32, affine_map<(d0, d1, d2) -> (d0 + d1 * 4 + d2 * 8192)>>')
            checker.check('affine.store %[[Loaded_B_Val]], %[[Cache_B]][0, symbol(%[[Thread_Y]]) * 16 + symbol(%[[Thread_X]]) - (symbol(%[[Thread_Y]]) floordiv 2) * 32, (%[[lpt_iv]] * 8 + symbol(%[[Thread_Y]]) floordiv 2) mod 16] : memref<1x32x16xf32, 3>')
            checker.run()
        self._verify_matrix_multiplication_function(function, package, package_name, file_check_fn=file_check_fn, check_correctness=CUDA_AVAILABLE, file_list=[f'{package_name}.cu', f'{package_name}.hat'], package_format=Package.Format.DEFAULT)

    def test_gpu_cache_block_level_private_mem(self):
        from accera import Array, Nest, Package, ScalarType, Target
        from accera._lang_python._lang import _MemorySpace
        M = 2560
        N = 1536
        K = 2048
        block_x = 16
        block_y = block_x
        k_outer_tile_size = 512
        k_inner_tile_size = 32
        m_tile_size = block_x
        n_tile_size = block_y
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N), layout=Array.Layout.LAST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: m_tile_size, j: n_tile_size, k: k_outer_tile_size})
        kkk = schedule.split(kk, k_inner_tile_size)
        schedule.reorder(i, j, k, kk, ii, jj, kkk)
        target = Target(category=Target.Category.GPU, runtime=Target.Runtime.ROCM)
        plan = schedule.create_plan(target=target)
        plan.bind(mapping={i: target.GridUnit.BLOCK_X, j: target.GridUnit.BLOCK_Y, ii: target.GridUnit.THREAD_X, jj: target.GridUnit.THREAD_Y})
        plan.cache(C, index=k, location=_MemorySpace.PRIVATE, layout=Array.Layout.FIRST_MAJOR)
        package_name = 'test_gpu_cache_block_level_private_mem'
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=package_name)

        def file_check_fn(verifier):
            checker = verifier.file_checker(f'*_LoopNestToValueFunc.mlir')
            checker.check_label('accv.func nested @test_gpu_cache_block_level_private_mem_')
            checker.check('"accv.lambda"() ({')
            checker.check('%[[Cache_C:[0-9_]+]] = "accv.alloc"() : () -> memref<1x1xf32, 5>')
            checker.run()
        self._verify_matrix_multiplication_function(function, package, package_name, file_check_fn=file_check_fn, check_correctness=ROCM_AVAILABLE, file_list=[f'{package_name}.cu', f'{package_name}.hat'], package_format=Package.Format.DEFAULT | Package.Format.MLIR)

    def test_gpu_cache_block_level_shared_mem(self):
        from accera import Array, Nest, Package, ScalarType, Target
        from accera._lang_python._lang import _MemorySpace
        M = 2560
        N = 1536
        K = 2048
        block_x = 16
        block_y = block_x
        k_outer_tile_size = 512
        k_inner_tile_size = 32
        m_tile_size = block_x
        n_tile_size = block_y
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N), layout=Array.Layout.LAST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: m_tile_size, j: n_tile_size, k: k_outer_tile_size})
        kkk = schedule.split(kk, k_inner_tile_size)
        schedule.reorder(i, j, k, kk, ii, jj, kkk)
        target = Target(category=Target.Category.GPU, runtime=Target.Runtime.ROCM)
        plan = schedule.create_plan(target=target)
        plan.bind(mapping={i: target.GridUnit.BLOCK_X, j: target.GridUnit.BLOCK_Y, ii: target.GridUnit.THREAD_X, jj: target.GridUnit.THREAD_Y})
        plan.cache(C, index=j, location=_MemorySpace.SHARED, layout=Array.Layout.FIRST_MAJOR)
        package_name = 'test_gpu_cache_block_level_shared_mem'
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=package_name)

        def file_check_fn(verifier):
            checker = verifier.file_checker(f'*_LoopNestToValueFunc.mlir')
            checker.check_label('accv.func nested @test_gpu_cache_block_level_shared_mem_')
            checker.check('"accv.lambda"() ({')
            checker.check(f'%[[Cache_C:[0-9_]+]] = "accv.alloc"() : () -> memref<{m_tile_size}x{n_tile_size}xf32, 3>')
            checker.run()
        self._verify_matrix_multiplication_function(function, package, package_name, file_check_fn=file_check_fn, check_correctness=False, file_list=[f'{package_name}.cu', f'{package_name}.hat'], package_format=Package.Format.DEFAULT | Package.Format.MLIR)

    @expectedFailure(FailedReason.NOT_IN_CORE, 'Global memory caches are not yet supported on GPU targets.')
    def test_gpu_cache_block_level_global_mem(self):
        from accera import Array, Nest, Package, ScalarType, Target
        from accera._lang_python._lang import _MemorySpace
        M = 2560
        N = 1536
        K = 2048
        block_x = 16
        block_y = block_x
        k_outer_tile_size = 512
        k_inner_tile_size = 32
        m_tile_size = block_x
        n_tile_size = block_y
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N), layout=Array.Layout.LAST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: m_tile_size, j: n_tile_size, k: k_outer_tile_size})
        kkk = schedule.split(kk, k_inner_tile_size)
        schedule.reorder(i, j, k, kk, ii, jj, kkk)
        target = Target(Target.Model.AMD_MI100)
        plan = schedule.create_plan(target=target)
        plan.bind(mapping={i: target.GridUnit.BLOCK_X, j: target.GridUnit.BLOCK_Y, ii: target.GridUnit.THREAD_X, jj: target.GridUnit.THREAD_Y})
        plan.cache(C, index=j, location=_MemorySpace.GLOBAL, layout=Array.Layout.FIRST_MAJOR)
        package_name = 'test_gpu_cache_block_level_global_mem'
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=package_name)

        def file_check_fn(verifier):
            checker = verifier.file_checker(f'*_LoopNestToValueFunc.mlir')
            checker.check_label('accv.func nested @test_gpu_cache_block_level_global_mem_')
            checker.check('"accv.lambda"() ({')
            checker.check(f"""%[[Cache_C:[0-9_]+]] = "accv.ref_global"() {'{'}global_name = @cache_[[cache_id:[0-9]+]]{'}'} : () -> memref<{m_tile_size}x{N}xf32>""")
            checker.run()
        self._verify_matrix_multiplication_function(function, package, package_name, file_check_fn=file_check_fn, check_correctness=ROCM_AVAILABLE, file_list=[f'{package_name}.cu', f'{package_name}.hat'], package_format=Package.Format.DEFAULT | Package.Format.MLIR)

    def test_vectorized_and_unvectorized_cpu_caches(self):
        from accera import AUTO
        M = 512
        N = 512
        S = 512
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, S))
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(S, N))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N))
        nest = Nest(shape=(M, N, S))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii = schedule.split(i, 6)
        jj = schedule.split(j, 128)
        jjj = schedule.split(jj, 16)
        jjjj = schedule.split(jjj, 8)
        kk = schedule.split(k, 256)
        kkk = schedule.split(kk, 4)
        schedule.reorder(j, k, i, jj, kk, kkk, ii, jjj, jjjj)
        plan = schedule.create_plan()
        plan.cache(A, index=ii, vectorize=True, layout=Array.Layout.FIRST_MAJOR)
        plan.cache(B, index=kk, trigger_index=jj, vectorize=AUTO, layout=Array.Layout.FIRST_MAJOR)
        plan.cache(C, index=ii, vectorize=False, layout=Array.Layout.FIRST_MAJOR)
        plan.vectorize(jjjj)
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name='test_vectorized_and_unvectorized_cpu_caches')
        self._verify_matrix_multiplication_function(function, package, f'test_vectorized_and_unvectorized_cpu_caches')

    def test_rocm_cache_double_buffering__with_c_cache_tensorize(self) -> None:
        from accera import Array, Nest, Package, ScalarType, Target
        M = 1024
        N = 1024
        K = 1024
        outer_tile_x = 64
        outer_tile_y = outer_tile_x
        outer_tile_k = 64
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N), layout=Array.Layout.FIRST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: outer_tile_x, j: outer_tile_y, k: outer_tile_k})
        mma_shape = _MMAShape.M16xN16xK4_B1
        num_total_passes = 4
        target = Target(Target.Model.AMD_MI100)
        tensor_splits = target.tensor_core_info.compute_tensor_splits(mma_shape, num_total_passes=num_total_passes)
        iii, jjj, kkk = schedule.tile({ii: tensor_splits[0], jj: tensor_splits[1], kk: tensor_splits[2]})
        outer_nest_order = (i, j, k, ii, jj, kk)
        plan, tensorization_indices = schedule._create_tensorizable_plan(target, block_indices=(i, j), warp_indices=(ii, jj), tensor_indices=(iii, jjj, kkk), outer_nest_order=outer_nest_order)
        plan.tensorize(indices=tensorization_indices, mma_shape=mma_shape, num_total_passes=num_total_passes)
        plan.cache(A, index=ii, double_buffer=True, location=target.MemorySpace.SHARED, double_buffer_location=target.MemorySpace.PRIVATE, layout=Array.Layout.FIRST_MAJOR)
        plan.cache(B, index=ii, double_buffer=True, location=target.MemorySpace.SHARED, double_buffer_location=target.MemorySpace.PRIVATE, layout=Array.Layout.FIRST_MAJOR)
        plan.cache(C, index=iii, location=target.MemorySpace.MMA_FRAGMENT, layout=Array.Layout.FIRST_MAJOR)
        test_name = 'test_rocm_cache_double_buffering__with_c_cache_tensorize'
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        self._verify_matrix_multiplication_function(function, package, test_name, check_correctness=ROCM_AVAILABLE, file_list=[f'{test_name}.cu', f'{test_name}.hat'], package_format=Package.Format.DEFAULT)

    def test_rocm_c_cache_private(self) -> None:
        from accera import Array, Nest, Package, ScalarType, Target
        M = 1024
        N = 1024
        K = 1024
        outer_tile_x = 64
        outer_tile_y = outer_tile_x
        outer_tile_k = 64
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N), layout=Array.Layout.FIRST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: outer_tile_x, j: outer_tile_y, k: outer_tile_k})
        iii, jjj, kkk = schedule.tile({ii: 2, jj: 2, kk: 16})
        schedule.reorder(i, j, k, ii, jj, kk, iii, jjj, kkk)
        target = Target(Target.Model.AMD_MI100)
        plan = schedule.create_plan(target=target)
        plan.bind(mapping={i: target.GridUnit.BLOCK_X, j: target.GridUnit.BLOCK_Y, ii: target.GridUnit.THREAD_X, jj: target.GridUnit.THREAD_Y})
        plan.cache(C, index=iii, location=target.MemorySpace.PRIVATE, layout=Array.Layout.FIRST_MAJOR)
        test_name = 'test_rocm_c_cache_private'
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        self._verify_matrix_multiplication_function(function, package, test_name, check_correctness=ROCM_AVAILABLE, file_list=[f'{test_name}.cu', f'{test_name}.hat'], package_format=Package.Format.DEFAULT)

    def test_fill_fp16(self):
        from accera import Array, Nest, Package, ScalarType
        from accera import cast
        N = 2 ** 16
        Out = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float16, shape=(N,))
        nest = Nest(shape=(N,))
        i = nest.get_indices()

        @nest.iteration_logic
        def _():
            Out[i] = cast(2, ScalarType.float16)
        schedule = nest.create_schedule()
        plan = schedule.create_plan()
        package = Package()
        package_name = 'test_fill_fp16'
        function = package.add(plan, args=(Out,), base_name=package_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(name=package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir)

            def fill_fp16():
                return 2 * np.ones(N).astype(np.float16)
            Output_test = np.random.random(N).astype(np.float16)
            Output_ref = fill_fp16()
            v.check_correctness(function.name, before=(Output_test,), after=(Output_ref,))

    def test_abs_fp16(self):
        from accera import Array, Nest, Package, ScalarType, Target
        from accera import abs
        N = 16
        In = Array(role=Role.INPUT, element_type=ScalarType.float16, shape=(N,))
        Out = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float16, shape=(N,))
        nest = Nest(shape=(N,))
        i = nest.get_indices()

        @nest.iteration_logic
        def _():
            Out[i] = abs(In[i])
        schedule = nest.create_schedule()
        plan = schedule.create_plan()
        package = Package()
        package_name = 'test_add_scalar_fp16'
        function = package.add(plan, args=(In, Out), base_name=package_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(name=package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir)

            def abs_fp16(a):
                return np.abs(a)
            Input_test, Output_test = (np.random.uniform(-1, 1, p.shape).astype(np.float16) for p in function.args)
            Output_ref = abs_fp16(Input_test)
            v.check_correctness(function.name, before=(Input_test, Output_test), after=(Input_test, Output_ref))

    def test_vec_add_fp16(self):
        from accera import Array, Nest, Package, ScalarType
        N = 2 ** 16
        A = Array(role=Role.INPUT, element_type=ScalarType.float16, shape=(N,))
        B = Array(role=Role.INPUT, element_type=ScalarType.float16, shape=(N,))
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float16, shape=(N,))
        nest = Nest(shape=(N,))
        i = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i] = A[i] + B[i]
        schedule = nest.create_schedule()
        plan = schedule.create_plan()
        package = Package()
        package_name = 'test_vec_add_fp16'
        function = package.add(plan, args=(A, B, C), base_name=package_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(name=package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir)

            def vecadd_ref(a, b):
                return a + b
            Input0_test, Input1_test, Output_test = (np.random.random(p.shape).astype(np.float16) for p in function.args)
            Output_ref = vecadd_ref(Input0_test, Input1_test)
            v.check_correctness(function.name, before=(Input0_test, Input1_test, Output_test), after=(Input0_test, Input1_test, Output_ref))

    def test_rocm_tensorize_fp16(self) -> None:
        from accera import Array, Nest, Package, ScalarType, Target
        M = 1024
        N = 1024
        K = 1024
        outer_tile_x = 64
        outer_tile_y = outer_tile_x
        outer_tile_k = 64
        A = Array(role=Role.INPUT, element_type=ScalarType.float16, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.float16, shape=(K, N), layout=Array.Layout.FIRST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: outer_tile_x, j: outer_tile_y, k: outer_tile_k})
        mma_shape = _MMAShape.M16xN16xK16_B1
        target = Target(Target.Model.AMD_MI100)
        tensor_splits = target.tensor_core_info.compute_tensor_splits(mma_shape, num_total_passes=1)
        iii, jjj, kkk = schedule.tile({ii: tensor_splits[0], jj: tensor_splits[1], kk: tensor_splits[2]})
        outer_nest_order = (i, j, k, ii, jj, kk)
        plan, tensorization_indices = schedule._create_tensorizable_plan(target, block_indices=(i, j), warp_indices=(ii, jj), tensor_indices=(iii, jjj, kkk), outer_nest_order=outer_nest_order)
        plan.tensorize(indices=tensorization_indices, mma_shape=mma_shape)
        test_name = 'test_rocm_tensorize_fp16'
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        self._verify_matrix_multiplication_function(function, package, test_name, check_correctness=ROCM_AVAILABLE, tolerance=0.2, file_list=[f'{test_name}.cu', f'{test_name}.hat'], package_format=Package.Format.DEFAULT)

    def test_rocm_cache_double_buffering_tensorize_fp16(self) -> None:
        from accera import Array, Nest, Package, ScalarType, Target
        M = 1024
        N = 1024
        K = 1024
        outer_tile_x = 64
        outer_tile_y = outer_tile_x
        outer_tile_k = 64
        A = Array(role=Role.INPUT, element_type=ScalarType.float16, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.float16, shape=(K, N), layout=Array.Layout.FIRST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: outer_tile_x, j: outer_tile_y, k: outer_tile_k})
        mma_shape = _MMAShape.M16xN16xK16_B1
        target = Target(Target.Model.AMD_MI100)
        tensor_splits = target.tensor_core_info.compute_tensor_splits(mma_shape, num_total_passes=1)
        iii, jjj, kkk = schedule.tile({ii: tensor_splits[0], jj: tensor_splits[1], kk: tensor_splits[2]})
        outer_nest_order = (i, j, k, ii, jj, kk)
        plan, tensorization_indices = schedule._create_tensorizable_plan(target, block_indices=(i, j), warp_indices=(ii, jj), tensor_indices=(iii, jjj, kkk), outer_nest_order=outer_nest_order)
        plan.tensorize(indices=tensorization_indices, mma_shape=mma_shape)
        plan.cache(A, index=ii, double_buffer=True, location=target.MemorySpace.SHARED, double_buffer_location=target.MemorySpace.PRIVATE, layout=Array.Layout.FIRST_MAJOR)
        plan.cache(B, index=ii, double_buffer=True, location=target.MemorySpace.SHARED, double_buffer_location=target.MemorySpace.PRIVATE, layout=Array.Layout.FIRST_MAJOR)
        test_name = 'test_rocm_cache_double_buffering_tensorize_fp16'
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        self._verify_matrix_multiplication_function(function, package, test_name, check_correctness=ROCM_AVAILABLE, tolerance=0.2, file_list=[f'{test_name}.cu', f'{test_name}.hat'], package_format=Package.Format.DEFAULT | Package.Format.MLIR)

    def test_rocm_double_buffer_small_cache_vectorized_unvectorized_tensorized(self) -> None:
        from accera import Array, Nest, Package, ScalarType, Target
        M = 512
        N = 512
        K = 512
        outer_tile_x = 32
        outer_tile_y = 32
        outer_tile_k = 16
        A = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(M, K), layout=Array.Layout.FIRST_MAJOR)
        B = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(K, N), layout=Array.Layout.FIRST_MAJOR)
        C = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(M, N), layout=Array.Layout.FIRST_MAJOR)
        nest = Nest(shape=(M, N, K))
        i, j, k = nest.get_indices()

        @nest.iteration_logic
        def _():
            C[i, j] += A[i, k] * B[k, j]
        schedule = nest.create_schedule()
        ii, jj, kk = schedule.tile({i: outer_tile_x, j: outer_tile_y, k: outer_tile_k})
        mma_shape = _MMAShape.M16xN16xK4_B1
        num_total_passes = 4
        target = Target(Target.Model.AMD_MI100)
        tensor_splits = target.tensor_core_info.compute_tensor_splits(mma_shape, num_total_passes=num_total_passes)
        iii, jjj, kkk = schedule.tile({ii: tensor_splits[0], jj: tensor_splits[1], kk: tensor_splits[2]})
        outer_nest_order = (i, j, k, ii, jj, kk)
        plan, tensorization_indices = schedule._create_tensorizable_plan(target, block_indices=(i, j), warp_indices=(ii, jj), tensor_indices=(iii, jjj, kkk), outer_nest_order=outer_nest_order)
        plan.tensorize(indices=tensorization_indices, mma_shape=mma_shape, num_total_passes=num_total_passes)
        plan.cache(A, index=ii, double_buffer=True, vectorize=True, location=target.MemorySpace.SHARED, double_buffer_location=target.MemorySpace.PRIVATE, layout=Array.Layout.FIRST_MAJOR)
        plan.cache(B, index=ii, double_buffer=True, location=target.MemorySpace.SHARED, double_buffer_location=target.MemorySpace.PRIVATE, layout=Array.Layout.FIRST_MAJOR)
        test_name = 'test_rocm_double_buffer_small_cache_vectorized_unvectorized'
        package = Package()
        function = package.add(plan, args=(A, B, C), base_name=test_name)
        self._verify_matrix_multiplication_function(function, package, test_name, check_correctness=ROCM_AVAILABLE, file_list=[f'{test_name}.cu', f'{test_name}.hat'], package_format=Package.Format.DEFAULT | Package.Format.MLIR)

    def test_loop_erase_hack(self) -> None:
        M = 256
        N = 128
        K = 512
        M_tile = 32
        N_tile = 16
        K_tile = 8
        A = Array(role=Role.INPUT, shape=(M, K))
        B = Array(role=Role.INPUT, shape=(K, N))
        C = Array(role=Role.INPUT_OUTPUT, shape=(M, N))
        nest0 = Nest(shape=(M, N, K))
        i0, j0, k0 = nest0.get_indices()

        @nest0.iteration_logic
        def _():
            C[i0, j0] += A[i0, k0] * B[k0, j0]
        schedule0 = nest0.create_schedule()
        ii0, jj0, kk0 = schedule0.tile({i0: M_tile, j0: N_tile, k0: K_tile})
        schedule0.reorder(i0, j0, k0, ii0, jj0, kk0)
        nest1 = Nest(shape=(M, N, K))
        i1, j1, k1 = nest1.get_indices()

        @nest1.iteration_logic
        def _():
            C[i1, j1] = C[i1, j1] * Scalar(0.2)
        schedule1 = nest1.create_schedule()
        ii1, jj1, kk1 = schedule1.tile({i1: M_tile, j1: N_tile, k1: K_tile})
        schedule1.reorder(i1, j1, k1, ii1, jj1, kk1)
        schedule = fuse((schedule0, schedule1), partial=3)
        i, j, k, f, ii0, jj0, kk0, ii1, jj1, kk1 = schedule.get_indices()
        plan = schedule.create_plan()
        plan._erase_loops([kk1])
        package_name = 'test_loop_erase_hack'
        package = Package()
        package.add(plan, args=(A, B, C), base_name='test_loop_erase_hack')
        with verifiers.VerifyPackage(self, package_name, TEST_PACKAGE_DIR):
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=TEST_PACKAGE_DIR)

    def test_dynamic_size_redundant_split(self) -> None:
        package_name = 'test_dynamic_size_redundant_split'
        split_size = 32
        m_extent = Dimension(name='m_extent')
        input_arr = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(m_extent,))
        output_arr = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(m_extent,))
        nest = Nest((m_extent,))
        i, = nest.get_indices()

        @nest.iteration_logic
        def _():
            output_arr[i] += input_arr[i]
        sched = nest.create_schedule()
        ii = sched.split(i, split_size)
        iii = sched.split(ii, split_size)
        sched.reorder(i, ii, iii)
        plan = sched.create_plan()
        package = Package()
        fn = package.add(plan, args=(m_extent, input_arr, output_arr), base_name=package_name)
        M_test = np.int64(67)
        input_test = np.random.random((M_test,)).astype(np.float32)
        output_test = np.random.random((M_test,)).astype(np.float32)
        correctness_check_values = {'pre': [M_test, input_test, output_test], 'post': [M_test, input_test, output_test + input_test]}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir)
            v.check_correctness(fn.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    def test_dynamic_size_redundant_split_1(self) -> None:
        package_name = 'test_dynamic_size_redundant_split_1'
        split_size = 1
        m_extent = Dimension('m_extent')
        input_arr = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(m_extent,))
        output_arr = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(m_extent,))
        nest = Nest((m_extent,))
        i, = nest.get_indices()

        @nest.iteration_logic
        def _():
            output_arr[i] += input_arr[i]
        sched = nest.create_schedule()
        ii = sched.split(i, split_size)
        iii = sched.split(ii, split_size)
        sched.reorder(i, ii, iii)
        plan = sched.create_plan()
        package = Package()
        fn = package.add(plan, args=(m_extent, input_arr, output_arr), base_name=package_name)
        M_test = np.int64(1)
        input_test = np.random.random((M_test,)).astype(np.float32)
        output_test = np.random.random((M_test,)).astype(np.float32)
        correctness_check_values = {'pre': [M_test, input_test, output_test], 'post': [M_test, input_test, output_test + input_test]}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir, _quiet=False)
            v.check_correctness(fn.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    def test_dynamic_size_split_1(self) -> None:
        package_name = 'test_dynamic_size_split_1'
        split_size = 1
        m_extent = Dimension('m_extent')
        input_arr = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(m_extent,))
        output_arr = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(m_extent,))
        nest = Nest((m_extent,))
        i, = nest.get_indices()

        @nest.iteration_logic
        def _():
            output_arr[i] += input_arr[i]
        sched = nest.create_schedule()
        ii = sched.split(i, split_size)
        sched.reorder(i, ii)
        plan = sched.create_plan()
        package = Package()
        fn = package.add(plan, args=(m_extent, input_arr, output_arr), base_name=package_name)
        M_test = np.int64(1)
        input_test = np.random.random((M_test,)).astype(np.float32)
        output_test = np.random.random((M_test,)).astype(np.float32)
        correctness_check_values = {'pre': [M_test, input_test, output_test], 'post': [M_test, input_test, output_test + input_test]}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir, _quiet=False)
            v.check_correctness(fn.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    def test_dynamic_size_split_and_redundant_split_1(self) -> None:
        package_name = 'test_dynamic_size_split_and_redundant_split_1'
        outer_split_size = 16
        inner_split_size = 1
        m_extent = Dimension('m_extent')
        input_arr = Array(role=Role.INPUT, element_type=ScalarType.float32, shape=(m_extent,))
        output_arr = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.float32, shape=(m_extent,))
        nest = Nest((m_extent,))
        i, = nest.get_indices()

        @nest.iteration_logic
        def _():
            output_arr[i] += input_arr[i]
        sched = nest.create_schedule()
        ii = sched.split(i, outer_split_size)
        iii = sched.split(ii, inner_split_size)
        iiii = sched.split(iii, inner_split_size)
        sched.reorder(i, ii, iii, iiii)
        plan = sched.create_plan()
        package = Package()
        fn = package.add(plan, args=(m_extent, input_arr, output_arr), base_name=package_name)
        M_test = np.int64(37)
        input_test = np.random.random((M_test,)).astype(np.float32)
        output_test = np.random.random((M_test,)).astype(np.float32)
        correctness_check_values = {'pre': [M_test, input_test, output_test], 'post': [M_test, input_test, output_test + input_test]}
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(package_name, format=self.PACKAGE_FORMAT, mode=self.PACKAGE_MODE, output_dir=output_dir, _quiet=False)
            v.check_correctness(fn.name, before=correctness_check_values['pre'], after=correctness_check_values['post'])

    def test_vectorized_masked_buffer_fill(self) -> None:
        from accera._lang_python._lang import _If
        N_input = 5
        N_output = 8
        Input = Array(role=Role.INPUT, element_type=ScalarType.int32, shape=(N_input,))
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.int32, shape=(N_output,))
        package = Package()
        nest = Nest(shape=(N_output,))
        i, = nest.get_indices()

        @nest.iteration_logic
        def _nest():

            def store_value():
                Output[i] = Input[i]

            def store_zero():
                Output[i] = 0
            _If(i < N_input, store_value).Else(store_zero)
        sched = nest.create_schedule()
        plan = sched.create_plan()
        plan.vectorize(i)
        fn = package.add(plan, args=(Input, Output), base_name='test_vectorized_masked_buffer_fill')
        package_name = 'test_vectorized_masked_buffer_fill'
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(name=package_name, format=self.PACKAGE_FORMAT | Package.Format.MLIR_VERBOSE, mode=self.PACKAGE_MODE, output_dir=output_dir)

    def test_vectorized_masked_store(self) -> None:
        from accera._lang_python._lang import _If
        N_input = 8
        N_output = 5
        Input = Array(role=Role.INPUT, element_type=ScalarType.int32, shape=(N_input,))
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.int32, shape=(N_output,))
        package = Package()
        nest = Nest(shape=(N_input,))
        i, = nest.get_indices()

        @nest.iteration_logic
        def _nest():

            def store_value():
                Output[i] = Input[i]
            _If(i < N_output, store_value)
        sched = nest.create_schedule()
        plan = sched.create_plan()
        plan.vectorize(i)
        fn = package.add(plan, args=(Input, Output), base_name='test_vectorized_masked_store')
        package_name = 'test_vectorized_masked_store'
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(name=package_name, format=self.PACKAGE_FORMAT | Package.Format.MLIR_VERBOSE, mode=self.PACKAGE_MODE, output_dir=output_dir)

    def test_vectorized_masked_accumulate(self) -> None:
        from accera._lang_python._lang import _If
        N_input = 8
        N_output = 5
        Input = Array(role=Role.INPUT, element_type=ScalarType.int32, shape=(N_input,))
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.int32, shape=(N_output,))
        package = Package()
        nest = Nest(shape=(N_input,))
        i, = nest.get_indices()

        @nest.iteration_logic
        def _nest():

            def store_value():
                Output[i] += Input[i]
            _If(i < N_output, store_value)
        sched = nest.create_schedule()
        plan = sched.create_plan()
        plan.vectorize(i)
        fn = package.add(plan, args=(Input, Output), base_name='test_vectorized_masked_accumulate')
        package_name = 'test_vectorized_masked_accumulate'
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(name=package_name, format=self.PACKAGE_FORMAT | Package.Format.MLIR_VERBOSE, mode=self.PACKAGE_MODE, output_dir=output_dir)

    def test_packing_floordiv_mod_no_splits(self) -> None:
        package_name = 'test_packing_floordiv_mod_no_splits'
        M = 256
        M_inner = 16
        N = 64
        N_inner = 8
        input_shape = (M, N)
        packed_shape = (M // M_inner, N // N_inner, M_inner, N_inner)
        Input = Array(role=Role.INPUT, element_type=ScalarType.int32, shape=input_shape)
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.int32, shape=packed_shape)
        package = Package()
        nest = Nest(shape=(M, N))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _nest():
            Output[i // M_inner, j // N_inner, i % M_inner, j % N_inner] = Input[i, j]
        sched = nest.create_schedule()
        plan = sched.create_plan()
        fn = package.add(plan, args=(Input, Output), base_name=package_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(name=package_name, format=self.PACKAGE_FORMAT | Package.Format.MLIR, mode=self.PACKAGE_MODE, output_dir=output_dir)

    def test_packing_floordiv_mod_splits(self) -> None:
        package_name = 'test_packing_floordiv_mod_splits'
        M = 256
        M_inner = 16
        N = 64
        N_inner = 8
        input_shape = (M, N)
        packed_shape = (M // M_inner, N // N_inner, M_inner, N_inner)
        Input = Array(role=Role.INPUT, element_type=ScalarType.int32, shape=input_shape)
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.int32, shape=packed_shape)
        package = Package()
        nest = Nest(shape=(M, N))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _nest():
            Output[i // M_inner, j // N_inner, i % M_inner, j % N_inner] = Input[i, j]
        sched = nest.create_schedule()
        ii, jj = sched.tile(dict(zip([i, j], [M_inner, N_inner])))
        plan = sched.create_plan()
        fn = package.add(plan, args=(Input, Output), base_name=package_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(name=package_name, format=self.PACKAGE_FORMAT | Package.Format.MLIR, mode=self.PACKAGE_MODE, output_dir=output_dir)

    def test_packing_floordiv_mod_splits_vectorize(self) -> None:
        package_name = 'test_packing_floordiv_mod_splits_vectorize'
        M = 256
        M_inner = 16
        N = 64
        N_inner = 8
        input_shape = (M, N)
        packed_shape = (M // M_inner, N // N_inner, M_inner, N_inner)
        Input = Array(role=Role.INPUT, element_type=ScalarType.int32, shape=input_shape)
        Output = Array(role=Role.INPUT_OUTPUT, element_type=ScalarType.int32, shape=packed_shape)
        package = Package()
        nest = Nest(shape=(M, N))
        i, j = nest.get_indices()

        @nest.iteration_logic
        def _nest():
            Output[i // M_inner, j // N_inner, i % M_inner, j % N_inner] = Input[i, j]
        sched = nest.create_schedule()
        ii, jj = sched.tile(dict(zip([i, j], [M_inner, N_inner])))
        plan = sched.create_plan()
        plan.vectorize(jj)
        fn = package.add(plan, args=(Input, Output), base_name=package_name)
        output_dir = pathlib.Path(TEST_PACKAGE_DIR) / package_name
        shutil.rmtree(output_dir, ignore_errors=True)
        with verifiers.VerifyPackage(self, package_name, output_dir) as v:
            package.build(name=package_name, format=self.PACKAGE_FORMAT | Package.Format.MLIR, mode=self.PACKAGE_MODE, output_dir=output_dir)
if __name__ == '__main__':
    unittest.main(verbosity=10)