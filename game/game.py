from abc import ABC
import numpy as np


class DropMergeError(ValueError):
    pass


class Game(ABC):
    def __init__(self):
        self.board = [[0 for _ in range(7)] for _ in range(5)]
        self.values = np.arange(1, 6, 1)
        self.next = 0
        self.heights = [0, 0, 0, 0, 0]
        self.largest = np.max(self.board)

    def __repr__(self):
        return f'{np.flip(np.transpose(np.array(self.board)), axis=0)}'

    def next_round(self):
        self.next = 2**(int(np.random.uniform(self.values[0], self.values[-1])))
        print(self.next)

    def place_block(self, row):
        # row 0 to 4
        if self.board[row][-1] and self.board[row][-1] - self.next:
            raise DropMergeError(f"Row {row} is full!")
        elif self.board[row][-1]:
            self.board[row][-1] *= 2
        else:
            self.board[row][self.heights[row]] = self.next
            self.heights[row] += 1
        print(self)


    #def resolve(self, row):
    #   top, left, bottom, right = False, False, False, False
    #    if self.board[]