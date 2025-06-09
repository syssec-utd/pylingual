import sys
from ..api import pipeline
import fuc
description = f'\nRun genotyping pipeline for chip data.\n'
epilog = f'\n[Example] To genotype the CYP3A5 gene from chip data:\n  $ pypgx {fuc.api.common._script_name()} \\\n  CYP3A5 \\\n  CYP3A5-pipeline \\\n  variants.vcf.gz\n'

def create_parser(subparsers):
    parser = fuc.api.common._add_parser(subparsers, fuc.api.common._script_name(), description=description, epilog=epilog, help='Run genotyping pipeline for chip data.')
    parser.add_argument('gene', help='Target gene.')
    parser.add_argument('output', help='Output directory.')
    parser.add_argument('variants', help='Input VCF file must be already BGZF compressed (.gz)\nand indexed (.tbi) to allow random access.\nStatistical haplotype phasing will be skipped if\ninput VCF is already fully phased.')
    parser.add_argument('--assembly', metavar='TEXT', default='GRCh37', help="\nReference genome assembly (default: 'GRCh37')\n(choices: 'GRCh37', 'GRCh38').")
    parser.add_argument('--panel', metavar='PATH', help='VCF file corresponding to a reference haplotype panel\n(compressed or uncompressed). By default, the 1KGP\npanel in the ~/pypgx-bundle directory will be used.')
    parser.add_argument('--impute', action='store_true', help='Perform imputation of missing genotypes.')
    parser.add_argument('--force', action='store_true', help='Overwrite output directory if it already exists.')
    parser.add_argument('--samples', metavar='TEXT', nargs='+', help='Specify which samples should be included for analysis\nby providing a text file (.txt, .tsv, .csv, or .list)\ncontaining one sample per line. Alternatively, you\ncan provide a list of samples.')
    parser.add_argument('--exclude', action='store_true', help='Exclude specified samples.')

def main(args):
    pipeline.run_chip_pipeline(args.gene, args.output, args.variants, assembly=args.assembly, panel=args.panel, impute=args.impute, force=args.force, samples=args.samples, exclude=args.exclude)