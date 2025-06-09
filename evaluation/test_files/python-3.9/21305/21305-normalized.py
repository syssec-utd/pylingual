def options(self, parser, env):
    """
        Add options to command line.
        """
    super(Coverage, self).options(parser, env)
    parser.add_option('--cover-package', action='append', default=env.get('NOSE_COVER_PACKAGE'), metavar='PACKAGE', dest='cover_packages', help='Restrict coverage output to selected packages [NOSE_COVER_PACKAGE]')
    parser.add_option('--cover-erase', action='store_true', default=env.get('NOSE_COVER_ERASE'), dest='cover_erase', help='Erase previously collected coverage statistics before run')
    parser.add_option('--cover-tests', action='store_true', dest='cover_tests', default=env.get('NOSE_COVER_TESTS'), help='Include test modules in coverage report [NOSE_COVER_TESTS]')
    parser.add_option('--cover-min-percentage', action='store', dest='cover_min_percentage', default=env.get('NOSE_COVER_MIN_PERCENTAGE'), help='Minimum percentage of coverage for teststo pass [NOSE_COVER_MIN_PERCENTAGE]')
    parser.add_option('--cover-inclusive', action='store_true', dest='cover_inclusive', default=env.get('NOSE_COVER_INCLUSIVE'), help='Include all python files under working directory in coverage report.  Useful for discovering holes in test coverage if not all files are imported by the test suite. [NOSE_COVER_INCLUSIVE]')
    parser.add_option('--cover-html', action='store_true', default=env.get('NOSE_COVER_HTML'), dest='cover_html', help='Produce HTML coverage information')
    parser.add_option('--cover-html-dir', action='store', default=env.get('NOSE_COVER_HTML_DIR', 'cover'), dest='cover_html_dir', metavar='DIR', help='Produce HTML coverage information in dir')
    parser.add_option('--cover-branches', action='store_true', default=env.get('NOSE_COVER_BRANCHES'), dest='cover_branches', help='Include branch coverage in coverage report [NOSE_COVER_BRANCHES]')
    parser.add_option('--cover-xml', action='store_true', default=env.get('NOSE_COVER_XML'), dest='cover_xml', help='Produce XML coverage information')
    parser.add_option('--cover-xml-file', action='store', default=env.get('NOSE_COVER_XML_FILE', 'coverage.xml'), dest='cover_xml_file', metavar='FILE', help='Produce XML coverage information in file')