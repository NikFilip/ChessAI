from Piece import Piece
from Coordinate import Coordinate as C

WHITE = True
BLACK = False


class Queen(Piece):

    stringRep = 'Q'
    value = 9

    def __init__(self, board, side, pos, moveHistory=0):
        super(Queen, self).__init__(board, side, pos)
        self.moveHistory = moveHistory

    #possible moves for a queen to make using coordinates
    def posMoves(self):
        currentPosition = self.position

        directions = [C(0, 1), C(0, -1), C(1, 0), C(-1, 0), C(1, 1),
                      C(1, -1), C(-1, 1), C(-1, -1)]
        for direction in directions:
            for move in self.moveInDirecFromPos(currentPosition,
                                                     direction, self.side):
                yield move
