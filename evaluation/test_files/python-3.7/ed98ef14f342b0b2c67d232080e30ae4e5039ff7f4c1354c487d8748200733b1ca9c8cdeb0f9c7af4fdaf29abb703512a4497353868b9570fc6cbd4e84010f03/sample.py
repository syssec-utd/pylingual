"""This randomly samples a KGTK file, dividing it into an output file and an optional reject file.

A probability option, `--probability frac`, determines the probability that
an input record is passed to the standard output file. The probability ranges
from 0.0 to 1.0, with 1 being the default.  The number of output records
may not match the number of input records times the probability.

The probability value must not be negative, and it must not be greater than 1.

Alternatively, `--input-size N' and '--sample-size n' may be provided.  The
sampling probability will be computed as n/N. The number of output records may not
exactly match the desired count unless `--exact` is specified.  `--exact`
consumes more memory on large input files.

The input count, if specified, must be positive.  The desired count, if specified,
must be positive.

Finally, `--sample-size n` may be provided without `--input-size N`.  Exactly
`n` records will be selected, unless the input file has fewer than `n` records.
The selected records will be buffered in memory as the input file is processed,
so a significant amount of memory may be needed if `n` is large.

TODO: Optionally raise an exception if the sample size is greater than the
input size (prespecified or the actual number of input records, as applicable).

--mode=NONE is default.

TODO: Need KgtkWriterOptions

"""
from argparse import Namespace, SUPPRESS
import typing
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {'help': 'Randomly sample a KGTK file.', 'description': 'This utility randomly samples a KGTK file, dividing it into an optput file and an optional reject file. ' + 'The probability of an input record being passed to the output file is controlled by `--probability n`, where ' + '`n` ranges from 0 to 1. ' + '\n\nThis command defaults to --mode=NONE so it will work with TSV files that do not follow KGTK column naming conventions.' + '\n\nAdditional options are shown in expert help.\nkgtk --expert sample --help'}

def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions
    _expert: bool = parsed_shared_args._expert

    def h(msg: str) -> str:
        if _expert:
            return msg
        else:
            return SUPPRESS
    parser.add_input_file()
    parser.add_output_file()
    parser.add_output_file(who='The KGTK reject file for records that fail the filter.', dest='reject_file', options=['--reject-file'], metavar='REJECT_FILE', optional=True)
    parser.add_argument('--probability', dest='probability', type=float, default=1.0, help='The probability of passing an input record to the output file (default=%(default)d).')
    parser.add_argument('--seed', dest='seed', type=int, help='The optional random number generator seed (default=None).')
    parser.add_argument('--input-size', dest='input_size', type=int, help='The optional number of input records (default=None).')
    parser.add_argument('--sample-size', dest='sample_size', type=int, help='The optional desired number of output records (default=None).')
    parser.add_argument('--exact', dest='exact', metavar='True|False', help='Ensure that exactly the desired sample size is extracted when ' + '--input-size and --sample-size are supplied. (default=%(default)s).', type=optional_bool, nargs='?', const=True, default=False)
    parser.add_argument('--output-format', dest='output_format', help=h('The file format (default=kgtk)'), type=str, choices=KgtkWriter.OUTPUT_FORMAT_CHOICES)
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, default_mode=KgtkReaderMode.NONE, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles, output_file: KGTKFiles, reject_file: KGTKFiles, probability: float, seed: typing.Optional[int], input_size: typing.Optional[int], sample_size: typing.Optional[int], exact: bool, output_format: str, errors_to_stdout: bool=False, errors_to_stderr: bool=True, show_options: bool=False, verbose: bool=False, very_verbose: bool=False, **kwargs) -> int:
    from collections import deque
    from pathlib import Path
    from queue import PriorityQueue
    import random
    import sys
    import typing
    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions
    input_file_path: Path = KGTKArgumentParser.get_input_file(input_file)
    output_file_path: Path = KGTKArgumentParser.get_output_file(output_file)
    reject_file_path: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(reject_file, who='KGTK reject file')
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, mode=KgtkReaderMode.NONE)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)
    if show_options:
        print('--input-file=%s' % str(input_file_path), file=error_file, flush=True)
        print('--output-file=%s' % str(output_file_path), file=error_file, flush=True)
        if reject_file_path is not None:
            print('--reject-file=%s' % str(reject_file_path), file=error_file)
        print('--probability=%s' % str(probability), file=error_file, flush=True)
        if input_size is not None:
            print('--input-size=%d' % input_size, file=error_file, flush=True)
        if sample_size is not None:
            print('--sample-size=%d' % sample_size, file=error_file, flush=True)
        print('--exact=%s' % str(exact), file=error_file, flush=True)
        if seed is not None:
            print('--seed=%d' % seed, file=error_file, flush=True)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print('=======', file=error_file, flush=True)
    if probability < 0.0:
        raise KGTKException('The probability (%f) must not be negative.' % probability)
    if probability > 1.0:
        raise KGTKException('The probability (%f) must not be greater than 1.0.' % probability)
    if input_size is not None and input_size <= 0:
        raise KGTKException('The input count (%d) must be positive.' % input_size)
    if sample_size is not None and sample_size <= 0:
        raise KGTKException('The desired count (%d) must be positive.' % input_size)
    rg: random.Random = random.Random(seed)
    sample_set: typing.Optional[typing.Set[int]] = None
    priorityq: typing.Optional[PriorityQueue] = None
    if sample_size is not None:
        if input_size is None:
            priorityq = PriorityQueue()
        elif sample_size > input_size:
            probability = 1.0
        elif exact:
            sample_set = set(rg.sample(range(input_size), sample_size))
        else:
            probability = sample_size / input_size
    try:
        kr: KgtkReader = KgtkReader.open(input_file_path, options=reader_options, value_options=value_options, error_file=error_file, verbose=verbose, very_verbose=very_verbose)
        output_mode: KgtkWriter.Mode = KgtkWriter.Mode.NONE
        if kr.is_edge_file:
            output_mode = KgtkWriter.Mode.EDGE
            if verbose:
                print('Opening the output edge file: %s' % str(output_file_path), file=error_file, flush=True)
        elif kr.is_node_file:
            output_mode = KgtkWriter.Mode.NODE
            if verbose:
                print('Opening the output node file: %s' % str(output_file_path), file=error_file, flush=True)
        elif verbose:
            print('Opening the output file: %s' % str(output_file_path), file=error_file, flush=True)
        kw: KgtkWriter = KgtkWriter.open(kr.column_names, output_file_path, use_mgzip=reader_options.use_mgzip, mgzip_threads=reader_options.mgzip_threads, gzip_in_parallel=False, mode=output_mode, output_format=output_format, error_file=error_file, verbose=verbose, very_verbose=very_verbose)
        rkw: typing.Optional[KgtkWriter] = None
        if reject_file_path is not None:
            rkw = KgtkWriter.open(kr.column_names, reject_file_path, use_mgzip=reader_options.use_mgzip, mgzip_threads=reader_options.mgzip_threads, gzip_in_parallel=False, mode=output_mode, output_format=output_format, error_file=error_file, verbose=verbose, very_verbose=very_verbose)

        def copy_sample_set() -> typing.Tuple[int, int, int]:
            input_count: int = 0
            output_count: int = 0
            reject_count: int = 0
            row: typing.List[str]
            for row in kr:
                if input_count in sample_set:
                    kw.write(row)
                    output_count += 1
                elif rkw is not None:
                    rkw.write(row)
                    reject_count += 1
                input_count += 1
            return (input_count, output_count, reject_count)

        def copy_probably() -> typing.Tuple[int, int, int]:
            input_count: int = 0
            output_count: int = 0
            reject_count: int = 0
            row: typing.List[str]
            for row in kr:
                if probability > rg.random():
                    kw.write(row)
                    output_count += 1
                elif rkw is not None:
                    rkw.write(row)
                    reject_count += 1
                input_count += 1
            return (input_count, output_count, reject_count)

        def fill_priority_queue() -> typing.Tuple[int, int, int]:
            input_count: int = 0
            queued_count: int = 0
            reject_count: int = 0
            row: typing.List[str]
            for row in kr:
                priority = rg.random()
                priorityq.put((priority, row))
                queued_count += 1
                if queued_count > sample_size:
                    (priority, row) = priorityq.get()
                    queued_count -= 1
                    if rkw is not None:
                        rkw.write(row)
                        reject_count += 1
                input_count += 1
            return (input_count, queued_count, reject_count)

        def write_priority_queue(queued_count: int):
            priority: int
            row: typing.List[str]
            while queued_count > 0:
                queued_count -= 1
                (priority, row) = priorityq.get()
                kw.write(row)
        input_count: int
        output_count: int
        reject_count: int
        if priorityq is not None:
            (input_count, output_count, reject_count) = fill_priority_queue()
            write_priority_queue(output_count)
        else:
            (input_count, output_count, reject_count) = copy_sample_set() if sample_set is not None else copy_probably()
        kr.close()
        kw.close()
        if rkw is not None:
            rkw.close()
        if verbose:
            print('Read %d records, wrote %d records and %d reject records.' % (input_count, output_count, reject_count), file=error_file, flush=True)
    except SystemExit as e:
        raise KGTKException('Exit requested')
    except Exception as e:
        raise KGTKException(str(e))