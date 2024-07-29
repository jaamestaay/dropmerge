from abc import ABC
import numpy as np


class DropMergeError(ValueError):
    pass


class Game(ABC):
    def __init__(self, base=2, rows=5, height=7):
        # TO DO: Input Game Stats to output below!
        self.base = base
        self.rows = rows
        self.height = height
        self.board = [[0 for _ in range(height)] for _ in range(rows)]
        self.values = np.arange(1, 6, 1)
        self.next = 0
        self.heights = [0, 0, 0, 0, 0]
        self.target = base**(6+height)

    def __repr__(self):
        return f'{np.flip(np.transpose(np.array(self.board)), axis=0)}'

    def next_round(self):
        self.next = self.base**(int(np.random.uniform(self.values[0],
                                                      self.values[-1])))
        print(self.next)
        lose = True
        for i in range(self.rows):
            if self.heights[i] < self.height or self.next == self.board[i][-1]:
                lose = False
                break
        return lose

    def check_input(self, input):
        try:
            input = float(input)
        except ValueError:
            print("Input must either be 'False' or an integer.")
        else:
            leftover = input % 1
            row = int(input)-1
            if row > 4 or row < 0 or leftover:
                print("Row must be an integer from 1 to 5 (inclusive).")
                return False
            elif self.board[row][-1] and self.board[row][-1] - self.next:
                print(f"Row {row} is full!")
                return False
            else:
                return True

    def place_block(self, row):
        # row 0 to 4
        if self.board[row][-1]:
            self.board[row][-1] *= self.base
        else:
            self.board[row][self.heights[row]] = self.next
            self.heights[row] += 1

    def resolve(self, row, col):
        top, left, bottom, right = False, False, False, False
        val = self.board[row][col]
        mult = 0
        if not val:
            return
        try:
            if not self.board[row][col+1] - val:
                top = True
                mult += 1
        except IndexError:
            pass
        try:
            if not self.board[row][col-1] - val:
                bottom = True
                mult += 1
        except IndexError:
            pass
        try:
            if not self.board[row+1][col] - val:
                right = True
                mult += 1
        except IndexError:
            pass
        try:
            if not self.board[row-1][col] - val:
                left = True
                mult += 1
        except IndexError:
            pass
        self.board[row][col] *= self.base**mult
        if top and bottom and left and right:
            self.board[row+1].pop(col)
            self.board[row+1].append(0)
            self.board[row-1].pop(col)
            self.board[row-1].append(0)
            self.board[row].pop(col+1)
            self.board[row].pop(col-1)
            self.board[row].extend([0, 0])
            self.heights[row-1] -= 1
            self.heights[row+1] -= 1
            self.heights[row] -= 2
            self.resolve(row, col-1)
            self.resolve(row, col)
            self.resolve(row-1, col)
            self.resolve(row+1, col)
        elif top and left and bottom:
            self.board[row-1].pop(col)
            self.board[row-1].append(0)
            self.board[row].pop(col+1)
            self.board[row].pop(col-1)
            self.board[row].extend([0, 0])
            self.heights[row-1] -= 1
            self.heights[row] -= 2
            self.resolve(row, col-1)
            self.resolve(row, col)
            self.resolve(row-1, col)
        elif top and right and bottom:
            self.board[row+1].pop(col)
            self.board[row+1].append(0)
            self.board[row].pop(col+1)
            self.board[row].pop(col-1)
            self.board[row].extend([0, 0])
            self.heights[row+1] -= 1
            self.heights[row] -= 2
            self.resolve(row, col-1)
            self.resolve(row, col)
            self.resolve(row+1, col)
        elif top and left and right:
            self.board[row+1].pop(col)
            self.board[row+1].append(0)
            self.board[row-1].pop(col)
            self.board[row-1].append(0)
            self.board[row].pop(col+1)
            self.board[row].append(0)
            self.heights[row-1] -= 1
            self.heights[row+1] -= 1
            self.heights[row] -= 1
            self.resolve(row, col)
            self.resolve(row, col+1)
            self.resolve(row-1, col)
            self.resolve(row+1, col)
        elif bottom and left and right:
            self.board[row+1].pop(col)
            self.board[row+1].append(0)
            self.board[row-1].pop(col)
            self.board[row-1].append(0)
            self.board[row].pop(col-1)
            self.board[row].append(0)
            self.heights[row-1] -= 1
            self.heights[row+1] -= 1
            self.heights[row] -= 1
            self.resolve(row, col-1)
            self.resolve(row, col)
            self.resolve(row-1, col)
            self.resolve(row+1, col)
        elif top and bottom:
            self.board[row].pop(col+1)
            self.board[row].pop(col-1)
            self.board[row].extend([0, 0])
            self.heights[row] -= 2
            self.resolve(row, col-1)
            self.resolve(row, col)
        elif top and left:
            self.board[row].pop(col+1)
            self.board[row].append(0)
            self.board[row-1].pop(col)
            self.board[row-1].append(0)
            self.heights[row-1] -= 1
            self.heights[row] -= 1
            self.resolve(row, col)
            self.resolve(row, col+1)
            self.resolve(row-1, col)
        elif top and right:
            self.board[row].pop(col+1)
            self.board[row].append(0)
            self.board[row+1].pop(col)
            self.board[row+1].append(0)
            self.heights[row+1] -= 1
            self.heights[row] -= 1
            self.resolve(row, col)
            self.resolve(row, col+1)
            self.resolve(row+1, col)
        elif bottom and left:
            self.board[row-1].pop(col)
            self.board[row-1].append(0)
            self.board[row].pop(col-1)
            self.board[row].append(0)
            self.heights[row-1] -= 1
            self.heights[row] -= 1
            self.resolve(row, col-1)
            self.resolve(row, col)
            self.resolve(row-1, col)
        elif bottom and right:
            self.board[row+1].pop(col)
            self.board[row+1].append(0)
            self.board[row].pop(col-1)
            self.board[row].append(0)
            self.heights[row+1] -= 1
            self.heights[row] -= 1
            self.resolve(row, col-1)
            self.resolve(row, col)
            self.resolve(row+1, col)
        elif left and right:
            self.board[row+1].pop(col)
            self.board[row+1].append(0)
            self.board[row-1].pop(col)
            self.board[row-1].append(0)
            self.heights[row-1] -= 1
            self.heights[row+1] -= 1
            self.resolve(row, col)
            self.resolve(row-1, col)
            self.resolve(row+1, col)
        elif top:
            self.board[row].pop(col+1)
            self.board[row].append(0)
            self.heights[row] -= 1
            self.resolve(row, col)
            self.resolve(row, col+1)
        elif bottom:
            self.board[row].pop(col-1)
            self.board[row].append(0)
            self.heights[row] -= 1
            self.resolve(row, col-1)
            self.resolve(row, col)
        elif left:
            self.board[row-1].pop(col)
            self.board[row-1].append(0)
            self.heights[row-1] -= 1
            self.resolve(row, col)
            self.resolve(row-1, col)
        elif right:
            self.board[row+1].pop(col)
            self.board[row+1].append(0)
            self.heights[row+1] -= 1
            self.resolve(row, col)
            self.resolve(row+1, col)
        return self

    def update_values(self):
        newval = np.max(self.board)
        if newval >= self.target:
            self.values *= self.base**(newval//self.target + 1)
            self.target = newval*self.base
            new_min = np.min(self.values)
            print(f'Congrats! You hit the goal of {self.target//self.base}.',
                  f'New goal: {self.target}')
            to_update = []
            for row in range(self.rows):
                for column in range(self.height):
                    if self.board[row][column] < new_min:
                        self.board[row].pop(column)
                        self.board[row].append(0)
                        to_update.append([row, column])
            for row, column in to_update:
                self.resolve(row, column)
        return self

    def play(self):
        print("Hello!")
        print(self)
        while True:
            outcome = self.next_round()
            if outcome:
                print("No more moves :(")
                return self
            while True:
                row = input("Which row to input? (type 'stop' to stop game)\n")
                if isinstance(row, str):
                    if row == 'stop':
                        print("Bye :(")
                        return self
                if self.check_input(row):
                    break
            row = int(row)-1
            self.place_block(row)
            self.resolve(row, self.heights[row]-1)
            self.update_values()
            print(self)


game = Game()
game.play()
