def write_features(self):
    """Saves features to file."""
    out_json = collections.OrderedDict()
    try:
        self.read_features()
    except (WrongFeaturesFormatError, FeaturesNotFound, NoFeaturesFileError):
        out_json = collections.OrderedDict({'metadata': {'versions': {'librosa': librosa.__version__, 'msaf': msaf.__version__, 'numpy': np.__version__}, 'timestamp': datetime.datetime.today().strftime('%Y/%m/%d %H:%M:%S')}})
        out_json['globals'] = {'dur': self.dur, 'sample_rate': self.sr, 'hop_length': self.hop_length, 'audio_file': self.file_struct.audio_file}
        out_json['est_beats'] = self._est_beats_times.tolist()
        out_json['est_beatsync_times'] = self._est_beatsync_times.tolist()
        if self._ann_beats_times is not None:
            out_json['ann_beats'] = self._ann_beats_times.tolist()
            out_json['ann_beatsync_times'] = self._ann_beatsync_times.tolist()
    except FeatureParamsError:
        with open(self.file_struct.features_file) as f:
            out_json = json.load(f)
    finally:
        out_json[self.get_id()] = {}
        out_json[self.get_id()]['params'] = {}
        for param_name in self.get_param_names():
            value = getattr(self, param_name)
            if hasattr(value, '__call__'):
                value = value.__name__
            else:
                value = str(value)
            out_json[self.get_id()]['params'][param_name] = value
        out_json[self.get_id()]['framesync'] = self._framesync_features.tolist()
        out_json[self.get_id()]['est_beatsync'] = self._est_beatsync_features.tolist()
        if self._ann_beatsync_features is not None:
            out_json[self.get_id()]['ann_beatsync'] = self._ann_beatsync_features.tolist()
        with open(self.file_struct.features_file, 'w') as f:
            json.dump(out_json, f, indent=2)