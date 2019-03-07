from Piece import Piece
from Coordinate import Coordinate as C

WHITE = True
BLACK = False


class Bishop (Piece):

    stringRep = 'B'
    value = 3

    def __init__(self, board, side, pos, moveHistory=0):
        super(Bishop, self).__init__(board, side, pos)
        self.moveHistory = moveHistory

    #possible moves for a bishop piece to make
    def posMoves(self):
        currentPosition = self.position
        directions = [C(1, 1), C(1, -1), C(-1, 1), C(-1, -1)]
        for direction in directions:
            for move in self.moveInDirecFromPos(currentPosition,
                                                     direction, self.side):
                yield move
