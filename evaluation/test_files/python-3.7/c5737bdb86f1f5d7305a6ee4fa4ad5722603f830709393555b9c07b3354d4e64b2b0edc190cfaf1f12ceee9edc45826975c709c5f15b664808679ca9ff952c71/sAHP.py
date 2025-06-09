"""sAHP eCode"""
'\nCopyright (c) 2022, EPFL/Blue Brain Project\n\n This file is part of BluePyEfe <https://github.com/BlueBrain/BluePyEfe>\n\n This library is free software; you can redistribute it and/or modify it under\n the terms of the GNU Lesser General Public License version 3.0 as published\n by the Free Software Foundation.\n\n This library is distributed in the hope that it will be useful, but WITHOUT\n ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS\n FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more\n details.\n\n You should have received a copy of the GNU Lesser General Public License\n along with this library; if not, write to the Free Software Foundation, Inc.,\n 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.\n'
import logging
import numpy
from ..recording import Recording
from .tools import scipy_signal2d
logger = logging.getLogger(__name__)

class SAHP(Recording):

    def __init__(self, config_data, reader_data, protocol_name='sAHP', efel_settings=None):
        super(SAHP, self).__init__(config_data, reader_data, protocol_name)
        self.ton = None
        self.tmid = None
        self.tmid2 = None
        self.toff = None
        self.tend = None
        self.amp = None
        self.amp2 = None
        self.hypamp = None
        self.dt = None
        self.amp_rel = None
        self.amp2_rel = None
        self.hypamp_rel = None
        if self.t is not None and self.current is not None:
            self.interpret(self.t, self.current, self.config_data, self.reader_data)
        if self.voltage is not None:
            self.compute_spikecount(efel_settings)
        self.export_attr = ['ton', 'tmid', 'tmid2', 'toff', 'tend', 'amp', 'amp2', 'hypamp', 'dt', 'amp_rel', 'amp2_rel', 'hypamp_rel']

    def get_stimulus_parameters(self):
        """Returns the eCode parameters"""
        ecode_params = {'delay': self.ton, 'tmid': self.tmid, 'tmid2': self.tmid2, 'toff': self.toff, 'amp': self.amp2, 'long_amp': self.amp, 'thresh_perc': self.amp2_rel, 'duration': self.tmid2 - self.tmid, 'totduration': self.tend}
        return ecode_params

    def interpret(self, t, current, config_data, reader_data):
        """Analyse a current array and extract from it the parameters
        needed to reconstruct the array"""
        self.dt = t[1]
        smooth_current = scipy_signal2d(current, 85)
        self.set_timing_ecode(['ton', 'tmid', 'tmid2', 'toff'], config_data)
        hypamp_value = numpy.median(numpy.concatenate((smooth_current[:self.ton], smooth_current[self.toff:])))
        self.set_amplitudes_ecode('hypamp', config_data, reader_data, hypamp_value)
        amp_value = numpy.median(numpy.concatenate((smooth_current[self.ton:self.tmid], smooth_current[self.tmid2:self.toff]))) - self.hypamp
        self.set_amplitudes_ecode('amp', config_data, reader_data, amp_value)
        amp2_value = numpy.median(smooth_current[self.tmid:self.tmid2]) - self.hypamp
        self.set_amplitudes_ecode('amp2', config_data, reader_data, amp2_value)
        for name_timing in ['ton', 'tmid', 'tmid2', 'toff']:
            self.timing_index_to_ms(name_timing, t)
        self.tend = len(t) * self.dt

    def generate(self):
        """Generate the current array from the parameters of the ecode"""
        ton = int(self.ton / self.dt)
        tmid = int(self.tmid / self.dt)
        tmid2 = int(self.tmid2 / self.dt)
        toff = int(self.toff / self.dt)
        time = numpy.arange(0.0, self.tend, self.dt)
        current = numpy.full(time.shape, self.hypamp)
        current[ton:tmid] += self.amp
        current[tmid2:toff] += self.amp
        current[tmid:tmid2] += self.amp2
        return (time, current)

    def compute_relative_amp(self, amp_threshold):
        self.amp_rel = 100.0 * self.amp / amp_threshold
        self.amp2_rel = 100.0 * self.amp2 / amp_threshold
        self.hypamp_rel = 100.0 * self.hypamp / amp_threshold

    def in_target(self, target, tolerance):
        """Returns a boolean. True if the amplitude of the eCode is close to
        target and False otherwise."""
        if numpy.abs(target - self.amp2_rel) < tolerance:
            return True
        else:
            return False

    def get_plot_amplitude_title(self):
        return ' ({:.01f}%/{:.01f}%)'.format(self.amp_rel, self.amp2_rel)