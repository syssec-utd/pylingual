def update_path(self, board, color, path):
    """ update win/loss count along path """
    wins = board.score(BLACK) >= board.score(WHITE)
    for node in path:
        if color == BLACK:
            color = WHITE
        else:
            color = BLACK
        if wins == (color == BLACK):
            node.wins += 1
        else:
            node.losses += 1
        if node.parent:
            node.parent.bestchild = node.parent.best_child()