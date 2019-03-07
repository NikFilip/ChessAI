from Piece import Piece
from Coordinate import Coordinate as C

WHITE = True
BLACK = False


class Rook (Piece):

    stringRep = 'R'
    value = 5

    def __init__(self, board, side, pos,  moveHistory=0):
        super(Rook, self).__init__(board, side, pos)
        self.moveHistory = moveHistory

    #possible moves that a rook can make from current position
    def posMoves(self):
        currentPosition = self.position

        directions = [C(0, 1), C(0, -1), C(1, 0), C(-1, 0)]
        for direction in directions:
            for move in self.moveInDirecFromPos(currentPosition,
                                                     direction, self.side):
                yield move
