""" Runner for onefile program tests of Nuitka.

These tests aim at showing that one specific functions work in onefile
mode, trying to find issues with that form of packaging.

"""
import os
import sys
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__.replace('\\', os.sep))), '..', '..')))
from nuitka.tools.testing.Common import checkLoadedFileAccesses, checkRequirements, compareWithCPython, createSearchMode, displayFileContents, displayRuntimeTraces, reportSkip, scanDirectoryForTestCases, setup, test_logger
from nuitka.tools.testing.RuntimeTracing import doesSupportTakingRuntimeTrace, getRuntimeTraceOfLoadedFiles
from nuitka.utils.Timing import TimerReport
from nuitka.utils.Utils import isMacOS

def displayError(dirname, filename):
    assert dirname is None
    inclusion_log_path = filename[:-3] + '.py.inclusion.log'
    displayFileContents('inclusion log', inclusion_log_path)

def main():
    python_version = setup(suite='onefile', needs_io_encoding=True)
    search_mode = createSearchMode()
    for filename in scanDirectoryForTestCases('.'):
        active = search_mode.consider(dirname=None, filename=filename)
        if not active:
            continue
        extra_flags = ['expect_success', 'remove_output', '--keep-binary', 'cpython_cache', 'timing', 'ignore_warnings']
        if filename == 'KeyboardInterruptTest.py':
            if isMacOS():
                reportSkip('Exit code from KeyboardInterrupt on macOS is not yet good.', '.', filename)
                continue
            if python_version < (3,):
                reportSkip('Python2 reports KeyboardInterrupt, but too late', '.', filename)
                continue
            if os.name == 'nt':
                reportSkip('Testing cannot send KeyboardInterrupt on Windows yet', '.', filename)
                continue
            extra_flags.append('--send-ctrl-c')
        (requirements_met, error_message) = checkRequirements(filename)
        if not requirements_met:
            reportSkip(error_message, '.', filename)
            continue
        test_logger.info('Consider output of onefile mode compiled program: %s' % filename)
        compareWithCPython(dirname=None, filename=filename, extra_flags=extra_flags, search_mode=search_mode, needs_2to3=False, on_error=displayError)
        binary_filename = filename[:-3] + ('.exe' if os.name == 'nt' else '.bin')
        try:
            if not doesSupportTakingRuntimeTrace():
                test_logger.info('Runtime traces are not possible on this machine.')
                continue
            if filename == 'KeyboardInterruptTest.py':
                test_logger.info('Runtime traces are not taken for case that needs killing.')
                continue
            with TimerReport('Determining run time loaded files took %.2f', logger=test_logger):
                loaded_filenames = getRuntimeTraceOfLoadedFiles(logger=test_logger, command=[binary_filename])
            illegal_accesses = checkLoadedFileAccesses(loaded_filenames=loaded_filenames, current_dir=os.getcwd())
            if illegal_accesses:
                displayError(None, filename)
                displayRuntimeTraces(test_logger, binary_filename)
                test_logger.warning("Should not access these file(s): '%s'." % ','.join(illegal_accesses))
                search_mode.onErrorDetected(1)
        finally:
            os.unlink(binary_filename)
    search_mode.finish()
if __name__ == '__main__':
    main()