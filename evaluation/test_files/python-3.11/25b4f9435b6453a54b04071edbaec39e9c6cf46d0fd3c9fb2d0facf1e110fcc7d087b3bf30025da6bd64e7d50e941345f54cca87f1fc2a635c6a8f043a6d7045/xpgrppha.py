from __future__ import print_function, division
import os
import ixpeobssim.utils.system_ as system_
from ixpeobssim.utils.logging_ import logger
__description__ = 'Small Python wrapper around the HEASARC GRPPHA utility, see\nhttps://heasarc.gsfc.nasa.gov/ftools/caldb/help/grppha.txt\n\nIn a nutshell, you should be able to pass any command that you would pass to\ngrppha interactively via the --comm command-line switch, e.g.\n\n> xpgrppha.py --comm "group min 100" pha1.fits\n\nwill (loosely) map to:\n\n> grppha infile="pha1.fits" outfile="pha1_grppha.fits" comm="group min 100 & write & exit" chatter=5 clobber=yes\n\n\n(Note that "& write & exit" are automatically added at the end.)\n\nWhile this is supposed to be as faithful as possible to the original, underlying\napplication, there are some notable differences you should keep in mind:\n\n* you can provide an arbitrary number of input files as command-line\n  arguments, and the wrapper will happily iterate over them;\n* sticking to the ixpeobssim convensions, the name of the output file is\n  programmatically built from the input, and you can (at least partially)\n  control that via the --suffix command-line switch;\n* the wrapper, as all the other ixpeobssim applications, offers a --overwrite\n  command-line option that is similar in spirit to the grppha clobber\n  option (for technical reasons grppha is always run with the clobber option\n  set to "yes" and the check on the output file is done independently).\n'

def xpgrppha(**kwargs):
    """Wrapper implementation.
    """
    file_list = kwargs.get('filelist')
    suffix = kwargs.get('suffix')
    outlist = []
    for in_file_path in file_list:
        assert in_file_path.endswith('.fits')
        out_file_path = in_file_path.replace('.fits', '_%s.fits' % suffix)
        if not kwargs.get('overwrite') and os.path.exists(out_file_path):
            logger.warning('Output file %s already exists, skipping...', out_file_path)
            logger.warning('Use the "--overwrite True" option to overwrite')
            continue
        args = (in_file_path, out_file_path, kwargs.get('comm'), kwargs.get('chatter'))
        cmd = 'grppha infile="%s" outfile="%s" comm="%s & write & exit" chatter=%d clobber=yes' % args
        system_.cmd(cmd, verbose=True)
        outlist.append(out_file_path)
    return outlist
'Command-line switches.\n'
from ixpeobssim.utils.argparse_ import xArgumentParser
PARSER = xArgumentParser(description=__description__)
PARSER.add_filelist()
PARSER.add_suffix('grppha')
PARSER.add_argument('--comm', type=str, required=True, help='the GRPPHA command string')
PARSER.add_argument('--chatter', type=int, default=5, help='value of the GRPPHA chatter commad-line switch')
PARSER.add_overwrite()

def main():
    args = PARSER.parse_args()
    xpgrppha(**args.__dict__)
if __name__ == '__main__':
    main()