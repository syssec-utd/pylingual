import warnings
import os
import json
import logging
import hashlib
from types import CodeType
from functools import reduce
from typing import Callable, Dict, List, Union
from omni.path import get_wrapped_callable
warnings.warn('Built-in Pipeline/Stage classes are deprecated. Use memori instead.', DeprecationWarning, stacklevel=2)

class Stage:
    """Stage object representing one node of a processing pipeline.

    Constructs a stage object that wraps a callable for use in a pipeline.
    When the `run` method is called the callable is executed and it's
    return value is stored in a result dictionary that can be accessed
    by the `results` property. The return value is parsed into this
    dictionary based on the list provide by `stage_outputs` (The position
    of each string in the list corresponds to each positional return
    value).

    Note: Stage objects convert their results to JSON so they can be
    written to file. This procedure will convert certain data structures
    (e.g. tuples to list, etc) and give unexpected results if not careful.
    In general, the current workaround is to use JSON compatible data
    structures for your function returns.

    Parameters
    ----------
    function_to_call: Callable
        A callable to wrap that the stage executes.
    stage_outputs: List[str]
        A list of strings to label each return value from the function_to_call.
    hash_output: str
        A directory that should be created or checked to cache the stage execution.
    stage_name: str
        Override the name for the stage.

    Methods
    -------
    run:
        Run the stage.
    """

    def __init__(self, function_to_call: Callable, stage_outputs: List=None, hash_output: str=None, stage_name: str=None, **kwargs):
        self.function_to_call = function_to_call
        func = get_wrapped_callable(self.function_to_call)
        num_of_input_args = func.__code__.co_argcount
        self.stage_inputs = list(func.__code__.co_varnames[:num_of_input_args])
        self.stage_outputs = stage_outputs if stage_outputs else list()
        self.stage_outputs = stage_outputs if type(stage_outputs) == list else [stage_outputs]
        self.stage_args = kwargs
        self.stage_input_args = dict()
        self.stage_name = stage_name if stage_name else function_to_call.__name__
        self.stage_results = dict()
        self.hash_output = hash_output
        if hash_output:
            self.stage_hash_location = os.path.join(hash_output, '%s.stage' % self.stage_name)
            self.input_hash_location = os.path.join(hash_output, '%s.inputs' % self.stage_name)
            self.output_hash_location = os.path.join(hash_output, '%s.outputs' % self.stage_name)

    def run(self, *args, force_skip_stage: bool=False, force_run_stage: bool=False, force_hash_write: bool=False, **kwargs) -> Dict:
        """Call function and save outputs in result dictionary.

        Runs the wrapped function_to_call with given args/kwargs.
        If any kwargs were specified on construction of the stage object,
        they will have precedence over any arguments specified in the
        calling `run` method. Hashes for the stage will also be checked to
        detect whether the stage should be run or not.

        Parameters
        ----------
        force_skip_stage: bool
            Specifies whether this stage should be forcefully skipped
        force_run_stage: bool
            Specifies whether this stage should be forcefully run. Has
            precedence over `force_skip_stage`
        force_hash_write: bool
            Specifies whether the hash for this stage should be written out
            even if the stage has not run.
        """
        self.stage_has_run = False
        for (i, name) in enumerate(self.inputs[:len(args)]):
            self.stage_input_args[name] = args[i]
        self.stage_input_args.update(kwargs)
        self.stage_input_args.update(self.stage_args)
        logging.info('Using these arguments for stage: {}\n{}'.format(self.stage_name, self.stage_input_args))
        stage_should_run = True
        if self.hash_output:
            hashes_matched = self._check_hashes()
            if hashes_matched:
                stage_should_run = False
        if force_skip_stage:
            logging.info('Force skip stage: %s', self.stage_name)
            stage_should_run = False
        if force_run_stage:
            logging.info('Force run stage: %s', self.stage_name)
            stage_should_run = True
        if stage_should_run:
            logging.info('Running stage: %s', self.stage_name)
            outputs = self.function_to_call(**self.stage_input_args)
            if not isinstance(outputs, (tuple, list)):
                outputs = [outputs]
            outputs = outputs[:len(self.stage_outputs)]
            for (stage_out, out) in zip(self.stage_outputs, outputs):
                self.stage_results[stage_out] = out
            self.stage_has_run = True
        else:
            logging.info('Skipping stage: %s execution...', self.stage_name)
            self._load_results_from_hash()
        if self.hash_output and (self.stage_has_run or force_hash_write):
            self._write_hashes()
        return self.stage_results

    def _load_results_from_hash(self) -> None:
        """Load output hash into results"""
        logging.info('Loading cached results...')
        with open(self.output_hash_location, 'r') as f:
            self.stage_results = self._unhash_files_in_dict(json.load(f), 'file')

    def _write_hashes(self) -> None:
        """Write hashes of stage to file"""
        self._write_stage_hash(self.stage_hash_location, self._get_function_byte_code)
        self._write_io_hash(self.input_hash_location, self.stage_input_args)
        self._write_io_hash(self.output_hash_location, self.stage_results)

    def _check_hashes(self) -> bool:
        """Check hashes of stage"""
        stage_match = self._check_stage_hash(self.stage_hash_location, self._get_function_byte_code)
        if not stage_match:
            logging.info('Stage hash for stage: %s did not match!', self.stage_name)
        input_match = self._check_io_hash(self.input_hash_location, self.stage_input_args)
        if not input_match:
            logging.info('Input hash for stage: %s did not match!', self.stage_name)
        output_hash_exists = os.path.exists(self.output_hash_location)
        if output_hash_exists:
            self._load_results_from_hash()
            output_match = self._check_io_hash(self.output_hash_location, self.stage_results)
            for key in self.stage_outputs:
                if key not in self.stage_results:
                    output_match = False
        else:
            output_match = False
        if not output_match:
            logging.info('Output hash for stage: %s did not match!', self.stage_name)
        return stage_match and input_match and output_hash_exists and output_match

    def _hash_files_in_dict(self, io_dict: Dict) -> Dict:
        """Replaces valid paths in Dict with a special 'file' dict.

        This method replaces valid, existing paths with a dict
        containing the following:

            { "file": file_path, "hash": sha256_hash }

        Parameters
        ----------
        io_dict: Dict
            Dictionary to replace paths with 'file' dict.

        Returns
        -------
        Dict
            A dictionary with all paths replace with 'file' dicts.
        """
        new_dict = io_dict.copy()
        for key in new_dict:
            value = new_dict[key]
            if isinstance(value, str) and os.path.isfile(value):
                file_hash = self._hash_file(value)
                new_dict[key] = {'file': value, 'hash': file_hash}
            elif isinstance(value, dict):
                new_dict[key] = self._hash_files_in_dict(value)
            elif isinstance(value, list):
                io_dict[key] = value.copy()
                for (i, v) in enumerate(value):
                    if type(v) == str and os.path.isfile(v):
                        file_hash = self._hash_file(v)
                        new_dict[key][i] = {'file': v, 'hash': file_hash}
                    elif isinstance(v, dict):
                        new_dict[key][i] = self._hash_files_in_dict(v)
        return new_dict

    def _unhash_files_in_dict(self, hash_dict: Dict, xtype: str='file') -> Dict:
        """Replaces special 'file' dict with hashes or files.

        This method replaces valid a dict containing the following:

            { "file": file_path, "hash": sha256_hash }

        with the value stored at the 'file' or 'hash' key.

        Parameters
        ----------
        hash_dict: Dict
            Dictionary to replace file dict with 'file' or 'hash'.
        xtype: str
            type to replace value with

        Returns
        -------
        Dict
            A dictionary with all file dicts replaced.
        """
        new_dict = hash_dict.copy()
        for key in new_dict:
            value = new_dict[key]
            if isinstance(value, dict):
                if 'file' in value and 'hash' in value:
                    if xtype == 'file':
                        new_dict[key] = value['file']
                    elif xtype == 'hash':
                        new_dict[key] = value['hash']
                    else:
                        raise ValueError('Invalid xtype.')
                else:
                    new_dict[key] = self._unhash_files_in_dict(value, xtype)
            elif isinstance(value, list):
                hash_dict[key] = value.copy()
                for (i, v) in enumerate(value):
                    if isinstance(v, dict):
                        new_dict[key][i] = self._unhash_files_in_dict({'v': v}, xtype)['v']
        return new_dict

    def _write_io_hash(self, hash_file: str, io_dict: Dict) -> None:
        """Write input/output hash to file.

        Parameters
        ----------
        hash_file: str
            Location of hash file to write to
        io_dict: Dict
            Input Dictionary
        """
        os.makedirs(os.path.dirname(hash_file), exist_ok=True)
        with open(hash_file, 'w') as f:
            json.dump(self._hash_files_in_dict(io_dict), f, sort_keys=True, indent=4)

    def _check_io_hash(self, hash_file: str, current_io_dict: Dict) -> bool:
        """Return if current input/output hash matches input dict of stage

        Parameters
        ----------
        hash_file: str
            Location of hash file to compare current input/output dict to.
        current_io_dict: Dict
            Input/Output dictionary to stage.
        """
        current_hash_dict = self._hash_files_in_dict(current_io_dict)
        if os.path.exists(hash_file):
            try:
                with open(hash_file, 'r') as f:
                    io_hash_from_file = self._unhash_files_in_dict(json.load(f), 'hash')
                    return io_hash_from_file == self._unhash_files_in_dict(current_hash_dict, 'hash')
            except json.JSONDecodeError:
                return False
        else:
            return False

    @staticmethod
    def _write_stage_hash(hash_file: str, stage_bytes: bytes) -> None:
        """Writes stage hash to file

        Parameters
        ----------
        hash_file: str
            Location of hash file to write to
        stage_bytes: bytes
            Byte value of stage function
        """
        os.makedirs(os.path.dirname(hash_file), exist_ok=True)
        with open(hash_file, 'wb') as f:
            f.write(stage_bytes)

    @staticmethod
    def _check_stage_hash(hash_file: str, current_stage_bytes: bytes) -> bool:
        """Return True/False if current stage hash matches current stage bytes

        Parameters
        ----------
        hash_file: str
            Location of hash file to compare current stage bytes to
        current_stage_bytes: bytes
            Byte value of stage function to call
        """
        if os.path.exists(hash_file):
            with open(hash_file, 'rb') as f:
                stage_hash_from_file = f.read()
                return stage_hash_from_file == current_stage_bytes
        else:
            return False

    @staticmethod
    def _hash_file(filename: str) -> str:
        """Hash file

        Parameters
        ----------
        filename: str
            Filename to hash.

        Returns
        -------
        str
            Hash of file.
        """
        hasher = hashlib.sha256()
        with open(filename, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()

    @property
    def _get_function_byte_code(self) -> bytes:
        """Get bytes of from function code object for hashing."""
        return get_func_hash(self.function_to_call)

    @property
    def inputs(self) -> List[str]:
        """List[str]: A list of input argument names for the stage."""
        return self.stage_inputs

    @property
    def outputs(self) -> List[str]:
        """List[str]: A list of output argument names for the stage."""
        return self.stage_outputs

    @property
    def args(self) -> Dict:
        """Dict: A dictionary of only the provided input arguments to the
        stage on construction."""
        return self.stage_args

    @property
    def input_args(self) -> Dict:
        """Dict: A dictionary of all input arguments to the stage. Is only
        populated after the `run` method is invoked."""
        return self.stage_input_args

    @property
    def results(self) -> Dict:
        """Dict: A dictionary of the output return values for the stage."""
        return self.stage_results

    @property
    def state(self) -> bool:
        """bool: A flag that specifies whether the current stage has been run
        (The callable has executed)."""
        return self.stage_has_run

class Pipeline:
    """This class defines a processing pipeline linking multiple Stages.

    The definition list accepts a tuple of Stage objects with the
    following syntax:

    Examples
    --------
    >>> # the start keyword is for stages that do not have input from other stages
    >>> spec = [("start", stage0), (stage0, stage1), ((stage0, stage1), stage2)]
    >>> # last entry has multiple inputs to another stage
    >>> # create the pipeline object
    >>> pipeline = Pipeline(spec)
    >>> # run the pipeline
    >>> pipeline.run()

    Stages are run in the order that they are defined in (In the example above: stage0 -> stage1 -> stage2).

    Parameters
    ----------
    definition: List
        A list of tuples containing Stage objects that define how a pipeline is connected.

    Methods
    -------
    run:
        Runs the pipeline.
    """

    def __init__(self, definition: List):
        self.definition = definition
        stages = list()
        for (input_stages, output_stages) in self.definition:
            if not isinstance(input_stages, tuple):
                input_stages = (input_stages,)
            stages.append(output_stages)
            stages.extend(input_stages)
        for stage in stages:
            if not (isinstance(stage, Stage) or stage == 'start'):
                raise ValueError('Found invalid input %s to pipeline definition!' % stage)
        self.pipeline_results = dict()

    def run(self, *args, **kwargs) -> None:
        """Runs the pipeline. Any stages linked to a "start" keyword accepts
        the input args/kwargs from this run method call.
        """
        for (input_stages, stage_to_run) in self.definition:
            if input_stages == 'start':
                stage_to_run.run(*args, **kwargs)
            else:
                input_args = dict()
                if not isinstance(input_stages, tuple):
                    input_stages = (input_stages,)
                combined_results = dict()
                for s in input_stages:
                    combined_results.update(s.results)
                combined_results.update(stage_to_run.args)
                for arg in stage_to_run.inputs:
                    try:
                        input_args[arg] = combined_results[arg]
                    except KeyError:
                        pass
                try:
                    stage_to_run.run(**input_args)
                except Exception as error:
                    print('\n\ninput_args: %s' % input_args)
                    print('\n\npipeline_results: %s\n\n' % combined_results)
                    raise error
            self.pipeline_results.update(stage_to_run.results)
        return self.pipeline_results

    @property
    def results(self) -> Dict:
        """Dict: A dictionary of the output return values for the pipeline."""
        return self._get_abspaths(self.pipeline_results)

    def _get_abspaths(self, dictionary: Dict):
        """Convert all valid paths in dictionary to absolute path"""
        new_dict = dictionary.copy()
        for key in new_dict:
            value = new_dict[key]
            if isinstance(value, str) and os.path.isfile(value):
                new_dict[key] = os.path.abspath(value)
            elif isinstance(value, dict):
                new_dict[key] = self._get_abspaths(value)
        return new_dict

def redefine_result_key(dictionary: Dict, from_key: str, to_key: str) -> Dict:
    """Redefines a result key in the dictionary to a different key.

    Examples
    --------
    >>> dictionary = {"hello": 1, "test": 2}
    >>> new_dict = redefine_result_key(dictionary, "hello", "testing")
    >>> # new_dict is now: {"testing": 1, "test": 2}

    Parameters
    ----------
    dictionary: Dict
        Dictionary to change key of.
    from_key: str
        Key to change.
    to_key: str
        Key to replace with.

    Returns
    -------
    Dict
        New dictionary with replaced keys.
    """
    new_dict = dictionary.copy()
    new_dict[to_key] = dictionary[from_key]
    del new_dict[from_key]
    return new_dict

def get_func_hash(func: Union[Callable, CodeType]) -> bytes:
    """Hashes a function into unique bytes.

    This function grabs relevant bytes from the
    function code object for hashing. It is ordered as
    the following:

        consts, methods, code

    In consts, the doc sting of the code object is removed
    and any embedded code objects are appended to the end
    of bytes array.

    Parameters
    ----------
    func: Union[Callable, CodeType]
        Function to hash.

    Returns
    -------
    bytes
        Unique bytes representing the function.
    """
    if '__code__' in func.__dir__():
        func = get_wrapped_callable(func)
        consts = func.__code__.co_consts[1:]
        methods = func.__code__.co_names
        code = func.__code__.co_code
        code_object_type = type(func.__code__)
    else:
        consts = func.co_consts[1:]
        methods = func.co_names
        code = func.co_code
        code_object_type = type(func)
    filtered_consts = list()
    embedded_code_objects = list()
    for c in consts:
        if code_object_type == type(c):
            embedded_code_objects.append(get_func_hash(c))
        else:
            filtered_consts.append(c)
    consts = tuple(filtered_consts)
    consts = str(consts).encode('utf-8')
    methods = str(methods).encode('utf-8')
    bytes_list = [consts, methods, code] + embedded_code_objects
    return reduce(lambda x, y: x + y, bytes_list)