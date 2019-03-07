from Piece import Piece
from Coordinate import Coordinate as C
from Move import Move

BLACK = False
WHITE = True


class Knight(Piece):

    stringRep = 'N'
    value = 3

    def __init__(self, board, side, pos,  moveHistory=0):
        super(Knight, self).__init__(board, side, pos)
        self.moveHistory = moveHistory

    #this method provides possible moves for a knight to make using the coordinate class
    def posMoves(self):
        board = self.board
        currentPos = self.position
        #possible positions the piece can 'jump' to
        movements = [C(2, 1), C(2, -1), C(-2, 1), C(-2, -1), C(1, 2),
                     C(1, -2), C(-1, -2), C(-1, 2)]

        for movement in movements:
            newPos = currentPos + movement
            if board.isValidPos(newPos):
                pieceAtNewPos = board.pieceAtPosition(newPos)
                if pieceAtNewPos is None:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side:
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos)
