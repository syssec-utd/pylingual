import argparse
from bashrange import expand_args

def main():
    EXAMPLE_TEXT = 'examples:\n'
    parser = argparse.ArgumentParser(prog='', description='', epilog=EXAMPLE_TEXT, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('', '', help='')
    args = parser.parse_args(expand_args())
if __name__ == '__main__':
    main()