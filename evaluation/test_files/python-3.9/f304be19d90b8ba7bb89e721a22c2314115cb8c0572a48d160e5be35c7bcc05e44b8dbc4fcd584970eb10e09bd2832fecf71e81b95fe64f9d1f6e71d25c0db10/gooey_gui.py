from gooey import Gooey, GooeyParser

@Gooey
def main():
    parser = GooeyParser(description='My GUI Program!')
    parser.add_argument('Filename', widget='FileChooser')
    parser.add_argument('Date', widget='DateChooser')
    args = parser.parse_args()
    print(args)
if __name__ == '__main__':
    main()