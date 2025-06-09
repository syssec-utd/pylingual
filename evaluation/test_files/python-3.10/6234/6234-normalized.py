def add_biomart_parser(subparsers):
    """Add function 'biomart' argument parsers."""
    argparser_biomart = subparsers.add_parser('biomart', help='Using BioMart API to convert gene ids.')
    biomart_opt = argparser_biomart.add_argument_group('Input arguments')
    biomart_opt.add_argument('-f', '--filter', action='store', nargs=2, dest='filter', required=True, metavar=('NAME', 'VALUE'), help='Which filter to use. Input filter name, and value.\n                                     If multi-value required, separate each value by comma.\n                                     If value is a txt file, then one ID per row, exclude header.')
    biomart_opt.add_argument('-a', '--attributes', action='store', dest='attrs', type=str, required=True, metavar='ATTR', help='Which attribute(s) to retrieve. Separate each attr by comma.')
    biomart_opt.add_argument('-o', '--ofile', dest='ofile', type=str, required=True, help='Output file name')
    biomart_opt.add_argument('-d', '--dataset', action='store', dest='bg', type=str, default='hsapiens_gene_ensembl', metavar='DATA', help='Which dataset to use. Default: hsapiens_gene_ensembl')
    biomart_opt.add_argument('--host', action='store', dest='host', type=str, default='www.ensembl.org', metavar='HOST', help="Which host to use. Select from {'www.ensembl.org', 'asia.ensembl.org', 'useast.ensembl.org'}.")
    biomart_opt.add_argument('-m', '--mart', action='store', dest='mart', type=str, metavar='MART', default='ENSEMBL_MART_ENSEMBL', help='Which mart to use. Default: ENSEMBL_MART_ENSEMBL.')
    biomart_opt.add_argument('-v', '--verbose', action='store_true', default=False, dest='verbose', help='Increase output verbosity, print out progress of your job')