from Board import Board
from MoveNode import MoveNode
from Input import Input
import copy
import random
from multiprocessing import Pool


WHITE = True
BLACK = False


class AI:

    depth = 1
    board = None
    side = None
    movesAnalyzed = 0

    def __init__(self, board, side, depth):
        self.board = board
        self.side = side
        self.depth = depth
        self.parser = Input(self.board, self.side)

    def getFirstMove(self, side):
        move = list(self.board.AllLegalMoves(side))[0]
        return move

    #returns a list of all filtered legal moves the ai can make
    #used for addign nodes to the tree
    def getAllLegalMovesConcur(self, side):
        p = Pool(8)
        unfilteredMovesWithBoard = \
            [(move, copy.deepcopy(self.board))
             for move in self.board.getAllMovesUnfilt(side)]
        legalMoves = p.starmap(self.returnMoveIfLegal,
                               unfilteredMovesWithBoard)
        p.close()
        p.join()
        return list(filter(None, legalMoves))

    #returns the lowest nodes of the tree(one sides best moves)
    def minChild(self, node):
        lowestNodes = []
        for child in node.children:
            if not lowestNodes:
                lowestNodes.append(child)
            elif child < lowestNodes[0]:
                lowestNodes = []
                lowestNodes.append(child)
            elif child == lowestNodes[0]:
                lowestNodes.append(child)
        return lowestNodes

    #returns the highest nodes of the tree(one sides best moves)
    def maxChild(self, node):
        highestNodes = []
        for child in node.children:
            if not highestNodes:
                highestNodes.append(child)
            elif child < highestNodes[0]:
                highestNodes = []
                highestNodes.append(child)
            elif child == highestNodes[0]:
                highestNodes.append(child)
        return highestNodes

    #used when user asks for a random move without AI
    def getRandomMove(self):
        legalMoves = list(self.board.AllLegalMoves(self.side))
        randomMove = random.choice(legalMoves)
        return randomMove

    def generateMoveTree(self):
        moveTree = []
        for move in self.board.AllLegalMoves(self.side):
            moveTree.append(MoveNode(move, [], None))

        for node in moveTree:
            self.board.makeMove(node.move)
            self.populateTree(node)
            self.board.undoLastMove()
        return moveTree

    #depth of tree is user selected
    def populateTree(self, node):
        node.pointAdvantage = self.board.getPAdvantageOfSide(self.side)
        node.depth = node.getDepth()
        if node.depth == self.depth:
            return

        side = self.board.currentSide

        #checks for a checkmate or stalemate
        #if no check or stale then it populates the tree with all legal moves
        #but if check is incurred then no legal moves can be made
        legalMoves = self.board.AllLegalMoves(side)
        #if no legal moves can be made then checkmate attribute is set and return
        if not legalMoves:
            if self.board.isCheckmate():
                node.move.checkmate = True
                return
        #if stalemate same as checkmate but set point advantage to 0 
            elif self.board.isStalemate():
                node.move.stalemate = True
                node.pointAdvantage = 0
                return
            raise Exception()

        for move in legalMoves:
            self.movesAnalyzed += 1
            node.children.append(MoveNode(move, [], node))
            self.board.makeMove(move)
            self.populateTree(node.children[-1])
            self.board.undoLastMove()

    #this method traverses the populated tree
    def getPointAdvantageForNode(self, node):
        if node.children:
            for child in node.children:
                child.pointAdvantage = \
                    self.getPointAdvantageForNode(child)

            # If the depth is divisible by 2,
            # it's a move for the AI's side, so return max
            if node.children[0].depth % 2 == 1:
                return(max(node.children).pointAdvantage)
            else:
                return(min(node.children).pointAdvantage)
        else:
            return node.pointAdvantage

    #picks a random best move from list of best moves
    def getBestMove(self):
        moveTree = self.generateMoveTree()
        bestMoves = self.bestMovesWithMoveTree(moveTree)
        randomBestMove = random.choice(bestMoves)
        randomBestMove.notation = self.parser.notForMove(randomBestMove)
        return randomBestMove

    def makeBestMove(self):
        self.board.makeMove(self.getBestMove())

    #picks the move with the highest point advantage in the tree
    def bestMovesWithMoveTree(self, moveTree):
        bestMoveNodes = []
        for moveNode in moveTree:
            moveNode.pointAdvantage = \
                self.getPointAdvantageForNode(moveNode)
            #if best moves list is empty
            #then add moveNode to the list regardless of its value 
            if not bestMoveNodes:
                bestMoveNodes.append(moveNode)
            #if moveNode is higher value than the move in the list
            #clear the list and add moveNode to it
            elif moveNode > bestMoveNodes[0]:
                bestMoveNodes = []
                bestMoveNodes.append(moveNode)
            #if its equal value then just add moveNode to the list
            elif moveNode == bestMoveNodes[0]:
                bestMoveNodes.append(moveNode)

        return [node.move for node in bestMoveNodes]

    #makes sure move is valid
    def isValidMove(self, move, side):
        for legalMove in self.board.AllLegalMoves(side):
            if move == legalMove:
                return True
        return False

    #used pick a value from bestMovesNodes list
    #dont want the AI to be too predictable
    def makeRandomMove(self):
        moveToMake = self.getRandomMove()
        self.board.makeMove(moveToMake)


if __name__ == "__main__":
    mainBoard = Board()
    ai = AI(mainBoard, True, 3)
    print(mainBoard)
    ai.makeBestMove()
    print(mainBoard)
    print(ai.movesAnalyzed)
    print(mainBoard.moveHistory)
