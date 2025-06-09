import json
import numpy as np
import pandas as pd
import pytest
import pywt
from amplo.automl.feature_processing.pooling import get_pool_functions
from amplo.automl.feature_processing.temporal_feature_extractor import ScoreWatcher, TemporalFeatureExtractor, _extract_wavelets, pl_pool

class TestScoreWatcher:

    def test_singular_scores(self):
        watcher = ScoreWatcher(['a', 'b'])
        watcher.update('a', 1)
        watcher.update('a', np.array(9))
        watcher.update('a', 15, weight=2)
        watcher.update('b', 20)
        assert watcher.mean() == 15.0
        assert watcher.std() == 5.0

    def test_multi_scores(self):
        watcher = ScoreWatcher(['a', 'b'])
        watcher.update('a', [1, 2, 3])
        watcher.update('a', np.array([9, 8, 7]))
        watcher.update('a', [15, 15, 15], weight=2)
        watcher.update('b', [20, 20, 20])
        assert all(watcher.mean() == 15.0)
        assert all(watcher.std() == 5.0)

@pytest.mark.usefixtures('make_rng')
class TestFunctions:

    def test_pool_single_index(self):
        size = 100
        window_size = 10
        x = pd.Series(self.rng.normal(size=size))
        agg_func = get_pool_functions('mean')
        pooled = pl_pool(x, window_size, agg_func, use_multi_index=False)
        desired_pool = x.values.reshape((-1, window_size)).mean(1)
        assert np.allclose(pooled.values.reshape(-1), desired_pool)

    def test_extract_wavelets(self):
        size = 100
        scales = [1, 10]
        wavelet = 'gaus2'
        x = pd.Series(self.rng.normal(size=size))
        transformed = _extract_wavelets(x, scales, wavelet)
        desired_trsf = pywt.cwt(x, scales, wavelet)[0].real.T
        assert np.allclose(transformed.values, desired_trsf)

@pytest.mark.usefixtures('make_rng')
class TestTemporalFeatureExtractor:

    @pytest.mark.parametrize('mode', ['classification', 'regression'])
    def test_mode_and_settings(self, mode, make_x_y):
        x, y = make_x_y
        x = x.iloc[:, :5]
        index = pd.MultiIndex.from_product([[0, 1], range(len(x) // 2)])
        x.index = index
        y.index = index
        fe = TemporalFeatureExtractor(mode=mode, timeout=3)
        out1 = fe.fit_transform(x, y)
        out2 = fe.transform(x)
        assert set(out1) == set(fe.features_), "`features_` doesn't match output."
        assert all(out1 == out2), "`fit_transform` and `transform` don't match."
        new_fe = TemporalFeatureExtractor().load_settings(fe.get_settings())
        new_out = new_fe.transform(x)
        assert all(out1 == new_out), 'FE loaded from settings has invalid output.'
        assert set(fe.features_) == set(new_fe.features_), 'FE from settings has erroneous `features_`.'
        settings = json.loads(json.dumps(fe.get_settings()))
        new_fe = TemporalFeatureExtractor().load_settings(settings)
        assert fe.get_settings() == new_fe.get_settings()
        assert all(fe.transform(x) == new_fe.transform(x))

    @pytest.mark.parametrize('mode', ['classification', 'regression'])
    def test_raw_features(self, mode):
        size = 600
        window_size = 3
        index = pd.MultiIndex.from_product([[0, 1], range(size // 2)])
        if mode == 'classification':
            y_np = np.array([*np.zeros(size // 2), *np.ones(size // 2)], dtype=int)
        elif mode == 'regression':
            y_np = np.arange(size)
        else:
            raise ValueError('Invalid mode.')
        random1 = self.rng.geometric(0.5, size // window_size)
        random2 = self.rng.normal(size=size // window_size)
        means = window_size * y_np[1::window_size] - random1 - random2
        mean_feat = np.array(list(zip(random1, means, random2))).reshape(-1)
        random_feat = self.rng.geometric(0.5, size)
        y = pd.Series(y_np, index=index)
        x = pd.DataFrame({'mean_feat': mean_feat, 'random_feat': random_feat}, index=index)
        fe = TemporalFeatureExtractor(mode=mode)
        fe._set_validation_model()
        fe.window_size_ = window_size
        fe._baseline_scores = [0.99]
        y_pooled = fe._pool_target(y)
        fe._fit_transform_raw_features(x, y_pooled)
        assert set(fe.features_) == set(fe.raw_features_)
        assert 'mean_feat__pool=mean' in fe.features_, 'Mean feature not found.'
        assert 'random_feat' not in ' '.join(fe.features_), 'Random feature accepted.'

    @pytest.mark.parametrize('mode', ['classification', 'regression'])
    def test_wav_features(self, mode):
        size = 600
        window_size = 3
        index = pd.MultiIndex.from_product([[0, 1], range(size // 2)])
        fit_wavelets = ['gaus3', 'cmor1.0-1.5', 'mexh']
        wavelet1 = fit_wavelets[0]
        wavelet2 = fit_wavelets[1]
        wav_contour1, _ = pywt.ContinuousWavelet(wavelet1).wavefun(level=6)
        wav_contour2, _ = pywt.ContinuousWavelet(wavelet2).wavefun(level=5)
        wav_contour1 = wav_contour1.real
        wav_contour2 = wav_contour2.real
        wav_feat = [*np.resize(wav_contour1, size // 2), *np.resize(wav_contour2, size // 2)]
        random_feat = self.rng.laplace(size=size)
        if mode == 'classification':
            y_np = np.array([*np.zeros(size // 2), *np.ones(size // 2)], dtype=int)
        elif mode == 'regression':
            y_raw1 = pd.Series(wav_feat, index=index).iloc[:size // 2]
            y_raw2 = pd.Series(wav_feat, index=index).iloc[size // 2:]
            y_np1 = _extract_wavelets(y_raw1, scales=[16.0], wavelet=wavelet1).values
            y_np2 = _extract_wavelets(y_raw2, scales=[8.0], wavelet=wavelet2).values
            y_np = np.concatenate([y_np1, y_np2]).reshape(-1)
        else:
            raise ValueError('Invalid mode.')
        y = pd.Series(y_np, index=index)
        x = pd.DataFrame({'wav_feat': wav_feat, 'random_feat': random_feat}, index=index)
        fe = TemporalFeatureExtractor(mode=mode, fit_wavelets=fit_wavelets)
        fe._set_validation_model()
        if mode == 'classification':
            fe._baseline_scores = [0.95]
            fe.window_size_ = window_size
        else:
            fe._baseline_scores = [0.7]
            fe.window_size_ = 1
        y_pooled = fe._pool_target(y)
        fe._fit_transform_wav_features(x, y_pooled)
        for wav in [wavelet1, wavelet2]:
            assert wav in str(fe.features_), f'Wavelet feature {wav} not found.'
        assert 'wav_feat' in str(fe.features_), "Didn't accept any wavelet feature."
        assert 'random_feat' not in str(fe.features_), 'Accepted random feature.'

    @pytest.mark.parametrize('mode', ['classification', 'regression'])
    @pytest.mark.parametrize('index_type', ['homogeneous', 'heterogeneous'])
    def test_set_window_size(self, mode, index_type):
        if index_type == 'homogeneous':
            idx_tuple = [(i, j) for i in range(10) for j in range(100000)]
        elif index_type == 'heterogeneous':
            idx_tuple = [(i, j) for i in range(10) for j in range(np.random.randint(100, 100000))]
        else:
            raise ValueError('Invalid index type.')
        index = pd.MultiIndex.from_tuples(idx_tuple)
        fe = TemporalFeatureExtractor(mode=mode)
        fe._set_window_size(index)
        if mode == 'classification':
            assert fe.window_size_ >= 1
        elif mode == 'regression':
            assert fe.window_size_ == 1
        else:
            raise ValueError('Invalid mode.')

    @pytest.mark.parametrize('mode', ['classification', 'regression'])
    def test_pool_target(self, mode, make_x_y):
        size = 90
        fe = TemporalFeatureExtractor(mode=mode)
        fe.window_size_ = 9
        if mode == 'classification':
            y_np = self.rng.choice([0, 1], size=size)
            desired_pool = pd.DataFrame(y_np.reshape((-1, fe.window_size_))).apply(lambda row: row.value_counts().idxmax(), axis=1).values
        elif mode == 'regression':
            y_np = self.rng.normal(size=size)
            desired_pool = pd.DataFrame(y_np.reshape((-1, fe.window_size_))).mean(axis=1).values
        else:
            raise ValueError('Invalid mode.')
        index = pd.MultiIndex.from_product([[0], range(size)])
        y = pd.Series(y_np, index=index)
        y_pooled = fe._pool_target(y).values
        assert np.allclose(y_pooled, desired_pool), "Pooling doesn't work as expected."

    def test_pool_features(self):
        size = 90
        index = pd.MultiIndex.from_product([[0], range(size)])
        x = pd.DataFrame({'feat_1': self.rng.normal(size=size)}, index=index)
        fe = TemporalFeatureExtractor()
        fe.window_size_ = 9
        out = fe._pool_features(x, instruction=None)
        assert out.shape[0] == size // fe.window_size_
        out = fe._pool_features(x, instruction={'feat_1': ['mean']})
        assert out.shape[0] == size // fe.window_size_
        desired_out = x.values.reshape((-1, fe.window_size_, x.shape[1])).mean(1)
        assert np.allclose(out.values, desired_out)

    @pytest.mark.parametrize('n_idx_lvl', range(1, 4))
    def test_check_index(self, n_idx_lvl):
        size = 100
        if n_idx_lvl == 1:
            index = pd.RangeIndex(size)
        elif n_idx_lvl == 2:
            index = pd.MultiIndex.from_product([[0], range(size)])
        elif n_idx_lvl == 3:
            index = pd.MultiIndex.from_product([[0], [0], range(size)])
        else:
            raise ValueError("Invalid parameter 'n_idx_lvl'.")
        x = pd.DataFrame({'feat': np.arange(size)}, index=index)
        fe = TemporalFeatureExtractor()
        if n_idx_lvl in (1, 3):
            with pytest.raises(ValueError):
                fe._check_x(x)
        else:
            x_check = fe._check_x(x)
            assert np.allclose(x, x_check)
        if n_idx_lvl == 1:
            x_check = fe._check_x(x, convert_single_index=True)
            assert np.allclose(x, x_check)