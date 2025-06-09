from DeepMTP.utils.eval_utils import get_performance_results
import numpy as np
from sklearn.metrics import hamming_loss, f1_score, recall_score, precision_score, mean_squared_error, mean_absolute_error, r2_score, accuracy_score
import pytest
import math
from sklearn.preprocessing import StandardScaler
mode = [{'problem_mode': 'classification', 'metrics': ['accuracy', 'hamming_loss', 'f1_score', 'recall', 'precision'], 'averaging': ['macro', 'micro', 'instance'], 'format': 'numpy', 'validation_setting': 'B', 'scaler': None}, {'problem_mode': 'classification', 'metrics': ['accuracy', 'hamming_loss', 'f1_score', 'recall', 'precision'], 'averaging': ['macro'], 'format': 'list', 'validation_setting': 'B', 'scaler': None}, {'problem_mode': 'classification', 'metrics': ['accuracy', 'hamming_loss', 'f1_score', 'recall', 'precision'], 'averaging': ['micro'], 'format': 'numpy', 'validation_setting': 'B', 'scaler': None}, {'problem_mode': 'classification', 'metrics': ['accuracy', 'hamming_loss', 'f1_score', 'recall', 'precision'], 'averaging': ['instance'], 'format': 'numpy', 'validation_setting': 'B', 'scaler': None}, {'problem_mode': 'regression', 'metrics': ['RMSE', 'MSE', 'MAE', 'R2'], 'averaging': ['macro', 'micro', 'instance'], 'format': 'numpy', 'validation_setting': 'B', 'scaler': None}, {'problem_mode': 'regression', 'metrics': ['RMSE', 'MSE', 'MAE', 'R2'], 'averaging': ['macro'], 'format': 'numpy', 'validation_setting': 'B', 'scaler': None}, {'problem_mode': 'regression', 'metrics': ['RMSE', 'MSE', 'MAE', 'R2'], 'averaging': ['micro'], 'format': 'numpy', 'validation_setting': 'A', 'scaler': None}, {'problem_mode': 'regression', 'metrics': ['RMSE', 'MSE', 'MAE', 'R2'], 'averaging': ['micro'], 'format': 'numpy', 'validation_setting': 'A', 'scaler': 'standard'}, {'problem_mode': 'regression', 'metrics': ['RMSE', 'MSE', 'MAE', 'R2'], 'averaging': ['instance'], 'format': 'numpy', 'validation_setting': 'B', 'scaler': None}]

@pytest.mark.parametrize('mode', mode)
def test_get_performance_results(mode):
    if mode['problem_mode'] == 'classification':
        y_true = np.random.rand(1000, 10)
        y_true[y_true > 0.5] = 1
        y_true[y_true <= 0.5] = 0
        y_pred = np.random.rand(1000, 10)
        y_pred[y_pred > 0.5] = 1
        y_pred[y_pred <= 0.5] = 0
        accuracy_per_column = []
        hamming_loss_per_column = []
        f1_score_per_column = []
        recall_per_column = []
        precision_per_column = []
        for j in range(y_true.shape[1]):
            result = y_true[:, j] == y_pred[:, j]
            accuracy_per_column.append(accuracy_score(y_true[:, j], y_pred[:, j]))
            hamming_loss_per_column.append(hamming_loss(y_true[:, j], y_pred[:, j]))
            f1_score_per_column.append(f1_score(y_true[:, j], y_pred[:, j]))
            recall_per_column.append(recall_score(y_true[:, j], y_pred[:, j]))
            precision_per_column.append(precision_score(y_true[:, j], y_pred[:, j]))
        macro_accuracy = np.mean(accuracy_per_column)
        macro_hamming_loss = np.mean(hamming_loss_per_column)
        macro_f1_score = np.mean(f1_score_per_column)
        macro_recall = np.mean(recall_per_column)
        macro_precision = np.mean(precision_per_column)
        micro_accuracy = accuracy_score(y_true.flatten(), y_pred.flatten())
        micro_hamming_loss = hamming_loss(y_true.flatten(), y_pred.flatten())
        micro_f1_score = f1_score(y_true.flatten(), y_pred.flatten())
        micro_recall = recall_score(y_true.flatten(), y_pred.flatten())
        micro_precision = precision_score(y_true.flatten(), y_pred.flatten())
        accuracy_per_row = []
        hamming_loss_per_row = []
        f1_score_per_row = []
        recall_per_row = []
        precision_per_row = []
        for j in range(y_true.shape[0]):
            result = y_true[j, :] == y_pred[j, :]
            accuracy_per_row.append(accuracy_score(y_true[j, :], y_pred[j, :]))
            hamming_loss_per_row.append(hamming_loss(y_true[j, :], y_pred[j, :]))
            f1_score_per_row.append(f1_score(y_true[j, :], y_pred[j, :]))
            recall_per_row.append(recall_score(y_true[j, :], y_pred[j, :]))
            precision_per_row.append(precision_score(y_true[j, :], y_pred[j, :]))
        instance_accuracy = np.mean(accuracy_per_row)
        instance_hamming_loss = np.mean(hamming_loss_per_row)
        instance_f1_score = np.mean(f1_score_per_row)
        instance_recall = np.mean(recall_per_row)
        instance_precision = np.mean(precision_per_row)
        (instances_arr, targets_arr, true_values_arr, pred_values_arr) = ([], [], [], [])
        for i in range(y_true.shape[0]):
            for j in range(y_true.shape[1]):
                instances_arr.append(i)
                targets_arr.append(j)
                true_values_arr.append(y_true[i, j])
                pred_values_arr.append(y_pred[i, j])
        if mode['format'] == 'numpy':
            instances_arr = np.array(instances_arr)
            targets_arr = np.array(targets_arr)
            true_values_arr = np.array(true_values_arr)
            pred_values_arr = np.array(pred_values_arr)
        results = get_performance_results('train', 0, instances_arr, targets_arr, true_values_arr, pred_values_arr, mode['validation_setting'], mode['problem_mode'], mode['metrics'], mode['averaging'], slices_arr=None, verbose=False, per_target_verbose=False, per_instance_verbose=False, top_k=None, return_detailed_macro=False, train_true_value=None, scaler_per_target=None)
        if 'accuracy' in mode['metrics']:
            if 'macro' in mode['averaging']:
                assert math.isclose(results['train_accuracy_macro'], macro_accuracy)
            if 'micro' in mode['averaging']:
                assert math.isclose(results['train_accuracy_micro'], micro_accuracy)
            if 'instance' in mode['averaging']:
                assert math.isclose(results['train_accuracy_instance'], instance_accuracy, abs_tol=0.01)
        if 'hamming_loss' in mode['metrics']:
            if 'macro' in mode['averaging']:
                assert math.isclose(results['train_hamming_loss_macro'], macro_hamming_loss)
            if 'micro' in mode['averaging']:
                assert math.isclose(results['train_hamming_loss_micro'], micro_hamming_loss)
            if 'instance' in mode['averaging']:
                assert math.isclose(results['train_hamming_loss_instance'], instance_hamming_loss, abs_tol=0.01)
        if 'f1_score' in mode['metrics']:
            if 'macro' in mode['averaging']:
                assert math.isclose(results['train_f1_score_macro'], macro_f1_score)
            if 'micro' in mode['averaging']:
                assert math.isclose(results['train_f1_score_micro'], micro_f1_score)
            if 'instance' in mode['averaging']:
                assert math.isclose(results['train_f1_score_instance'], instance_f1_score, abs_tol=0.01)
        if 'recall' in mode['metrics']:
            if 'macro' in mode['averaging']:
                assert math.isclose(results['train_recall_macro'], macro_recall)
            if 'micro' in mode['averaging']:
                assert math.isclose(results['train_recall_micro'], micro_recall)
            if 'instance' in mode['averaging']:
                assert math.isclose(results['train_recall_instance'], instance_recall, abs_tol=0.01)
        if 'precision' in mode['metrics']:
            if 'macro' in mode['averaging']:
                assert math.isclose(results['train_precision_macro'], macro_precision)
            if 'micro' in mode['averaging']:
                assert math.isclose(results['train_precision_micro'], micro_precision)
            if 'instance' in mode['averaging']:
                assert math.isclose(results['train_precision_instance'], instance_precision, abs_tol=0.01)
    else:
        y_true = np.random.rand(1000, 10)
        y_pred = np.random.rand(1000, 10)
        RMSE_per_column = []
        MSE_per_column = []
        MAE_score_per_column = []
        R2_per_column = []
        for j in range(y_true.shape[1]):
            RMSE_per_column.append(mean_squared_error(y_true[:, j], y_pred[:, j], squared=False))
            MSE_per_column.append(mean_squared_error(y_true[:, j], y_pred[:, j], squared=True))
            MAE_score_per_column.append(mean_absolute_error(y_true[:, j], y_pred[:, j]))
            R2_per_column.append(r2_score(y_true[:, j], y_pred[:, j]))
        macro_RMSE = np.mean(RMSE_per_column)
        macro_MSE = np.mean(MSE_per_column)
        macro_MAE = np.mean(MAE_score_per_column)
        macro_R2 = np.mean(R2_per_column)
        RMSE_per_row = []
        MSE_per_row = []
        MAE_score_per_row = []
        R2_per_row = []
        for j in range(y_true.shape[0]):
            RMSE_per_row.append(mean_squared_error(y_true[j, :], y_pred[j, :], squared=False))
            MSE_per_row.append(mean_squared_error(y_true[j, :], y_pred[j, :], squared=True))
            MAE_score_per_row.append(mean_absolute_error(y_true[j, :], y_pred[j, :]))
            R2_per_row.append(r2_score(y_true[j, :], y_pred[j, :]))
        instance_RMSE = np.mean(RMSE_per_row)
        instance_MSE = np.mean(MSE_per_row)
        instance_MAE = np.mean(MAE_score_per_row)
        instance_R2 = np.mean(R2_per_row)
        micro_RMSE = mean_squared_error(y_true.flatten(), y_pred.flatten(), squared=False)
        micro_MSE = mean_squared_error(y_true.flatten(), y_pred.flatten(), squared=True)
        micro_MAE = mean_absolute_error(y_true.flatten(), y_pred.flatten())
        micro_R2 = r2_score(y_true.flatten(), y_pred.flatten())
        (instances_arr, targets_arr, true_values_arr, pred_values_arr) = ([], [], [], [])
        for i in range(y_true.shape[0]):
            for j in range(y_true.shape[1]):
                instances_arr.append(i)
                targets_arr.append(j)
                true_values_arr.append(y_true[i, j])
                pred_values_arr.append(y_pred[i, j])
        if mode['format'] == 'numpy':
            instances_arr = np.array(instances_arr)
            targets_arr = np.array(targets_arr)
            true_values_arr = np.array(true_values_arr)
            pred_values_arr = np.array(pred_values_arr)
        true_values_arr_scaled = None
        pred_values_arr_scaled = None
        scaler = None
        if mode['scaler'] is not None:
            if mode['scaler'].lower() == 'standard':
                if mode['validation_setting'] == 'A':
                    scaler = StandardScaler()
                    scaler.fit(true_values_arr.flatten().reshape(-1, 1))
                    true_values_arr_scaled = scaler.transform(true_values_arr.reshape(-1, 1))
                    pred_values_arr_scaled = scaler.transform(pred_values_arr.reshape(-1, 1))
        results = get_performance_results('train', 0, instances_arr, targets_arr, true_values_arr if mode['scaler'] is None else true_values_arr_scaled, pred_values_arr if mode['scaler'] is None else pred_values_arr_scaled, mode['validation_setting'], mode['problem_mode'], mode['metrics'], mode['averaging'], slices_arr=None, verbose=False, per_target_verbose=False, per_instance_verbose=False, top_k=None, return_detailed_macro=False, train_true_value=None, scaler_per_target=scaler)
        if 'MSE' in mode['metrics']:
            if 'macro' in mode['averaging']:
                assert math.isclose(results['train_MSE_macro'], macro_MSE)
            if 'micro' in mode['averaging']:
                assert math.isclose(results['train_MSE_micro'], micro_MSE)
            if 'instance' in mode['averaging']:
                assert math.isclose(results['train_MSE_instance'], instance_MSE, abs_tol=0.01)
        if 'MAE' in mode['metrics']:
            if 'macro' in mode['averaging']:
                assert math.isclose(results['train_MAE_macro'], macro_MAE)
            if 'micro' in mode['averaging']:
                assert math.isclose(results['train_MAE_micro'], micro_MAE)
            if 'instance' in mode['averaging']:
                assert math.isclose(results['train_MAE_instance'], instance_MAE, abs_tol=0.01)
        if 'R2' in mode['metrics']:
            if 'macro' in mode['averaging']:
                assert math.isclose(results['train_R2_macro'], macro_R2)
            if 'micro' in mode['averaging']:
                assert math.isclose(results['train_R2_micro'], micro_R2)
            if 'instance' in mode['averaging']:
                assert math.isclose(results['train_R2_instance'], instance_R2, abs_tol=0.01)
        if 'RMSE' in mode['metrics']:
            if 'macro' in mode['averaging']:
                assert math.isclose(results['train_RMSE_macro'], macro_RMSE)
            if 'micro' in mode['averaging']:
                assert math.isclose(results['train_RMSE_micro'], micro_RMSE)
            if 'instance' in mode['averaging']:
                assert math.isclose(results['train_RMSE_instance'], instance_RMSE, abs_tol=0.01)