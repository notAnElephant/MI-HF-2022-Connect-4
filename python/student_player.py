import math
import random
from typing import List
from board import Board


class StudentPlayer:
    def __init__(self, player_index: int, board_size: List[int], n_to_connect: int):
        self.__n_to_connect = n_to_connect
        self.__board_size = board_size
        self.__player_index = player_index

        self.__board = Board(self.__board_size, self.__n_to_connect)

        # own code
        self._other_player_index = 1 if player_index == 2 else 2

        """
        One step (column selection) of the current player.
        :param last_player_col: [-1, board_size[1]), it is -1 if there was no step yet
        :return: step (column index) of the current player
        """

    def step(self, last_player_col: int) -> int:
        if last_player_col != -1:  # if the other player made a step, update the board accordingly
            self.__board.step(self._other_player_index, last_player_col)

        col = self.minimax(self.__board, 2, self.__player_index)[0]

        self.__board.step(self.__player_index, col)
        return col

    # implement minimax algorithm, where the current player is the maximizing player
    # and the desired return value is the column index of the best step
    def minimax(self, board, remaining_depth, player_index):
        valid_steps = board.get_valid_steps()
        col = random.choice(valid_steps)
        if remaining_depth == 0 or board.game_ended():  # evaluate the current board state
            return col, self.value_of_board(board, player_index)

        if player_index == self.__player_index:  # our player is the maximizing player
            highest_score = -math.inf
            for step in valid_steps:
                copy_board = board.copy()
                copy_board.step(player_index, step)
                possible_score = self.minimax(copy_board, remaining_depth - 1, self._other_player_index)[1]
                if possible_score > highest_score:
                    highest_score = possible_score
                    col = step
            return col, highest_score
        else:  # it's the other player's turn, who is the minimizing player
            lowest_score = math.inf
            for step in valid_steps:
                copy_board = board.copy()
                copy_board.step(player_index, step)
                possible_score = self.minimax(copy_board, remaining_depth - 1, self.__player_index)[1]
                if possible_score < lowest_score:
                    lowest_score = possible_score
                    col = step
            return col, lowest_score

    def value_of_board(self, board, player_index):
        if board.game_ended():
            if board.get_winner() == 1:
                return -10000
            else:
                return 10000
        return 0
        # board_values = board.get_state()
        # cols = [0, 0, 0, 0, 0, 0, 0]
        # for i in range(0, 7):
        #     for j in range(0, 6):
        #         if board_values[j][i] == 0:
        #             continue
        #         if board_values[j][i] == player_index:
        #             cols[i] += 1
        #         elif board_values[j][i] != player_index:
        #             break
        #
        # return cols.sum()
