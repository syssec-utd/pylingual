import argparse
import logging
import os
from typing import List, Optional
import numpy as np
import torch as pt
from . import arguments
from . import constants as C
from . import data_io
from . import utils
from .log import setup_main_logger
from .model import SockeyeModel, load_model
from .vocab import Vocab
from .utils import check_condition
from .knn import KNNConfig, get_state_store_path, get_word_store_path, get_config_path
logger = logging.getLogger(__name__)

class NumpyMemmapStorage:
    """
    Wraps a numpy memmap as a datastore for decoder state vectors.

    :param file_name: disk file path to store the memory-mapped file
    :param num_dim: number of dimensions of the vectors in the data store
    :param dtype: data type of the vectors in the data store
    """

    def __init__(self, file_name: str, num_dim: int, dtype: np.dtype) -> None:
        self.file_name = file_name
        self.num_dim = num_dim
        self.dtype = dtype
        self.block_size = -1
        self.mmap = None
        self.tail_idx = 0
        self.size = 0

    def open(self, initial_size: int, block_size: int) -> None:
        """Create a memmap handle and initialize its sizes."""
        self.mmap = np.memmap(self.file_name, dtype=self.dtype, mode='w+', shape=(initial_size, self.num_dim))
        self.size = initial_size
        self.block_size = block_size

    def add(self, array: np.ndarray) -> None:
        """
        It turns out that numpy memmap actually cannot be re-sized.
        So we have to pre-estimate how many entries we need and put it down as initial_size.
        If we end up adding more entries to the memmap than initially claimed, we'll have to bail out.

        :param array: the array of states to be added.
        """
        assert self.mmap is not None
        (num_entries, num_dim) = array.shape
        assert num_dim == self.num_dim
        if self.tail_idx + num_entries > self.size:
            logger.warning(f'Trying to write {num_entries} entries into a numpy memmap that ' + f'has size {self.size} and already has {self.tail_idx} entries. Nothing is written.')
        else:
            start = self.tail_idx
            end = self.tail_idx + num_entries
            self.mmap[start:end] = array
            self.tail_idx += num_entries

class DecoderStateGenerator:
    """
    Generate decoder states by using a translation model to force-decode a parallel dataset.

    :param model: Sockeye translation model used to generate the states.
    :param source_vocabs: source vocabs for the translation model.
    :param target_vocabs: target vocabs for the translation model.
    :param output_dir: path to the memmap (directory) storing decoder states.
    :param max_seq_len_source: maximum source length for decoding.
    :param max_seq_len_target: maximum source length for decoding.
    :param state_data_type: data type for storing decoder states.
    :param word_data_type: data type for storing word indexes.
    :param device: device (cpu/gpu) for decoding.
    """

    def __init__(self, model: SockeyeModel, source_vocabs: List[Vocab], target_vocabs: List[Vocab], output_dir: str, max_seq_len_source: int, max_seq_len_target: int, state_data_type: str, word_data_type: str, device: pt.device) -> None:
        self.model = model
        self.source_vocabs = source_vocabs
        self.target_vocabs = target_vocabs
        self.device = device
        self.traced_model = None
        self.max_seq_len_source = max_seq_len_source
        self.max_seq_len_target = max_seq_len_target
        self.output_dir = output_dir
        self.state_store_file = None
        self.words_store_file = None
        self.num_states = 0
        self.dimension = None
        self.state_data_type = utils.get_numpy_dtype(state_data_type)
        self.word_data_type = utils.get_numpy_dtype(word_data_type)

    @staticmethod
    def probe_token_count(target_path: str, max_seq_len: int) -> int:
        """Count the number of tokens in the file at `target_path`, with each line truncated at `max_seq_len`."""
        token_count = 0
        with open(target_path, 'r') as f:
            for line in f:
                token_count += min(len(line.split()) + 1, max_seq_len)
        return token_count

    def init_store_file(self, initial_size: int) -> None:
        """Initialize the memory map files."""
        self.dimension = self.model.config.config_decoder.model_size
        self.state_store_file = NumpyMemmapStorage(get_state_store_path(self.output_dir), self.dimension, self.state_data_type)
        self.words_store_file = NumpyMemmapStorage(get_word_store_path(self.output_dir), 1, self.word_data_type)
        self.state_store_file.open(initial_size, 1)
        self.words_store_file.open(initial_size, 1)

    def generate_states_and_store(self, sources: List[str], targets: List[str], batch_size: int) -> None:
        """
        Generate decoder states by force-decoding the sentence pairs in `sources` and `targets` with a NMT model.

        :param sources: list of source segments.
        :param targets: list of target segments.
        :param batch_size: number of sentence pairs to decode at once.
        """
        assert self.state_store_file != None, 'You should call probe_token_count first to initialize the store files.'
        data_iter = data_io.get_scoring_data_iters(sources=sources, targets=targets, source_vocabs=self.source_vocabs, target_vocabs=self.target_vocabs, batch_size=batch_size, max_seq_len_source=self.max_seq_len_source, max_seq_len_target=self.max_seq_len_target)
        with pt.inference_mode():
            for (batch_no, batch) in enumerate(data_iter, 1):
                if (batch_no + 1) % 1000 == 0:
                    logger.debug('At batch number {0}'.format(batch_no + 1))
                batch = batch.load(self.device)
                model_inputs = (batch.source, batch.source_length, batch.target, batch.target_length)
                if self.traced_model is None:
                    trace_inputs = {'get_decoder_states': model_inputs}
                    self.traced_model = pt.jit.trace_module(self.model, trace_inputs, strict=False)
                decoder_states = self.traced_model.get_decoder_states(*model_inputs)
                pad_mask = (batch.target != C.PAD_ID)[:, :, 0]
                flat_target = batch.target[pad_mask].cpu().detach().numpy()
                flat_states = decoder_states[pad_mask].cpu().detach().numpy()
                self.state_store_file.add(flat_states)
                self.words_store_file.add(flat_target)

    def save_config(self):
        """
        Save a config file with information of the data store.
        """
        config = KNNConfig(index_size=self.num_states, dimension=self.dimension, state_data_type=utils.dtype_to_str(self.state_data_type), word_data_type=utils.dtype_to_str(self.word_data_type), index_type='', train_data_size=-1)
        config.save(get_config_path(self.output_dir))

def store(args: argparse.Namespace):
    """Build a data store with an existing model and a parallel corpus."""
    use_cpu = args.use_cpu
    if not pt.cuda.is_available():
        logger.info('CUDA not available, using cpu')
        use_cpu = True
    device = pt.device('cpu') if use_cpu else pt.device('cuda', args.device_id)
    logger.info(f'Scoring device: {device}')
    (model, source_vocabs, target_vocabs) = load_model(args.model, device=device, dtype=args.dtype)
    model.eval()
    max_seq_len_source = model.max_supported_len_source
    max_seq_len_target = model.max_supported_len_target
    if args.max_seq_len is not None:
        max_seq_len_source = min(args.max_seq_len[0] + C.SPACE_FOR_XOS, max_seq_len_source)
        max_seq_len_target = min(args.max_seq_len[1] + C.SPACE_FOR_XOS, max_seq_len_target)
    sources = [args.source] + args.source_factors
    sources = [str(os.path.abspath(source)) for source in sources]
    targets = [args.target] + args.target_factors
    targets = [str(os.path.abspath(target)) for target in targets]
    check_condition(len(targets) == model.num_target_factors, 'Number of target inputs/factors provided (%d) does not match number of target factors required by the model (%d)' % (len(targets), model.num_target_factors))
    if args.state_dtype is None:
        args.state_dtype = utils.dtype_to_str(model.dtype)
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
    elif os.path.isfile(args.output_dir):
        logging.error(f'{args.output_dir} already exists as a file')
    generator = DecoderStateGenerator(model, source_vocabs, target_vocabs, args.output_dir, max_seq_len_source, max_seq_len_target, args.state_dtype, C.KNN_WORD_DATA_STORE_DTYPE, device)
    generator.num_states = DecoderStateGenerator.probe_token_count(targets[0], max_seq_len_target)
    generator.init_store_file(generator.num_states)
    generator.generate_states_and_store(sources, targets, args.batch_size)
    generator.save_config()

def main():
    params = arguments.ConfigArgumentParser(description='CLI to generate decoder states from parallel data with a trained model, and build a data store from it.')
    arguments.add_state_generation_args(params)
    args = params.parse_args()
    check_condition(args.batch_type == C.BATCH_TYPE_SENTENCE, 'Batching by number of words is not supported')
    setup_main_logger(file_logging=False, console=not args.quiet, level=args.loglevel)
    utils.log_basic_info(args)
    store(args)
if __name__ == '__main__':
    main()