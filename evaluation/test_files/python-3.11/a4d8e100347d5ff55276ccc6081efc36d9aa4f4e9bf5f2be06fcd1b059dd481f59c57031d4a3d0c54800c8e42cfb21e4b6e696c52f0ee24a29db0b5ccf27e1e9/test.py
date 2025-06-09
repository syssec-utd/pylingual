"""
Test a dataset using Pocketsphinx

:key_phrase str
    Key phrase composed of words from dictionary

:dict_file str
    Filename of dictionary with word pronunciations

:hmm_folder str
    Folder containing hidden markov model

:-th --threshold str 1e-90
    Threshold for activations

:-t --use-train
    Evaluate training data instead of test data

:-nf --no-filenames
    Don't show the names of files that failed

...
"""
import wave
from prettyparse import Usage
from subprocess import check_output, PIPE
from precise.pocketsphinx.listener import PocketsphinxListener
from precise.scripts.base_script import BaseScript
from precise.scripts.test import Stats
from precise.train_data import TrainData

class PocketsphinxTestScript(BaseScript):
    usage = Usage(__doc__) | TrainData.usage

    def __init__(self, args):
        super().__init__(args)
        self.listener = PocketsphinxListener(args.key_phrase, args.dict_file, args.hmm_folder, args.threshold)
        self.outputs = []
        self.targets = []
        self.filenames = []

    def get_stats(self):
        return Stats(self.outputs, self.targets, self.filenames)

    def run(self):
        args = self.args
        data = TrainData.from_both(args.tags_file, args.tags_folder, args.folder)
        print('Data:', data)
        ww_files, nww_files = data.train_files if args.use_train else data.test_files
        self.run_test(ww_files, 'Wake Word', 1.0)
        self.run_test(nww_files, 'Not Wake Word', 0.0)
        stats = self.get_stats()
        if not self.args.no_filenames:
            fp_files = stats.calc_filenames(False, True, 0.5)
            fn_files = stats.calc_filenames(False, False, 0.5)
            print('=== False Positives ===')
            print('\n'.join(fp_files))
            print()
            print('=== False Negatives ===')
            print('\n'.join(fn_files))
            print()
        print(stats.counts_str(0.5))
        print()
        print(stats.summary_str(0.5))

    def eval_file(self, filename) -> float:
        transcription = check_output(['pocketsphinx_continuous', '-kws_threshold', '1e-20', '-keyphrase', 'hey my craft', '-infile', filename], stderr=PIPE)
        return float(bool(transcription) and (not transcription.isspace()))

    def run_test(self, test_files, label_name, label):
        print()
        print('===', label_name, '===')
        for test_file in test_files:
            try:
                with wave.open(test_file) as wf:
                    frames = wf.readframes(wf.getnframes())
            except (OSError, EOFError):
                print('?', end='', flush=True)
                continue
            out = int(self.listener.found_wake_word(frames))
            self.outputs.append(out)
            self.targets.append(label)
            self.filenames.append(test_file)
            print('!' if out else '.', end='', flush=True)
        print()
main = PocketsphinxTestScript.run_main
if __name__ == '__main__':
    main()