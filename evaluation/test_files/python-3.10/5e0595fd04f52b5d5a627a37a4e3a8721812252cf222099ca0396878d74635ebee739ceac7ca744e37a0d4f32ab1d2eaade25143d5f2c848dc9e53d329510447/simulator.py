import logging
import sys
import traceback
from .generator import CourseGenerator
from .generator import PlayersGenerator
from .generator import RoundGenerator
from ..tee import TeeMarker
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
COLUMN_WIDTH = 5

def print_header(header, max_len):
    print(header.ljust(max_len))

def print_column(value, hole_number):
    width = COLUMN_WIDTH + 1 if hole_number > 9 else COLUMN_WIDTH
    sys.stdout.write(str(value).center(width, ' ') + '|')

def print_separator_header(max_player_name_length):
    scorecard_length = max_player_name_length + 18 + 9 * 5 + 9 * 6 + 6
    print('-' * scorecard_length)

def pretty_print(round):
    print('--------------------')
    print(round.course)
    print('--------------------')
    max_len = 0
    for player in round.players:
        curr = len(player.name)
        max_len = curr if curr > max_len else max_len
    print_header('Hole', max_len)
    for hole in round.course.holes:
        print_column(hole.number, hole.number)
    print('')
    print_separator_header(max_len)
    for marker in list(TeeMarker):
        print_header(marker.name, max_len)
        for hole in round.course.holes:
            tee = hole.get_tee(marker)
            print_column(tee.distance, hole.number)
        print(' ' + str(round.course.total_distance(marker)))
        print_header('', max_len)
        for hole in round.course.holes:
            tee = hole.get_tee(marker)
            print_column(tee.par, hole.number)
        print('')
    print_separator_header(max_len)
    for player in round.players:
        print_header(player.name, max_len)
        for hole in round.course.holes:
            score = round.scorecard.get_score(player, hole.number).score
            print_column(score, hole.number)
        print(' ' + str(round.scorecard.get_scores(player).total_score))
if __name__ == '__main__':
    try:
        players = PlayersGenerator.generate()
        course = CourseGenerator.generate('Makalena', 18)
        round = RoundGenerator.generate(course, players)
        pretty_print(round)
    except:
        trace = traceback.format_exc()
        logging.error('OMGWTFBBQ: {0}'.format(trace))
        sys.exit(1)
    sys.exit(0)