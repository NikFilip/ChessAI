from Piece import Piece
from Move import Move
from Coordinate import Coordinate as C

WHITE = True
BLACK = False


class King (Piece):

    stringRep = 'K'
    value = 100

    def __init__(self, board, side, pos,  moveHistory=0):
        super(King, self).__init__(board, side, pos)
        self.moveHistory = moveHistory

    #This method provides the possible positions a king piece can move to using coordinates
    def posMoves(self):
        currentPos = self.position
        movements = [C(0, 1), C(0, -1), C(1, 0), C(-1, 0), C(1, 1),
                     C(1, -1), C(-1, 1), C(-1, -1)]
        for movement in movements:
            newPos = currentPos + movement
            if self.board.isValidPos(newPos):
                pieceAtNewPos = self.board.pieceAtPosition(newPos)
                if self.board.pieceAtPosition(newPos) is None:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side:
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos)

        # Castling
        #using a lot of statements to see if castling is allowed
        #by checking for conditions such as the position of rooks and 
        #if the king is in check or not
        if self.moveHistory == 0:
            inCheck = False
            kingCastleBlocked = False
            queenCastleBlocked = False
            kingCastleCheck = False
            queenCastleCheck = False
            kingRookMoved = True
            queenRookMoved = True

            #looks at the rook on the kings side
            kingCastlePositions = [self.position - C(1, 0),
                                       self.position - C(2, 0)]
            for pos in kingCastlePositions:
                if self.board.pieceAtPosition(pos):
                    kingCastleBlocked = True
            
            #looks at the rook on the queenside
            queenCastlePositions = [self.position + C(1, 0),
                                        self.position + C(2, 0),
                                        self.position + C(3, 0)]
            for pos in queenCastlePositions:
                if self.board.pieceAtPosition(pos):
                    queenCastleBlocked = True

            if kingCastleBlocked and queenCastleBlocked:
                return

            otherSideMoves = \
                self.board.getAllMovesUnfilt(not self.side,
                                                 includeKing=False)
            for move in otherSideMoves:
                if move.newPos == self.position:
                    inCheck = True
                    break
                if move.newPos == self.position - C(1, 0) or \
                   move.newPos == self.position - C(2, 0):
                    kingCastleCheck = True
                if move.newPos == self.position + C(1, 0) or \
                   move.newPos == self.position + C(2, 0):
                    queenCastleCheck = True

            kingRookPos = self.position - C(3, 0)
            kingRook = self.board.pieceAtPosition(kingRookPos) \
                if self.board.isValidPos(kingRookPos) \
                else None
            if kingRook and \
               kingRook.stringRep == 'R' and \
               kingRook.moveHistory == 0:
                kingRookMoved = False

            queenRookPos = self.position + C(4, 0)
            queenRook = self.board.pieceAtPosition(queenRookPos) \
                if self.board.isValidPos(queenRookPos) \
                else None
            if queenRook and \
               queenRook.stringRep == 'R' and \
               queenRook.moveHistory == 0:
                queenRookMoved = False
            
            #checks for all possibilities to see if castling is allowed
            if not inCheck:
                if not kingCastleBlocked and \
                   not kingCastleCheck and \
                   not kingRookMoved:
                    move = Move(self, self.position - C(2, 0))
                    rookMove = Move(self.position, self.position - C(1, 0))
                    move.specialMovePiece = \
                        self.board.pieceAtPosition(kingRookPos)
                    move.kingsideCastle = True
                    move.rookMove = rookMove
                    yield move
                if not queenCastleBlocked and \
                   not queenCastleCheck and \
                   not queenRookMoved:
                    move = Move(self, self.position + C(2, 0))
                    rookMove = Move(self.position, self.position + C(1, 0))
                    move.specialMovePiece = \
                        self.board.pieceAtPosition(queenRookPos)
                    move.queensideCastle = True
                    move.rookMove = rookMove
                    yield move
