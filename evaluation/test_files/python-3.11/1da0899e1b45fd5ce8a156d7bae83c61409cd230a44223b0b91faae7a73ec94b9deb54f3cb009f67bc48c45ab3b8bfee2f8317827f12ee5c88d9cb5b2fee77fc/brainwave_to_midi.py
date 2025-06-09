"""
@author: NeuroBrave
this code  is distributed under BSD licence.

this code requires: 
    active internet conenction 
    subscription to NeuroSpeed.io service.
    active EEG stream from neuroSpeed cloud.
"""
GRAPH_ENGAGEMENT = False
import rtmidi
import re
import sys
from pathlib import Path
import os
from neurospeed.auth.auth_as_user_handler import Auth_AS_User_Handler
from neurospeed.api_socket_handlers.user_room_as_user_handler import UserRoom_AS_User_Handler
from neurospeed.utils.helper_service import UtilService
global user_auth
import statistics
import queue
import time
from vispy import gloo, app, visuals
import numpy as np
import math
from seaborn import color_palette
from scipy.signal import lfilter, lfilter_zi
from mne.filter import create_filter
import socket
import json
global brain_wave_power_max
global midiout
brain_wave_power_max = 0
stream_q_EEG = queue.Queue(-1)
VERT_SHADER = '\n#version 120\n// y coordinate of the position.\nattribute float a_position;\n// row, col, and time index.\nattribute vec3 a_index;\nvarying vec3 v_index;\n// 2D scaling factor (zooming).\nuniform vec2 u_scale;\n// Size of the table.\nuniform vec2 u_size;\n// Number of samples per signal.\nuniform float u_n;\n// Color.\nattribute vec3 a_color;\nvarying vec4 v_color;\n// Varying variables used for clipping in the fragment shader.\nvarying vec2 v_position;\nvarying vec4 v_ab;\nvoid main() {\n    float n_rows = u_size.x;\n    float n_cols = u_size.y;\n    // Compute the x coordinate from the time index.\n    float x = -1 + 2*a_index.z / (u_n-1);\n    vec2 position = vec2(x - (1 - 1 / u_scale.x), a_position);\n    // Find the affine transformation for the subplots.\n    vec2 a = vec2(1./n_cols, 1./n_rows)*.9;\n    vec2 b = vec2(-1 + 2*(a_index.x+.5) / n_cols,\n                    -1 + 2*(a_index.y+.5) / n_rows);\n    // Apply the static subplot transformation + scaling.\n    gl_Position = vec4(a*u_scale*position+b, 0.0, 1.0);\n    v_color = vec4(a_color, 1.);\n    v_index = a_index;\n    // For clipping test in the fragment shader.\n    v_position = gl_Position.xy;\n    v_ab = vec4(a, b);\n}\n'
FRAG_SHADER = '\n#version 120\nvarying vec4 v_color;\nvarying vec3 v_index;\nvarying vec2 v_position;\nvarying vec4 v_ab;\nvoid main() {\n    gl_FragColor = v_color;\n    // Discard the fragments between the signals (emulate glMultiDrawArrays).\n    if ((fract(v_index.x) > 0.) || (fract(v_index.y) > 0.))\n        discard;\n    // Clipping test.\n    vec2 test = abs((v_position.xy-v_ab.zw)/v_ab.xy);\n    if ((test.x > 1))\n        discard;\n}\n'
global UPDATE_TIMER
UPDATE_TIMER = 1.5
window_title = 'use mouse wheel for vertical zoom, +/- keys for horizontal zoom. D key toggles high pass filter'

class Canvas(app.Canvas):

    def __init__(self, stream_info, scale=1000, filt=True):
        app.Canvas.__init__(self, title=window_title, keys='interactive')
        window = 10
        self.sfreq = stream_info['srate']
        self.n_chans = stream_info['n_chans']
        ch_names = stream_info['ch_names']
        n_samples = int(self.sfreq * window)
        n_rows = self.n_chans
        n_cols = 1
        m = n_rows * n_cols
        n = n_samples
        amplitudes = np.zeros((m, n)).astype(np.float32)
        y = amplitudes
        color = color_palette('RdBu_r', n_rows)
        color = np.repeat(color, n, axis=0).astype(np.float32)
        index = np.c_[np.repeat(np.repeat(np.arange(n_cols), n_rows), n), np.repeat(np.tile(np.arange(n_rows), n_cols), n), np.tile(np.arange(n), m)].astype(np.float32)
        self.program = gloo.Program(VERT_SHADER, FRAG_SHADER)
        self.program['a_position'] = y.reshape(-1, 1)
        self.program['a_color'] = color
        self.program['a_index'] = index
        self.program['u_scale'] = (1.0, 1.0)
        self.program['u_size'] = (n_rows, n_cols)
        self.program['u_n'] = n
        self.font_size = 24.0
        self.names = []
        self.quality = []
        for ii in range(self.n_chans):
            text = visuals.TextVisual(ch_names[ii], bold=True, color='white')
            self.names.append(text)
            text = visuals.TextVisual('', bold=True, color='white')
            self.quality.append(text)
        self.quality_colors = color_palette('RdYlGn', 11)[::-1]
        self.scale = scale
        self.n_samples = n_samples
        self.filt = filt
        self.af = [1.0]
        self.data_f = np.zeros((n_samples, self.n_chans))
        self.data = np.zeros((n_samples, self.n_chans))
        self.bf = create_filter(self.data_f.T, self.sfreq, None, 10.0, method='fir')
        zi = lfilter_zi(self.bf, self.af)
        self.filt_state = np.tile(zi, (self.n_chans, 1)).transpose()
        self._timer = app.Timer(UPDATE_TIMER, connect=self.on_timer, start=True)
        gloo.set_viewport(0, 0, *self.physical_size)
        gloo.set_state(clear_color='black', blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))
        self.show()

    def on_key_press(self, event):
        if event.key.name == 'D':
            self.filt = not self.filt
        if event.key.name in ['+', '-']:
            if event.key.name == '+':
                dx = -0.05
            else:
                dx = 0.05
            scale_x, scale_y = self.program['u_scale']
            scale_x_new, scale_y_new = (scale_x * math.exp(1.0 * dx), scale_y * math.exp(0.0 * dx))
            self.program['u_scale'] = (max(1, scale_x_new), max(1, scale_y_new))
            self.update()

    def on_mouse_wheel(self, event):
        dx = np.sign(event.delta[1]) * 0.05
        scale_x, scale_y = self.program['u_scale']
        scale_x_new, scale_y_new = (scale_x * math.exp(0.0 * dx), scale_y * math.exp(2.0 * dx))
        self.program['u_scale'] = (max(1, scale_x_new), max(0.01, scale_y_new))
        self.update()

    def on_timer(self, event):
        """Add some data at the end of each signal (real-time signals)."""
        samples = stream_q_EEG.get(timeout=1)
        if True:
            samples = np.array(samples)[:, ::-1]
            self.data = np.vstack([self.data, samples])
            self.data = self.data[-self.n_samples:]
            filt_samples, self.filt_state = lfilter(self.bf, self.af, samples, axis=0, zi=self.filt_state)
            self.data_f = np.vstack([self.data_f, filt_samples])
            self.data_f = self.data_f[-self.n_samples:]
            if self.filt:
                plot_data = self.data_f / self.scale
            elif not self.filt:
                plot_data = (self.data - self.data.mean(axis=0)) / self.scale
            sd = np.std(plot_data[-int(self.sfreq):], axis=0)[::-1] * self.scale
            co = np.int32(np.tanh((sd - 30) / 15) * 5 + 5)
            for ii in range(self.n_chans):
                self.quality[ii].text = '%.2f' % sd[ii]
                self.quality[ii].color = self.quality_colors[co[ii]]
                self.quality[ii].font_size = 12 + co[ii]
                self.names[ii].font_size = 12 + co[ii]
                self.names[ii].color = self.quality_colors[co[ii]]
            self.program['a_position'].set_data(plot_data.T.ravel().astype(np.float32))
            self.update()

    def on_resize(self, event):
        vp = (0, 0, self.physical_size[0], self.physical_size[1])
        self.context.set_viewport(*vp)
        for ii, t in enumerate(self.names):
            t.transforms.configure(canvas=self, viewport=vp)
            t.pos = (self.size[0] * 0.025, (ii + 0.5) / self.n_chans * self.size[1])
        for ii, t in enumerate(self.quality):
            t.transforms.configure(canvas=self, viewport=vp)
            t.pos = (self.size[0] * 0.975, (ii + 0.5) / self.n_chans * self.size[1])

    def on_draw(self, event):
        gloo.clear()
        gloo.set_viewport(0, 0, *self.physical_size)
        self.program.draw('line_strip')
        [t.draw() for t in self.names + self.quality]
global EEG_sensor_information
EEG_sensor_information = None

def EEG_processing_handler1(payload):
    global brain_wave_power_max
    global EEG_sensor_information
    global midiout
    if EEG_sensor_information == None:
        EEG_sensor_information = {}
        EEG_sensor_information['EEG_channel_names'] = payload['sensor_info']['channel_map']
        EEG_sensor_information['EEG_channel_num'] = len(payload['sensor_info']['channel_map'])
        EEG_sensor_information['sampling_frequency'] = payload['sensor_info']['sampling_frequency']
    electrode_select = [0]
    if 'all' in electrode_select:
        brain_wave_power = statistics.mean(payload['output']['brainwave_power']['alpha'])
    else:
        brain_wave_power = statistics.mean([payload['output']['brainwave_power']['alpha'][electrode_index] for electrode_index in electrode_select])
    if brain_wave_power > brain_wave_power_max:
        brain_wave_power_max = brain_wave_power
    if brain_wave_power_max > 0:
        output_value = int(127 * brain_wave_power / brain_wave_power_max)
    else:
        output_value = 0
    if output_value > 127:
        output_value = 127
    midi_Control_Change_number = 7
    print('sent CC value: ', output_value)
    midiout.send_message([88, 11, 64])
    if GRAPH_ENGAGEMENT:
        values = []
        for i in range(100):
            values.append([brain_wave_power])
        stream_q_EEG.put(values, timeout=1)

def EEG_processing_handler2(payload):
    pass

def customer_gamepad_msg_handler_function(payload):
    print('customer_gamepad_msg_handler_function')
    pass

def customer_user_data_msg_handler_function(payload):
    print('customer_user_data_msg_handler_function')
    pass
generic_handler = {'eeg': [EEG_processing_handler1, EEG_processing_handler2], 'gamepad': [customer_gamepad_msg_handler_function], 'user_data': [customer_user_data_msg_handler_function]}

def user_data_external_handler(payload):
    username = user_auth.get_username()
    stream_id = payload['stream_id']
    device_type = payload['device_type']
    hia_id = payload['hia_id']
    sensor_info = payload['sensor_info']
    device_type = device_type.lower()
    handler_functions = generic_handler[device_type]
    for func in handler_functions:
        func(payload)

def user_device_event_external_handler(payload):
    print('event: ', payload)
    pass
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
if available_ports:
    connected = False
    while not connected:
        print('Available MIDI output ports in the system: ')
        print(available_ports)
        print('Select port by typing  in port number')
        port_number = int(re.findall('[0-9]+', input())[0])
        if port_number in range(0, len(available_ports)):
            print('selected port ', available_ports[port_number], ' opening...')
            midiout.open_port(port_number)
            connected = True
            time.sleep(3)
        else:
            print('incorrect input, try again:')
else:
    print('no MIDI outputs found in system, terminating the program.')
    del midiout
    sys.exit()

def main():
    global user_auth
    user1_config_path = os.path.join(str(Path().absolute()), 'config\\', 'hia_config1.json')
    print(user1_config_path)
    config_user1 = UtilService.load_config_file(user1_config_path)
    user_auth = Auth_AS_User_Handler(config_user1)
    user_auth.login()
    userRoom = UserRoom_AS_User_Handler(user_auth)
    userRoom.set_data_external_handler(user_data_external_handler)
    userRoom.set_device_events_external_handler(user_device_event_external_handler)
    userRoom.connect()
    time.sleep(5)
    print(EEG_sensor_information)
    if GRAPH_ENGAGEMENT:
        stream_info = {'n_chans': 1, 'srate': 100, 'ch_names': ['engamement']}
        Canvas(stream_info)
        app.run()
if __name__ == '__main__':
    main()