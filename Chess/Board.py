from Pawn import Pawn
from Rook import Rook
from King import King
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from Coordinate import Coordinate as C
from termcolor import colored
from Move import Move
from pip._vendor import colorama

WHITE = True
BLACK = False


class Board:

    def __init__(self, checkMate=False, castling=False,
                 enpessant=False, promo=False):
        self.pieces = []
        self.history = []
        self.points = 0
        self.currentSide = WHITE
        self.moveHistory = 0
        self.checkmate = False

        if not checkMate and not castling and not enpessant and not promo:
            self.pieces.extend([Rook(self, BLACK, C(0, 7)),
                                Knight(self, BLACK, C(1, 7)),
                                Bishop(self, BLACK, C(2, 7)),
                                Queen(self, BLACK, C(3, 7)),
                                King(self, BLACK, C(4, 7)),
                                Bishop(self, BLACK, C(5, 7)),
                                Knight(self, BLACK, C(6, 7)),
                                Rook(self, BLACK, C(7, 7))])
            for x in range(8):
                self.pieces.append(Pawn(self, BLACK, C(x, 6)))
            for x in range(8):
                self.pieces.append(Pawn(self, WHITE, C(x, 1)))
            self.pieces.extend([Rook(self, WHITE, C(0, 0)),
                                Knight(self, WHITE, C(1, 0)),
                                Bishop(self, WHITE, C(2, 0)),
                                Queen(self, WHITE, C(3, 0)),
                                King(self, WHITE, C(4, 0)),
                                Bishop(self, WHITE, C(5, 0)),
                                Knight(self, WHITE, C(6, 0)),
                                Rook(self, WHITE, C(7, 0))])

        elif promo:
            pawnToPromote = Pawn(self, WHITE, C(1, 6))
            pawnToPromote.moveHistory = 1
            kingWhite = King(self, WHITE, C(4, 0))
            kingBlack = King(self, BLACK, C(3, 2))
            self.pieces.extend([pawnToPromote, kingWhite, kingBlack])

        elif enpessant:
            pawn = Pawn(self, WHITE, C(1, 4))
            pawn2 = Pawn(self, BLACK, C(2, 6))
            kingWhite = King(self, WHITE, C(4, 0))
            kingBlack = King(self, BLACK, C(3, 2))
            self.pieces.extend([pawn, pawn2, kingWhite, kingBlack])
            self.history = []
            self.currentSide = BLACK
            self.points = 0
            self.moveHistory = 0
            self.checkmate = False
            firstMove = Move(pawn2, C(2, 4))
            self.makeMove(firstMove)
            self.currentSide = WHITE
            return

    def __str__(self):
        return self.wrapStringRepresentation(self.makeStringRepresentation(self.pieces))

    def undoLastMove(self):
        lastMove, pieceTaken = self.history.pop()

        if lastMove.queensideCastle or lastMove.kingsideCastle:
            king = lastMove.piece
            rook = lastMove.specialMovePiece

            self.movePieceToPos(king, lastMove.oldPos)
            self.movePieceToPos(rook, lastMove.rookMove.oldPos)

            king.moveHistory -= 1
            rook.moveHistory -= 1

        elif lastMove.pessant:
            pawnMoved = lastMove.piece
            pawnTaken = pieceTaken
            self.pieces.append(pawnTaken)
            self.movePieceToPos(pawnMoved, lastMove.oldPos)
            pawnMoved.moveHistory -= 1
            if pawnTaken.side == WHITE:
                self.points += 1
            if pawnTaken.side == BLACK:
                self.points -= 1

        elif lastMove.promotion:
            pawnPromoted = lastMove.piece
            promotedPiece = self.pieceAtPosition(lastMove.newPos)
            self.pieces.remove(promotedPiece)
            self.pieces.append(pawnPromoted)
            if pawnPromoted.side == WHITE:
                self.points -= promotedPiece.value - 1
            elif pawnPromoted.side == BLACK:
                self.points += promotedPiece.value - 1
            pawnPromoted.moveHistory -= 1

        else:
            pieceToMoveBack = lastMove.piece
            self.movePieceToPos(pieceToMoveBack, lastMove.oldPos)
            if pieceTaken:
                if pieceTaken.side == WHITE:
                    self.points += pieceTaken.value
                if pieceTaken.side == BLACK:
                    self.points -= pieceTaken.value
                self.addPieceToPos(pieceTaken, lastMove.newPos)
                self.pieces.append(pieceTaken)
            pieceToMoveBack.moveHistory -= 1

        self.currentSide = not self.currentSide

    def isCheckmate(self):
        if len(self.AllLegalMoves(self.currentSide)) == 0:
            for move in self.getAllMovesUnfilt(not self.currentSide):
                pieceToTake = move.pieceToCapture
                if pieceToTake and pieceToTake.stringRep == "K":
                    return True
        return False

    def isStalemate(self):
        if len(self.AllLegalMoves(self.currentSide)) == 0:
            for move in self.getAllMovesUnfilt(not self.currentSide):
                pieceToTake = move.pieceToCapture
                if pieceToTake and pieceToTake.stringRep == "K":
                    return False
            return True
        return False

    def getLastMove(self):
        if self.history:
            return self.history[-1][0]

    #used for undoing last move
    def getLastPieceMoved(self):
        if self.history:
            return self.history[-1][0].piece

    #used in undoing moves
    def addMoveToHistory(self, move):
        pieceTaken = None
        if move.pessant:
            pieceTaken = move.specialMovePiece
            self.history.append([move, pieceTaken])
            return
        pieceTaken = move.pieceToCapture
        if pieceTaken:
            self.history.append([move, pieceTaken])
            return

        self.history.append([move, None])

    def getCurrentSide(self):
        return self.currentSide

    #used for making the sides different colours (blue and red)
    def makeStringRepresentation(self, pieces):
        stringRep = ''
        for y in range(7, -1, -1):
            for x in range(8):
                piece = None
                for p in pieces:
                    if p.position == C(x, y):
                        piece = p
                        break
                pieceRep = ''
                if piece:
                    side = piece.side
                    color = 'blue' if side == WHITE else 'red'
                    pieceRep = colored(piece.stringRep, color)
                else:
                    pieceRep = 'x'
                stringRep += pieceRep + ' '
            stringRep += '\n'
        stringRep = stringRep.strip()
        return stringRep


    def wrapStringRepresentation(self, stringRep):
        sRep = '\n'.join(
            ['   a b c d e f g h   ', ' '*21] +
            ['%d  %s  %d' % (8-r, s.strip(), 8-r)
             for r, s in enumerate(stringRep.split('\n'))] +
            [' '*21, '   a b c d e f g h   ']
            ).rstrip()
        return sRep

    #determines the value of pieces passed into method
    def valueOfPiece(self, piece):
        return str(piece.position[1] + 1)

    #creates a transtable for the pieces
    def placeOfPiece(self, piece):
        tranTable = str.maketrans('01234567', 'abcdefgh')
        return str(piece.position[0]).translate(tranTable)

    #returns the short notation of moves passed in
    def getShortNotForMove(self, move):
        notation = ""
        pieceToMove = move.piece
        pieceToTake = move.pieceToCapture

        if move.queensideCastle:
            return "0-0-0"

        if move.kingsideCastle:
            return "0-0"

        if pieceToMove.stringRep != 'p':
            notation += pieceToMove.stringRep

        if pieceToTake is not None:
            if pieceToMove.stringRep == 'p':
                notation += self.placeOfPiece(pieceToMove)
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)

        if move.promotion:
            notation += "=" + str(move.specialMovePiece.stringRep)

        return notation

    #used for taking pieces from opponent
    def getShortNotOfMoveWithPos(self, move):

        notation = ""
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if pieceToMove.stringRep != 'p':
            notation += pieceToMove.stringRep
            notation += self.placeOfPiece(pieceToMove)

        if pieceToTake is not None:
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)
        return notation

    #used for taking a piece from opponent if the attack is used(x)
    def getShortNotationOfMoveWithValue(self, move):

        notation = ""
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if pieceToMove.stringRep != 'p':
            notation += pieceToMove.stringRep
            notation += self.valueOfPiece(pieceToMove)

        if pieceToTake is not None:
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)
        return notation

    #used in finding the moves to take if the attack(x) is used in position
    def getShortNotationOfMoveWithPosAndValue(self, move):

        notation = ""
        pieceToMove = self.pieceAtPosition(move.oldPos)
        pieceToTake = self.pieceAtPosition(move.newPos)

        if pieceToMove.stringRep != 'p':
            notation += pieceToMove.stringRep
            notation += self.placeOfPiece(pieceToMove)
            notation += self.valueOfPiece(pieceToMove)

        if pieceToTake is not None:
            notation += 'x'

        notation += self.positionToHumanCoord(move.newPos)
        return notation
        return

    #translates the positions input to program specific code
    def humanCoordToPosition(self, coord):
        transTable = str.maketrans('abcdefgh', '12345678')
        coord = coord.translate(transTable)
        coord = [int(c)-1 for c in coord]
        pos = C(coord[0], coord[1])
        return pos

    #translates back to human coordinates
    def positionToHumanCoord(self, pos):
        transTable = str.maketrans('01234567', 'abcdefgh')
        notation = str(pos[0]).translate(transTable) + str(pos[1]+1)
        return notation

    #checks input for valid move
    def isValidPos(self, pos):
        if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7:
            return True
        else:
            return False

    def getSideOfMove(self, move):
        return move.piece.side

    #gives position of piece input
    def getPositionOfPiece(self, piece):
        for y in range(8):
            for x in range(8):
                if self.boardArray[y][x] is piece:
                    return C(x, 7-y)

    #gives the piece at current position input
    def pieceAtPosition(self, pos):
        for piece in self.pieces:
            if piece.position == pos:
                return piece
    

    #used in Doing/Undoing moves
    def movePieceToPos(self, piece, pos):
        piece.position = pos

    #used in Doing/Undoing moves
    def addPieceToPos(self, piece, pos):
        piece.position = pos

    #used in Doing/Undoing moves 
    def clearPos(self, pos):
        x, y = self.coordToLocInArray(pos)
        self.boardArray[x][y] = None

    def coordToLocInArray(self, pos):
        return (7-pos[1], pos[0])

    def locInArrayToCoord(self, loc):
        return (loc[1], 7-loc[0])

    def makeMove(self, move):
        self.addMoveToHistory(move)
        if move.kingsideCastle or move.queensideCastle:
            kingToMove = move.piece
            rookToMove = move.specialMovePiece
            self.movePieceToPos(kingToMove, move.newPos)
            self.movePieceToPos(rookToMove, move.rookMovePos)
            kingToMove.moveHistory += 1
            rookToMove.moveHistory += 1

        elif move.pessant:
            pawnToMove = move.piece
            pawnToTake = move.specialMovePiece
            pawnToMove.position = move.newPos
            self.pieces.remove(pawnToTake)
            pawnToMove.moveHistory += 1

        elif move.promotion:
            self.pieces.remove(move.piece)
            self.pieces.append(move.specialMovePiece)
            if move.piece.side == WHITE:
                self.points += move.specialMovePiece.value - 1
            if move.piece.side == BLACK:
                self.points -= move.specialMovePiece.value - 1

        else:
            pieceToMove = move.piece
            pieceToTake = move.pieceToCapture

            if pieceToTake:
                if pieceToTake.side == WHITE:
                    self.points -= pieceToTake.value
                if pieceToTake.side == BLACK:
                    self.points += pieceToTake.value
                self.pieces.remove(pieceToTake)

            self.movePieceToPos(pieceToMove, move.newPos)
            pieceToMove.moveHistory += 1
        self.moveHistory += 1
        self.currentSide = not self.currentSide

    #returns the point value of side thats passed in
    def getPValueOfSide(self, side):
        points = 0
        for piece in self.pieces:
            if piece.side == side:
                points += piece.value
        return points

    #returns point advantage of side thats passed in
    def getPAdvantageOfSide(self, side):
        pointAdvantage = self.getPValueOfSide(side) - \
            self.getPValueOfSide(not side)
        return pointAdvantage
        if side == WHITE:
            return self.points
        if side == BLACK:
            return -self.points

    #returns all possible moves, used for giving list of moves
    def getAllMovesUnfilt(self, side, includeKing=True):
        unfilteredMoves = []
        for piece in self.pieces:
            if piece.side == side:
                if includeKing or piece.stringRep != 'K':
                    for move in piece.posMoves():
                        unfilteredMoves.append(move)
        return unfilteredMoves

    def testIfLegalBoard(self, side):
        for move in self.getAllMovesUnfilt(side):
            pieceToTake = move.pieceToCapture
            if pieceToTake and pieceToTake.stringRep == 'K':
                return False
        return True

    def moveIsLegal(self, move):
        side = move.piece.side
        self.makeMove(move)
        isLegal = self.testIfLegalBoard(not side)
        self.undoLastMove()
        return isLegal


    def AllLegalMoves(self, side):
        unfilteredMoves = list(self.getAllMovesUnfilt(side))
        legalMoves = []
        for move in unfilteredMoves:
            if self.moveIsLegal(move):
                legalMoves.append(move)
        return legalMoves
