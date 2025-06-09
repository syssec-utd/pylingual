import inspect
import json
import warnings
from collections import OrderedDict
import gorilla
import logging
import numpy as np
import keras
from keras.callbacks import CSVLogger
from Accuinsight.modeler.core import func, path, get
from Accuinsight.modeler.core.func import get_time
from Accuinsight.modeler.core.LcConst import LcConst
from Accuinsight.modeler.core.LcConst.LcConst import RUN_NAME_KERAS, RUN_OBJ_NAME, RUN_MODEL_JSON_PATH, RUN_MODEL_SHAP_JSON_PATH, RUN_MODEL_VISUAL_JSON_PATH, SELECTED_METRICS, USER_ID
from Accuinsight.modeler.core.get_for_visual import roc_pr_curve, get_visual_info_regressor
from Accuinsight.modeler.core.Run.RunInfo.RunInfo import set_current_runs, clear_runs, set_model_json_path, set_visual_csv_path, set_visual_json_path, set_best_model_h5_path, set_best_model_json_path, set_python_dependencies, set_run_name, set_model_file_path, set_prefix_path, set_shap_json_path
from Accuinsight.modeler.core.feature_contribution import shap_value
from Accuinsight.modeler.utils.dl_utils import delete_files_except_best, get_best_model_path
from Accuinsight.modeler.utils.dependency.dependencies import gather_sources_and_dependencies
from Accuinsight.modeler.utils.os_getenv import is_in_ipython, get_os_env
from Accuinsight.modeler.clients.modeler_api import LifecycleRestApi
from Accuinsight.Lifecycle.common import Common
logging.basicConfig(level=logging.INFO, format='%(message)s')
warnings.filterwarnings('ignore')

class accuinsight(Common):

    def __init__(self):
        super().__init__()

    def get_file(self, storage_json_file_name=None):
        super().get_file(storage_json_file_name)

    @staticmethod
    def get_current_run_meta():
        global run_meta
        try:
            return run_meta
        except NameError:
            return None

    def get_current_run_id(self):
        try:
            return self.get_current_run_meta()[RUN_OBJ_NAME]
        except TypeError or KeyError:
            return None

    def autolog(self, tag=None, best_weights=False, model_monitor=False, runtime=False):
        global description, endpoint, var_model_file_path, message, thresholds, run_id, alarm, alarm_api, shap_on, run_meta
        description = tag
        endpoint = self.endpoint
        message = self.message
        thresholds = self.thresholds
        alarm = self.workspace_alarm
        alarm_api = self.workspace_alarm_api
        user_id = self.user_id
        if best_weights:
            best_weights_on = True
        else:
            best_weights_on = False
        if model_monitor:
            shap_on = True
            if self.feature_name is None:
                try:
                    if self.data is not None:
                        feature_name = get.feature_name(self.save_path, self.StorageInfo, self.target_name, data=self.data)
                        self.data = None
                    else:
                        feature_name = get.feature_name(self.save_path, self.StorageInfo, self.target_name)
                except:
                    pass
            else:
                feature_name = self.feature_name
        else:
            shap_on = False
        run_id = None
        run_meta = None
        if is_in_ipython():
            var_model_file_path = self.notebook_info
            _caller_globals = inspect.stack()[1][0].f_globals
            mainfile, sources, dependencies = gather_sources_and_dependencies(globs=_caller_globals, save_git_info=False)
        else:
            _caller_globals = inspect.stack()[1][0].f_globals
            mainfile, sources, dependencies = gather_sources_and_dependencies(globs=_caller_globals, save_git_info=True)
            var_model_file_path = mainfile['filename']

        class TrainHistoryCallbacks(keras.callbacks.Callback):

            def __init__(self, verbose=1, mode='auto', period=1):
                super(TrainHistoryCallbacks, self).__init__()
                self.verbose = verbose
                self.period = period
                self.best_epochs = 0
                self.epochs_since_last_save = 0
                self.mode = mode
                self.model_summary = OrderedDict()
                self.run_id = None
                self.model_type = None

            def on_train_begin(self, logs={}):
                logging.info('Using autolog(best_weights={}, model_monitor={}'.format(str(best_weights_on), str(shap_on)))
                global start
                start = get_time.now()
                opt = self.model.optimizer.get_config()
                opt_key = list(opt.keys())[1:]
                opt_result = {k: np.float64(opt[k]) for k in opt_key}
                self.model_summary['data_version'] = endpoint
                self.model_summary['model_description'] = description
                self.model_summary['logging_time'] = get_time.logging_time()
                self.model_summary['run_id'] = func.get_run_id()
                self.model_summary['model_type'] = get.model_type(self.model)
                if user_id is not None:
                    self.model_summary[USER_ID] = user_id
                if hasattr(self.model.loss, 'get_config'):
                    self.model_summary['loss_function'] = self.model.loss.get_config()['name']
                else:
                    self.model_summary['loss_function'] = self.model.loss
                self.model_summary['optimizer_info'] = {opt['name']: opt_result}
                '[get best model] on_train_begin '
                self.best_weights = self.model.get_weights()
                self.dict_path = path.get_file_path(self.model, usedFramework='keras')
                set_prefix_path(self.dict_path[LcConst.RUN_PREFIX_PATH])
                set_run_name(self.model_summary['model_type'], self.model_summary['run_id'])
                set_python_dependencies(py_depenpency=dependencies)
            '[get best model] on_epoch_end '

            def on_epoch_end(self, epoch, logs=None):
                logs = logs or {}
                if epoch == 0:
                    if len(self.model.metrics_names) == 1 and 'loss' in self.model.metrics_names:
                        self.monitor = 'val_loss'
                    elif len(self.model.metrics_names) >= 2:
                        self.monitor = 'val_' + self.model.metrics_names[1]
                    if self.mode not in ['auto', 'min', 'max']:
                        warnings.warn('GetBest mode %s is unknown, fallback to auto mode.' % self.mode, RuntimeWarning)
                        self.mode = 'auto'
                    if self.mode == 'min':
                        self.monitor_op = np.less
                        self.best = np.Inf
                    elif self.mode == 'max':
                        self.monitor_op = np.greater
                        self.best = -np.Inf
                    elif 'acc' in self.monitor or 'f1' in self.monitor:
                        self.monitor_op = np.greater
                        self.best = -np.Inf
                    else:
                        self.monitor_op = np.less
                        self.best = np.Inf
                else:
                    pass
                if best_weights_on:
                    self.epochs_since_last_save += 1
                    if self.epochs_since_last_save >= 1:
                        self.epochs_since_last_save = 0
                        current = logs.get(self.monitor)
                        if current is None:
                            warnings.warn('Can pick best model only with %s available, skipping.' % self.monitor, RuntimeWarning)
                        elif self.monitor_op(current, self.best):
                            self.best = current
                            self.best_epochs = epoch + 1
                            self.best_weights = self.model.get_weights()
                        else:
                            pass
                    self.current_value = current
                else:
                    self.last_epoch_metric = logs.get(self.monitor)
                    self.best_epochs = epoch + 1
                    self.current_value = logs.get(self.monitor)
                run_id = self.model_summary['model_type'] + '-' + self.model_summary['run_id']
                common_path = self.dict_path['save_model_path'] + run_id + '-epoch-' + str(epoch + 1).zfill(5) + '-' + self.monitor + '-' + str(current).zfill(5)
                save_model_path = common_path + '.json'
                save_weights_path = common_path + '.h5'
                model_json = self.model.to_json()
                with open(save_model_path, 'w') as json_file:
                    json_file.write(model_json)
                self.model.save_weights(save_weights_path)

            def on_train_end(self, logs={}):
                """[get best model] on_train_end """
                if self.verbose > 0:
                    print('Using epoch %05d with %s: %0.5f' % (self.best_epochs, self.monitor, self.best))
                self.model.set_weights(self.best_weights)
                end = get_time.now()
                self.model_summary['time_delta'] = str(end - start)
                self.model_summary[SELECTED_METRICS] = {self.monitor: self.best}
                set_model_json_path(self.dict_path['model_json'])
                model_json_full_path = self.dict_path[RUN_MODEL_JSON_PATH]
                with open(model_json_full_path, 'w', encoding='utf-8') as save_file:
                    json.dump(self.model_summary, save_file, indent='\t')
                if best_weights_on:
                    delete_files_except_best(run_id=self.model_summary['run_id'], epochs=str(self.best_epochs), path=self.dict_path)
                else:
                    delete_files_except_best(run_id=self.model_summary['run_id'], epochs=str(self.last_epochs), path=self.dict_path)
                path_for_setting_model_json = self.dict_path['save_model_dir'] + get_best_model_path(run_id=self.model_summary['run_id'], path=self.dict_path)['json']
                path_for_setting_model_h5 = self.dict_path['save_model_dir'] + get_best_model_path(run_id=self.model_summary['run_id'], path=self.dict_path)['h5']
                set_best_model_json_path(path_for_setting_model_json)
                set_best_model_h5_path(path_for_setting_model_h5)
                start_ts = int(start.timestamp())
                end_ts = int(end.timestamp())
                delta_ts = end_ts - start_ts
                global run_meta
                run_meta = clear_runs(start_ts, end_ts, delta_ts)
                accuinsight._send_message(metric=self.monitor, current_value=self.current_value, message=message, thresholds=thresholds, alarm_object=alarm, alarm_api=alarm_api)
                env_value = get_os_env('ENV')
                modeler_rest = LifecycleRestApi(env_value[LcConst.BACK_END_API_URL], env_value[LcConst.BACK_END_API_PORT], env_value[LcConst.BACK_END_API_URI])
                modeler_rest.lc_create_run(run_meta)
                if runtime:
                    accuinsight.set_runtime_model('keras')
                accuinsight.off_autolog()

        class visualCallbacks(keras.callbacks.Callback):

            def __init__(self, x_validation=None, y_validation=None):
                super(visualCallbacks, self).__init__()
                self.x_val = x_validation
                self.y_val = y_validation

            def on_train_end(self, logs={}):
                self.dict_path = path.get_file_path(self.model, usedFramework='keras')
                path_for_setting_visual_json = self.dict_path['visual_json']
                visual_json_full_path = self.dict_path[RUN_MODEL_VISUAL_JSON_PATH]
                set_visual_json_path(path_for_setting_visual_json)
                if get.is_classification(self.model):
                    visual_classification_json = roc_pr_curve(self.model, self.x_val, self.y_val)
                    with open(visual_json_full_path, 'w', encoding='utf-8') as save_file:
                        json.dump(visual_classification_json, save_file, indent='\t')
                else:
                    visual_regression_json = OrderedDict()
                    visual_regression_json['True_y'] = self.y_val.tolist()
                    visual_regression_json['Predicted_y'] = get_visual_info_regressor(self.model, self.x_val)
                    with open(visual_json_full_path, 'w', encoding='utf-8') as save_file:
                        json.dump(visual_regression_json, save_file, indent='\t')

        class shapCallbacks(keras.callbacks.Callback):

            def __init__(self, trainX, feature_name, run_id, trigger=shap_on):
                super(shapCallbacks, self).__init__()
                self.trainX = trainX
                self.trigger = trigger
                self.run_id = run_id
                self.feature_name_in_shap = feature_name

            def on_train_end(self, logs={}):
                if self.trigger:
                    self.shap_value = shap_value(self.model, self.trainX, self.feature_name_in_shap)
                    self.dict_path = path.get_file_path(self.model, usedFramework='keras')
                    shap_json_full_path = self.dict_path[RUN_MODEL_SHAP_JSON_PATH]
                    set_shap_json_path(self.dict_path['shap_json'])
                    with open(shap_json_full_path, 'w', encoding='utf-8') as save_file:
                        json.dump(self.shap_value, save_file, indent='\t')
                else:
                    pass

        def run_and_log_function(self, original, x, y, kwargs, unlogged_params):
            dict_path = path.get_file_path(self, usedFramework='keras')
            path_for_setting_visual_csv = dict_path['visual_csv']
            visual_csv_full_path = dict_path['visual_csv_full']
            set_current_runs(RUN_NAME_KERAS)
            set_model_file_path(var_model_file_path)
            set_visual_csv_path(path_for_setting_visual_csv)
            csv_logger = CSVLogger(visual_csv_full_path, append=True, separator=';')
            if 'x':
                x_train = x
            if shap_on:
                get_shap = shapCallbacks(x_train, feature_name, run_id, trigger=shap_on)
            else:
                pass
            ' save json for visualization '
            kwargs_dict = OrderedDict()
            for key, value in kwargs.items():
                kwargs_dict[key] = value
            if 'validation_data' in kwargs_dict.keys():
                validation_set = kwargs['validation_data']
                try:
                    x_val = validation_set[0]
                    y_val = validation_set[1]
                except:
                    iterator = iter(validation_set)
                    valid_set = next(iterator)
                    x_val = valid_set[0].numpy()
                    y_val = valid_set[1].numpy()
            else:
                raise ValueError('"validation_data" or "validation_split" does not exist.')
            get_visual = visualCallbacks(x_validation=x_val, y_validation=y_val)
            if 'callbacks' in kwargs:
                kwargs['callbacks'] += [csv_logger]
            else:
                kwargs['callbacks'] = [csv_logger]
            kwargs['callbacks'] += [get_visual]
            if shap_on:
                kwargs['callbacks'] += [get_shap]
            else:
                pass
            kwargs['callbacks'] += [TrainHistoryCallbacks()]
            return original(self, x, y, **kwargs)

        @gorilla.patch(keras.Model)
        def fit(self, x, y, **kwargs):
            original = gorilla.get_original_attribute(keras.Model, 'fit')
            unlogged_params = ['self', 'x', 'y', 'callbacks', 'validation_data', 'verbose']
            return run_and_log_function(self, original, x, y, kwargs, unlogged_params)
        settings = gorilla.Settings(allow_hit=True, store_hit=True)
        gorilla.apply(gorilla.Patch(keras.Model, 'fit', fit, settings=settings))

    def off_autolog():

        def stop_log(self, original, args, kwargs, unlogged_params):
            return original(self, *args, **kwargs)

        @gorilla.patch(keras.Model)
        def fit(self, *args, **kwargs):
            original = gorilla.get_original_attribute(keras.Model, 'fit')
            unlogged_params = ['self', 'x', 'y', 'callbacks', 'validation_data', 'verbose']
            return stop_log(self, original, args, kwargs, unlogged_params)
        settings = gorilla.Settings(allow_hit=True, store_hit=True)
        gorilla.apply(gorilla.Patch(keras.Model, 'fit', fit, settings=settings))