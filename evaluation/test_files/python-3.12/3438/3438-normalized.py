def process_arguments(args):
    """Argparse function to get the program parameters"""
    parser = argparse.ArgumentParser(description='Time stretching example')
    parser.add_argument('input_file', action='store', help='path to the input file (wav, mp3, etc)')
    parser.add_argument('output_file', action='store', help='path to the stretched output (wav)')
    parser.add_argument('-s', '--speed', action='store', type=float, default=2.0, required=False, help='speed')
    return vars(parser.parse_args(args))