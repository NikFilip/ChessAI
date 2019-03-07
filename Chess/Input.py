import re


class Input:

    def __init__(self, board, side):
        self.board = board
        self.side = side

    #checks for proper input and standardizes the input 
    def check(self, humanInput):
        humanInput = humanInput.lower()
        regexShortNotation = re.compile('[rnbkqp][a-z][1-8]')
        if regexShortNotation.match(humanInput):
            return self.shortNotForMove(humanInput)

    #short notation for moves
    def shortNotForMove(self, notation):
        moves = self.getMoves(self.side)
        for move in moves:
            if move.notation.lower() == notation.lower():
                return move
    
    #notation for moves
    def notForMove(self, move):
        side = self.board.getSideOfMove(move)
        moves = self.getMoves(side)
        for m in moves:
            if m == move:
                return m.notation

    #starts with an empty list of moves
    def getMoves(self, side):
        moves = []

        #grab a legal move from all possible moves and makes it into short notation
        for legalMove in self.board.AllLegalMoves(side):
            moves.append(legalMove)
            legalMove.notation = self.board.getShortNotForMove(legalMove)

        #
        duplicatedNotationMoves = self.duplicatedMoves(moves)
        for duplicateMove in duplicatedNotationMoves:
            duplicateMove.notation = \
                self.board.getShortNotOfMoveWithPos(duplicateMove)

        duplicatedNotationMoves = self.duplicatedMoves(moves)
        for duplicateMove in duplicatedNotationMoves:
            duplicateMove.notation = \
                self.board.getShortNotationOfMoveWithValue(duplicateMove)

        duplicatedNotationMoves = self.duplicatedMoves(moves)
        for duplicateMove in duplicatedNotationMoves:
            duplicateMove.notation = \
                self.board.getShortNotationOfMoveWithPosAndValue(duplicateMove)

        return moves

    #returns a new list that contains only those elements for which the function returned "True".
    #this is used to get rid of duplicate moves
    def duplicatedMoves(self, moves):
        return list(filter(
            lambda move:
            len([m for m in moves if m.notation == move.notation]) > 1, moves))
