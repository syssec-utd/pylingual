from copy import copy
from typing import Optional
import numpy as np
from scipy import stats
from scipy.special import boxcox, inv_boxcox
from statsmodels.tsa.api import STLForecast
from statsmodels.tsa.arima.model import ARIMA
from fedot.core.data.data import InputData, OutputData
from fedot.core.operations.evaluation.operation_implementations.data_operations.ts_transformations import ts_to_table
from fedot.core.operations.evaluation.operation_implementations.implementation_interfaces import ModelImplementation
from fedot.core.operations.operation_parameters import OperationParameters
from fedot.core.repository.dataset_types import DataTypesEnum
from fedot.utilities.ts_gapfilling import SimpleGapFiller

class ARIMAImplementation(ModelImplementation):

    def __init__(self, params: Optional[OperationParameters]=None):
        super().__init__(params)
        self.arima = None
        self.lambda_value = None
        self.scope = None
        self.actual_ts_len = None

    def fit(self, input_data):
        """ Class fit arima model on data

        :param input_data: data with features, target and ids to process
        """
        source_ts = np.array(input_data.features)
        self.actual_ts_len = len(source_ts)
        transformed_ts = self._apply_boxcox(source_ts)
        p = int(self.params.get('p'))
        d = int(self.params.get('d'))
        q = int(self.params.get('q'))
        params = {'order': (p, d, q)}
        self.arima = ARIMA(transformed_ts, **params).fit()
        return self.arima

    def predict(self, input_data: InputData):
        """ Method for time series prediction on forecast length

        :param input_data: data with features, target and ids to process

        :return output_data: output data with smoothed time series
        """
        input_data = copy(input_data)
        forecast_length = input_data.task.task_params.forecast_length
        self.handle_new_data(input_data)
        start_id = self.actual_ts_len
        end_id = start_id + forecast_length - 1
        predicted = self.arima.predict(start=start_id, end=end_id)
        predicted = self._inverse_boxcox(predicted=predicted, lambda_param=self.lambda_value)
        predict = self._inverse_shift(predicted)
        predict = np.array(predict).reshape(1, -1)
        output_data = self._convert_to_output(input_data, predict=predict, data_type=DataTypesEnum.table)
        return output_data

    def predict_for_fit(self, input_data: InputData):
        input_data = copy(input_data)
        forecast_length = input_data.task.task_params.forecast_length
        fitted_values = self.arima.fittedvalues
        fitted_values = self._inverse_boxcox(predicted=fitted_values, lambda_param=self.lambda_value)
        fitted_values = self._inverse_shift(fitted_values)
        diff = int(self.actual_ts_len - len(fitted_values))
        if diff != 0:
            first_element = fitted_values[0]
            first_elements = [first_element] * diff
            first_elements.extend(list(fitted_values))
            fitted_values = np.array(first_elements)
        _, predict = ts_to_table(idx=input_data.idx, time_series=fitted_values, window_size=forecast_length)
        new_idx, target_columns = ts_to_table(idx=input_data.idx, time_series=input_data.target, window_size=forecast_length)
        input_data.idx = new_idx
        input_data.target = target_columns
        output_data = self._convert_to_output(input_data, predict=predict, data_type=DataTypesEnum.table)
        return output_data

    def handle_new_data(self, input_data: InputData):
        """
        Method to update x samples inside a model (used when we want to use old model to a new data)

        :param input_data: new input_data
        """
        if input_data.idx[0] > self.actual_ts_len:
            self.arima = self.fit(input_data)
            self.log.info('Arima refitted for handling a new data')

    def _apply_boxcox(self, source_ts):
        min_value = np.min(source_ts)
        if min_value > 0:
            pass
        else:
            self.scope = abs(min_value) + 1
            source_ts = source_ts + self.scope
        _, self.lambda_value = stats.boxcox(source_ts)
        transformed_ts = boxcox(source_ts, self.lambda_value)
        return transformed_ts

    def _inverse_boxcox(self, predicted, lambda_param):
        """ Method apply inverse Box-Cox transformation """
        if lambda_param == 0:
            return np.exp(predicted)
        else:
            res = inv_boxcox(predicted, lambda_param)
            res = self._filling_gaps(res)
            return res

    def _inverse_shift(self, values):
        """ Method apply inverse shift operation """
        if self.scope is None:
            pass
        else:
            values = values - self.scope
        return values

    @staticmethod
    def _filling_gaps(res):
        nan_ind = np.argwhere(np.isnan(res))
        res[nan_ind] = -100.0
        if 0 in nan_ind:
            res[0] = np.mean(res)
        if int(len(res) - 1) in nan_ind:
            res[int(len(res) - 1)] = np.mean(res)
        if len(np.ravel(np.argwhere(np.isnan(res)))) != 0:
            gf = SimpleGapFiller()
            res = gf.linear_interpolation(res)
        return res

class STLForecastARIMAImplementation(ModelImplementation):

    def __init__(self, params: Optional[OperationParameters]=None):
        super().__init__(params)
        self.model = None
        self.lambda_param = None
        self.scope = None
        self.actual_ts_len = None

    def fit(self, input_data):
        """ Class fit STLForecast arima model on data

        :param input_data: data with features, target and ids to process
        """
        source_ts = np.array(input_data.features)
        self.actual_ts_len = len(source_ts)
        p = int(self.params.setdefault('p', 2))
        d = int(self.params.setdefault('d', 0))
        q = int(self.params.setdefault('q', 2))
        period = int(self.params.setdefault('period', 365))
        params = {'period': period, 'model_kwargs': {'order': (p, d, q)}}
        self.model = STLForecast(source_ts, ARIMA, **params).fit()
        return self.model

    def predict(self, input_data: InputData) -> OutputData:
        """ Method for time series prediction on forecast length

        :param input_data: data with features, target and ids to process

        :return output_data: output data with smoothed time series
        """
        parameters = input_data.task.task_params
        forecast_length = parameters.forecast_length
        self.handle_new_data(input_data)
        start_id = self.actual_ts_len
        end_id = start_id + forecast_length - 1
        predicted = self.model.get_prediction(start=start_id, end=end_id).predicted_mean
        predict = np.array(predicted).reshape(1, -1)
        new_idx = np.arange(start_id, end_id + 1)
        input_data.idx = new_idx
        output_data = self._convert_to_output(input_data, predict=predict, data_type=DataTypesEnum.table)
        return output_data

    def predict_for_fit(self, input_data: InputData) -> OutputData:
        parameters = input_data.task.task_params
        forecast_length = parameters.forecast_length
        idx = input_data.idx
        target = input_data.target
        fitted_values = self.model.get_prediction(start=idx[0], end=idx[-1]).predicted_mean
        diff = int(self.actual_ts_len) - len(fitted_values)
        if diff != 0:
            first_element = fitted_values[0]
            first_elements = [first_element] * diff
            first_elements.extend(list(fitted_values))
            fitted_values = np.array(first_elements)
        _, predict = ts_to_table(idx=idx, time_series=fitted_values, window_size=forecast_length)
        new_idx, target_columns = ts_to_table(idx=idx, time_series=target, window_size=forecast_length)
        input_data.idx = new_idx
        input_data.target = target_columns
        output_data = self._convert_to_output(input_data, predict=predict, data_type=DataTypesEnum.table)
        return output_data

    def handle_new_data(self, input_data: InputData):
        """ Refit model if use new test data"""
        if input_data.idx[0] > self.actual_ts_len:
            self.model = self.fit(input_data)
            self.log.info('STL Arima refitted for handling a new data')