import random
import math

class CheckersAgent:

    #coordinate to notation mapping to format move for output.txt
    x_coord_map = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5:3, 6:2, 7:1}
    y_coord_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    #pawn index to bonus points mapping
    white_pawn_bonuses = {1:3.5, 2:3, 3:2.5, 4:2, 5:1.5, 6:1, 7:0.5}
    black_pawn_bonuses = {0:0.5, 1:1, 2:1.5, 3:2, 4:2.5, 5:3, 6:3.5}

    #edges of the board are row 0, row 7, col 0, or col 7
    edge_indexes = {0,7}

    def __init__(self, checkersGame, board, color, depth, onlyKingsLeft):
        self.onlyKingsLeft = onlyKingsLeft
        self.checkersGame = checkersGame
        self.board = board
        self.color = color
        self.opponentColor = "WHITE" if color == "BLACK" else "BLACK"
        self.prunes = 0
        self.depth = depth
        self.totalRemainingPieces, self.numPlayerKings, self.numOpponentKings = 0, 0, 0

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != ".":
                    self.totalRemainingPieces += 1
                if board[i][j] == self.color[0]:
                    self.numPlayerKings += 1
                elif board[i][j] == self.opponentColor[0]:
                    self.numOpponentKings += 1

    def alphaBetaSearch(self, state):
        alpha = float('-inf')
        beta = float('inf')

        v, bestMove = self.maxValue(state, alpha, beta, 0)

        return bestMove

    def maxValue(self, state, alpha, beta, depth):
        if self.terminalTest(state, self.color, depth):
            return self.evaluation(state), None

        v = float('-inf')
        validSimples, validJumps = self.checkersGame.getValidMoves(self.color, state)
        actions = validJumps if validJumps else validSimples
        bestMove = None
        for validMove in actions:
            successor_state = self.checkersGame.executeMove(validMove,state,self.color)
            newV = self.minValue(successor_state, alpha, beta, depth + 1)[0]
            if newV > v:
                bestMove = validMove
                v = newV
            #flip a coin to randomly choose equivalent moves
            if newV == v:
                coin = random.randrange(2)
                if coin:
                    bestMove = validMove
                    v = newV
            if v >= beta:
                self.prunes += 1
                return v, bestMove
            alpha = max(alpha,v)

        return v, bestMove

    def minValue(self, state, alpha, beta, depth):

        if self.terminalTest(state, self.opponentColor, depth):
            return self.evaluation(state), None

        v = float('inf')
        validSimples, validJumps = self.checkersGame.getValidMoves(self.opponentColor, state)
        actions = validJumps if validJumps else validSimples
        bestMove = None
        for validMove in actions:
            successor_state = self.checkersGame.executeMove(validMove,state,self.opponentColor)
            newV = self.maxValue(successor_state, alpha, beta, depth + 1)[0]
            if newV < v:
                bestMove = validMove
                v = newV
            #flip a coin to randomly choose equivalent moves
            if newV == v:
                coin = random.randrange(2)
                if coin:
                    bestMove = validMove
                    v = newV
            if v <= alpha:
                self.prunes += 1
                return v, bestMove
            beta = min(beta,v)

        return v, bestMove

    #terminal test to check if max depth is reached or game over condition exists
    def terminalTest(self, state, color, depth):
        return depth == self.depth or self.checkersGame.checkLoseCondition(color, state)

    #main evaluation func that decides which evaluation technique to use based on current game state
    def evaluation(self, state):

        if self.checkersGame.checkLoseCondition(self.opponentColor, state):
            return 1000
        if self.checkersGame.checkLoseCondition(self.color, state):
            return -1000

        if self.onlyKingsLeft:
            return self.endGameEvaluation(state,self.color)

        elif self.totalRemainingPieces > 12:
            return self.beginningGameEvaluation(state,self.color)

        elif self.totalRemainingPieces <= 12:
            return self.midGameEvaluation(state,self.color)

    #evaluation function used when total remaining pieces on the board > 12
    #in the beginning, pawn position is not as important, but total remaining player pieces are
    def beginningGameEvaluation(self, state, color):

        playerScore = 0
        opponentScore = 0
        numPlayerPieces = 0

        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == color[0].lower():
                    playerScore += 2
                    numPlayerPieces += 1.5
                    #corners
                    if i in self.edge_indexes or j in self.edge_indexes:
                        playerScore += 0.5

                elif state[i][j] == color[0]:
                    playerScore += 3
                    numPlayerPieces += 1.5
                    #corners
                    if i in self.edge_indexes or j in self.edge_indexes:
                        playerScore += 0.5

                elif state[i][j] == self.opponentColor[0].lower():
                    opponentScore += 2
                    #corners
                    if i in self.edge_indexes or j in self.edge_indexes:
                        opponentScore += 0.5

                elif state[i][j] == self.opponentColor[0]:
                    opponentScore += 3
                    #corners
                    if i in self.edge_indexes or j in self.edge_indexes:
                        opponentScore += 0.5

        return (playerScore - opponentScore) + numPlayerPieces

    #evaluation function used when total remaining pieces on the board <= 12
    #pawn positioning is more important mid game, needs incentive to move towards King's row
    def midGameEvaluation(self, state, color):

        playerScore = 0
        opponentScore = 0

        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == color[0].lower():
                    if color == "WHITE":
                        playerScore += 2 + self.white_pawn_bonuses[i]
                    if color == "BLACK":
                        playerScore += 2 + self.black_pawn_bonuses[i]
                    #corners
                    if i in self.edge_indexes or j in self.edge_indexes:
                        playerScore += 0.5

                elif state[i][j] == color[0]:
                    playerScore += 7
                    #corners
                    if i in self.edge_indexes or j in self.edge_indexes:
                        playerScore += 0.5

                elif state[i][j] == self.opponentColor[0].lower():
                    if self.opponentColor == "WHITE":
                        opponentScore += 2 + self.white_pawn_bonuses[i]
                    if self.opponentColor == "BLACK":
                        opponentScore += 2 + self.black_pawn_bonuses[i]
                    #corners
                    if i in self.edge_indexes or j in self.edge_indexes:
                        opponentScore += 0.5

                elif state[i][j] == self.opponentColor[0]:
                    opponentScore += 7
                    #corners
                    if i in self.edge_indexes or j in self.edge_indexes:
                        opponentScore += 0.5

        return playerScore - opponentScore

    #evaluation function used when only Kings remain on the board
    #go on offense if you have more Kings or go on defense if the opponent has more Kings
    def endGameEvaluation(self, state, color):

        #only kings left
        playerScore = 0
        opponentScore = 0
        totalDistance = 0
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == color[0]:
                    playerScore += 100
                    for row in range(len(state)):
                        for col in range(len(state[row])):
                            if state[row][col] == self.opponentColor[0]:
                                totalDistance += math.sqrt((row-i)**2 + (col-j)**2)

                if state[i][j] == self.opponentColor[0]:
                    opponentScore += 100

        if self.numOpponentKings >= self.numPlayerKings:
            #go on defense
            return totalDistance + (playerScore - opponentScore)
        #go on offense
        return -totalDistance + (playerScore - opponentScore)

    #convert move path to notation to format used in output.txt
    def formatMove(self, move_path):
        result = [ ]
        for i in range(len(move_path) - 1):
            curr_x, curr_y = move_path[i]
            next_x, next_y = move_path[i+1]
            if abs(curr_x - next_x) + abs(curr_y - next_y) == 4:
                result.append("J " + str(self.y_coord_map[curr_y]) + str(self.x_coord_map[curr_x]) + " "
                              + str(self.y_coord_map[next_y]) + str(self.x_coord_map[next_x]))
            elif abs(curr_x - next_x) + abs(curr_y - next_y) == 2:
                result.append("E " + str(self.y_coord_map[curr_y]) + str(self.x_coord_map[curr_x]) + " "
                              + str(self.y_coord_map[next_y]) + str(self.x_coord_map[next_x]))
        return result