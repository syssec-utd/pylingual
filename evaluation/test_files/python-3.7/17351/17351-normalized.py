def main(argv):
    """main program loop"""
    global output_dir
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'hb', ['help', 'backup'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    if args == []:
        usage()
        sys.exit(1)
    output_dir = None
    do_backup = None
    for opt in opts:
        if opt[0] in ('-h', '--help'):
            usage()
            sys.exit(0)
        if opt[0] in ('-b', '--backup'):
            do_backup = 1
    source_processor = SourceProcessor()
    file_list = make_file_list(args)
    for filename in file_list:
        source_processor.parse_file(filename)
        for block in source_processor.blocks:
            beautify_block(block)
        new_name = filename + '.new'
        ok = None
        try:
            file = open(new_name, 'wt')
            for block in source_processor.blocks:
                for line in block.lines:
                    file.write(line)
                    file.write('\n')
            file.close()
        except:
            ok = 0