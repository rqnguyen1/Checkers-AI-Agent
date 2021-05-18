import copy

class Checkers:

    BOARD_WIDTH = 8
    BOARD_HEIGHT = 8
    BLACK_KINGS_ROW = {(0,1), (0,3), (0,5), (0,7)}
    WHITE_KINGS_ROW = {(7,0), (7,2), (7,4), (7,6)}

    def printBoard(self, game_board):
        print("    ", end = "")
        for i in range(len(game_board)):
            print(str(i) + "    ", end="")
        print()

        for i in range(len(game_board)):
            print(8-i, end = "")
            print(" " + str(game_board[i]) + " " + str(i))

        print("    ", end = "")
        for i in range(65, len(game_board[0]) + 65):
            print(chr(i) + "    ", end="")
        print()

    #returns a tuple(list, list) of valid simples moves and valid jump moves
    def getValidMoves(self, color, board) -> (list,list):
        validSimples = [ ]
        validJumps = [ ]

        #iterate through the board
        for i in range(self.BOARD_WIDTH):
            for j in range(self.BOARD_HEIGHT):
                if color[0].lower() == board[i][j].lower():
                    validSimplesAtPos, validJumpsAtPos = self.getValidMovesAtPos(i,j, color, board)
                    if validSimplesAtPos:
                        validSimples.extend(validSimplesAtPos)
                    if validJumpsAtPos:
                        validJumps.extend(validJumpsAtPos)

        #since we iterate the board from top to bottom, reverse the order of moves for white
        if color == "WHITE":
            return validSimples[::-1], validJumps[::-1]
        return validSimples, validJumps

    #returns a list of valid simples, and a list of valid jumps from position (x,y)
    def getValidMovesAtPos(self, x, y, color, board) -> (list,list):
        validSimples = [ ]

        if color == "BLACK":
            #simple moves
            for xOffset, yOffset in [(1,1), (1,-1)]:
                newX, newY = x + xOffset, y + yOffset
                if newX < 0 or newY < 0 or newX >= self.BOARD_HEIGHT or newY >= self.BOARD_WIDTH:
                    continue
                if board[newX][newY] == ".":
                    validSimples.append([(x,y)] + [(newX,newY)])

            #check two more directions if piece is a king
            if board[x][y] == "B":
                for xOffset, yOffset in [(-1,1), (-1,-1)]:
                    newX, newY = x + xOffset, y + yOffset
                    if newX < 0 or newY < 0 or newX >= self.BOARD_HEIGHT or newY >= self.BOARD_WIDTH:
                        continue
                    if board[newX][newY] == ".":
                        validSimples.append([(x,y)] + [(newX,newY)])

        if color == "WHITE":
            #simple moves
            for xOffset, yOffset in [(-1,1), (-1,-1)]:
                newX, newY = x + xOffset, y + yOffset
                if newX < 0 or newY < 0 or newX >= self.BOARD_HEIGHT or newY >= self.BOARD_WIDTH:
                    continue
                if board[newX][newY] == ".":
                    validSimples.append([(x,y)] + [(newX,newY)])

            #check two more directions if piece is a king
            if board[x][y] == "W":
                for xOffset, yOffset in [(1,1), (1,-1)]:
                    newX, newY = x + xOffset, y + yOffset
                    if newX < 0 or newY < 0 or newX >= self.BOARD_HEIGHT or newY >= self.BOARD_WIDTH:
                        continue
                    if board[newX][newY] == ".":
                        validSimples.append([(x,y)] + [(newX,newY)])

        #jump moves
        validJumps = [ ]
        self.getValidJumps(x,y,validJumps,[(x,y)], board, color)

        return validSimples, validJumps

    #gets valid jumps from position (x,y) using recursive backtracking
    def getValidJumps(self, x, y, validJumps, path, board, color):
        jumpsRemaining = False

        if color == "BLACK":
            if board[x][y] == "b":
                for xOffset, yOffset in [(2,2), (2,-2)]:
                    newX, newY = x + xOffset, y + yOffset
                    if newX < 0 or newY < 0 or newX >= self.BOARD_HEIGHT or newY >= self.BOARD_WIDTH:
                        continue
                    if board[newX][newY] == ".":
                        #middle piece must be the opponent
                        middleX, middleY = (x + newX)//2, (y + newY)//2
                        if board[middleX][middleY].lower() == "w":
                            jumpsRemaining = True
                            path.append((newX,newY))
                            #after being crowned a king, should not continue jumping
                            if (newX,newY) in self.WHITE_KINGS_ROW:
                                validJumps.append(list(path))
                                path.pop()
                                continue
                            successor_board = self.executeMove(path[-2::],board,color)
                            self.getValidJumps(newX,newY,validJumps,path, successor_board, color)
                            path.pop()

            #king piece
            if board[x][y] == "B":
                for xOffset, yOffset in [(2,2), (2,-2), (-2,2), (-2,-2)]:
                    newX, newY = x + xOffset, y + yOffset
                    if newX < 0 or newY < 0 or newX >= self.BOARD_HEIGHT or newY >= self.BOARD_WIDTH:
                        continue
                    if board[newX][newY] == ".":
                        #middle piece must be the opponent
                        middleX, middleY = (x + newX)//2, (y + newY)//2
                        if board[middleX][middleY].lower() == "w":
                            jumpsRemaining = True
                            path.append((newX,newY))
                            successor_board = self.executeMove(path[-2::],board,color)
                            self.getValidJumps(newX,newY,validJumps,path, successor_board, color)
                            path.pop()

        if color == "WHITE":
            if board[x][y] == "w":
                for xOffset, yOffset in [(-2,2), (-2,-2)]:
                    newX, newY = x + xOffset, y + yOffset
                    if newX < 0 or newY < 0 or newX >= self.BOARD_HEIGHT or newY >= self.BOARD_WIDTH:
                        continue
                    if board[newX][newY] == ".":
                        #middle piece must be the opponent
                        middleX, middleY = (x + newX)//2, (y + newY)//2
                        if board[middleX][middleY].lower() == "b":
                            jumpsRemaining = True
                            path.append((newX,newY))
                            #after being crowned a king, should not continue jumping
                            if (newX,newY) in self.BLACK_KINGS_ROW:
                                validJumps.append(list(path))
                                path.pop()
                                continue
                            successor_board = self.executeMove(path[-2::],board,color)
                            self.getValidJumps(newX,newY,validJumps,path, successor_board, color)
                            path.pop()

            #check two more directions if piece is a king
            if board[x][y] == "W":
                for xOffset, yOffset in [(2,2), (2,-2), (-2,2), (-2,-2)]:
                    newX, newY = x + xOffset, y + yOffset
                    if newX < 0 or newY < 0 or newX >= self.BOARD_HEIGHT or newY >= self.BOARD_WIDTH:
                        continue
                    if board[newX][newY] == ".":
                        #middle piece must be the opponent
                        middleX, middleY = (x + newX)//2, (y + newY)//2
                        if board[middleX][middleY].lower() == "b":
                            jumpsRemaining = True
                            path.append((newX,newY))
                            successor_board = self.executeMove(path[-2::],board,color)
                            self.getValidJumps(newX,newY,validJumps,path, successor_board, color)
                            path.pop()

        #reached a point where there are no jumps left to make
        if not jumpsRemaining and len(path) > 1:
            validJumps.append(list(path))


    #execute the specified move and return a copy of the new board state
    def executeMove(self, path: list, board, color):
        board_copy = copy.deepcopy(board)

        start_pos = path[0]
        next_pos = path[1]
        isJump = False
        if abs(start_pos[0] - next_pos[0]) + abs(start_pos[1] - next_pos[1]) == 4:
            isJump = True

        #simple move
        if not isJump:
            curr_piece = board_copy[start_pos[0]][start_pos[1]]
            board_copy[start_pos[0]][start_pos[1]] = "."
            board_copy[next_pos[0]][next_pos[1]] = curr_piece

            if color == "WHITE":
                if next_pos in self.BLACK_KINGS_ROW:
                    board_copy[next_pos[0]][next_pos[1]] = curr_piece.upper()

            if color == "BLACK":
                if next_pos in self.WHITE_KINGS_ROW:
                    board_copy[next_pos[0]][next_pos[1]] = curr_piece.upper()

        #jumps
        if isJump:
            curr_piece = board_copy[start_pos[0]][start_pos[1]]
            prev_pos = start_pos
            board_copy[start_pos[0]][start_pos[1]] = "."
            for i in range(1, len(path)):
                curr_pos = path[i]
                middleX = (curr_pos[0] + prev_pos[0]) // 2
                middleY = (curr_pos[1] + prev_pos[1]) // 2
                board_copy[middleX][middleY] = "."
                prev_pos = curr_pos

            board_copy[prev_pos[0]][prev_pos[1]] = curr_piece

            if color == "WHITE":
                if prev_pos in self.BLACK_KINGS_ROW:
                    board_copy[prev_pos[0]][prev_pos[1]] = curr_piece.upper()

            if color == "BLACK":
                if prev_pos in self.WHITE_KINGS_ROW:
                    board_copy[prev_pos[0]][prev_pos[1]] = curr_piece.upper()

        return board_copy

    #check the lose condition for the specified color
    def checkLoseCondition(self, color, board) -> bool:

        validSimples, validJumps = self.getValidMoves(color, board)
        if not validSimples and not validJumps:
            return True

        return False

    #returns True if only Kings remain on the board else False
    def onlyKingsLeft(self, board, color) -> bool:
        for i in range(self.BOARD_HEIGHT):
            for j in range(self.BOARD_WIDTH):
                if board[i][j] == "b" or board[i][j] == "w":
                    return False
        return True
