import copy
import time
import Checkers
import AlphaBetaAgent

#parses input.txt to extract game data
def parse_input_file(filename: str) -> dict:
    input_file = open(filename, "r")

    input_file_list = [ ]
    for line in input_file:
        input_file_list.append(line.strip())

    input_file_map = {}
    input_file_map["single_or_game"] = input_file_list[0]
    input_file_map["color"] = input_file_list[1]
    input_file_map["play_time"] = float(input_file_list[2])

    game_board = [ ]
    for line in input_file_list[3::]:
        game_board.append([char for char in line])

    input_file_map["game_board"] = game_board
    input_file.close()

    return input_file_map

#write formatted move to output.txt
def write_output_file(filename: str, move_path: list):
    output_file = open(filename, "w")
    for i in range(len(move_path)):
        output_file.write(move_path[i])
        if i != (len(move_path) - 1):
            output_file.write('\n')

    output_file.close()

#driver code
if __name__ == "__main__":
    #start_time = time.time()
    input_file_map = parse_input_file("./input.txt")
    color = input_file_map["color"]
    game_board = input_file_map["game_board"]

    checkersGame = Checkers.Checkers()
    onlyKingsLeft = checkersGame.onlyKingsLeft(game_board, color)

    remaining_time = input_file_map["play_time"]
    if remaining_time < 3:
        depth = 2
    else:
        depth = 3

    checkersAgent = AlphaBetaAgent.CheckersAgent(checkersGame, game_board, color, depth, onlyKingsLeft)
    bestMove = checkersAgent.alphaBetaSearch(copy.deepcopy(game_board))
    formattedBestMove = checkersAgent.formatMove(bestMove)
    write_output_file("./output.txt", formattedBestMove)

    #end_time = time.time()
    #print("total cpu time: " + str(end_time - start_time) + " seconds")