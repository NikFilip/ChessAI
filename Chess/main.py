from Board import Board
from GameTree import AI
import sys
import time
import random
from Input import Input

WHITE = True
BLACK = False

#player gets to choose which side to play
#default player is black
def chooseSide():
    playerChoiceInput = input(
        "Would you like to be white(w) or Black(B)? ").lower()
    if 'w' in playerChoiceInput:
        print("You chose white")
        return WHITE
    else:
        print("You chose black")
        return BLACK

#player chooses depth of game tree
#default is 2 
def treeDepth():
    depthInput = 2
    try:
        depthInput = int(input("How many levels should the game tree search?\n"
                               "Levels deeper than 3 will be very slow as no pruning was implemented"
                               ))
    except:
        print("Invalid input, defaulting to 2")
    return depthInput

#gives player command options
def listOfChoises():
    move = 'a3, Nc3, Qxa2, etc = make the move'
    legalMoves = 'l = show all legal moves'
    undo = 'u = undo last move'
    randomMove = 'r = make a random move'
    advantage = 'a = point advantage'
    quit = 'quit'
    
    options = [undo, legalMoves, randomMove,
               quit, move, advantage, '', ]
    print('\n'.join(options))

#gets all legal moves in short notation
def legalMoves(board, parser):
    for move in parser.getMoves(board.currentSide):
        print(move.notation)

#checks all legal moves and makes a random nonAI choice
def getRandomMove(board, parser):
    legalMoves = board.AllLegalMoves(board.currentSide)
    randomMove = random.choice(legalMoves)
    randomMove.notation = parser.notForMove(randomMove)
    return randomMove


def makeMove(move, board):
    print()
    print("Making move : " + move.notation)
    board.makeMove(move)

#this works based off of the minimax point system
def printPointAdvantage(board):
    print("Currently, the point difference is : " +
          str(board.getPAdvantageOfSide(board.currentSide)))

#will only work if more than two moves have been made
def undoLastTwoMoves(board):
    if len(board.history) >= 2:
        board.undoLastMove()
        board.undoLastMove()


def startGame(board, playerSide, ai):
    parser = Input(board, playerSide)
    while True:
        print(board)
        print()
        if board.isCheckmate():
            if board.currentSide == playerSide:
                print("Checkmate, you lost")
            else:
                print("Checkmate! You won!")
            return

        if board.isStalemate():
            if board.currentSide == playerSide:
                print("Stalemate")
            else:
                print("Stalemate")
            return

        if board.currentSide == playerSide:
            move = None
            command = input("It's your move."
                            " Type '?' for options.").lower()
            if command == 'u':
                undoLastTwoMoves(board)
                continue
            elif command == '?':
                listOfChoises()
                continue
            elif command == 'a':
                printPointAdvantage(board)
                continue
            elif command == 'l':
                legalMoves(board, parser)
                continue
            elif command == 'r':
                move = getRandomMove(board, parser)
            elif command == 'quit':
                return
            else:
                move = parser.shortNotForMove(command)
            if move:
                makeMove(move, board)
            else:
                print("Sorry input entered could not be passed, please enter a valid command or move.")

        else:
            print("AI thinking...")
            start = time.clock()
            move = ai.getBestMove()
            move.notation = parser.notForMove(move)
            stop = time.clock()
            print(stop-start)
            makeMove(move, board)


board = Board()
playerSide = chooseSide()
print()
aiDepth = treeDepth()
opponentAI = AI(board, not playerSide, aiDepth)

try:
    startGame(board, playerSide, opponentAI)
except KeyboardInterrupt:
    sys.exit()
