import numpy as np
import warnings
from numba import njit
warnings.filterwarnings('ignore')
import os
import sys
from _setup_ import game_name, time_run_game
sys.path.append(os.path.abspath(f'base/{game_name}'))
from env import *

def file_temp_to_action_Phong_130922(state, file_temp):
    a = getValidActions(state)
    a = np.where(a == 1)[0]
    RELU = np.ones(len(state))
    matrix_new = np.matmul(RELU, file_temp)
    list_val_action = matrix_new[a]
    action = a[np.argmax(list_val_action)]
    return action

def test(state, file_temp, file_per):
    if len(file_temp) < 2:
        player = 'Phong_130922'
        path_save_player = f'system/Agent/{player}/Data/{game_name}_{time_run_game}/'
        model_manh_nhat = np.load(f'{path_save_player}p_model_manh_nhat.npy', allow_pickle=True)[0][0][-1]
        file_temp = model_manh_nhat
    action = file_temp_to_action_Phong_130922(state, file_temp)
    return (action, file_temp, file_per)

def test2(state, file_temp, file_per, file_per_2):
    action = file_temp_to_action_Phong_130922(state, file_per_2)
    return (action, file_temp, file_per, file_per_2)