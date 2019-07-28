from random import randint
from random import sample


class CreateSudokuPuzzle:
    def __init__(self):
        self.rows = self.columns = self.total_blocks = 9
        self.sudoku = []
        for i in range(0, self.rows):
            row_list = []
            for j in range(0, self.columns):
                row_list.append(0)
            self.sudoku.append(row_list)
        self.block_dict = {
            0: [(0, 2), (0, 2), False],
            1: [(0, 2), (3, 5), False],
            2: [(0, 2), (6, 8), False],
            3: [(3, 5), (0, 2), False],
            4: [(3, 5), (3, 5), False],
            5: [(3, 5), (6, 8), False],
            6: [(6, 8), (0, 2), False],
            7: [(6, 8), (3, 5), False],
            8: [(6, 8), (6, 8), False],
        }
        self.random_block_combination = ((0, 4, 8), (1, 5, 6), (2, 3, 7))

    def get_block_num(self, row, col):
        for item in self.block_dict.items():
            if row >= item[1][0][0] and row <= item[1][0][1] and col >= item[1][1][0] and col <= item[1][1][1]:
                return item[0]

    def check_value_in_row(self, value, row):
        for col in range(0, self.columns):
            if self.sudoku[row][col] == value:
                return True
        return False

    def check_value_in_col(self, value, col):
        for row in range(0, self.rows):
            if self.sudoku[row][col] == value:
                return True
        return False

    def check_value_in_block(self, value, block_num):
        block_row_start = self.block_dict[block_num][0][0]
        block_row_end = self.block_dict[block_num][0][1]
        block_col_start = self.block_dict[block_num][1][0]
        block_col_end = self.block_dict[block_num][1][1]
        for row in range(block_row_start, block_row_end+1):
            for col in range(block_col_start, block_col_end+1):
                if self.sudoku[row][col] == value:
                    return True
        return False

    def display(self):
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                print(" {0:5} ".format(str(self.sudoku[i][j])), end=" ")
            print("\n")

    def populate_first_three_random_blocks(self):
        random_block = randint(0, 8)
        for block_tuple in self.random_block_combination:
            if random_block in block_tuple:
                for block in block_tuple:
                    random_list = sample(range(1, 10), 9)
                    random_block_row = self.block_dict[block][0]
                    random_block_col = self.block_dict[block][1]
                    random_list_index = 0
                    for i in range(random_block_row[0], random_block_row[1]+1):
                        for j in range(random_block_col[0], random_block_col[1]+1):
                            self.sudoku[i][j] = random_list[random_list_index]
                            random_list_index += 1
                            self.block_dict[block][2] = True
                break

    def check_if_safe_to_insert(self, value, row, col):
        block_num = self.get_block_num(row, col)
        if self.check_value_in_block(value, block_num) or self.check_value_in_row(value, row) or self.check_value_in_col(value, col):
            return False
        else:
            return True

    def get_first_empty_cell(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.sudoku[row][col] == 0:
                    return (row, col)
        return (None, None)

    def solve_sudoku(self, partial_sudoku):
        row, col = self.get_first_empty_cell()
        if row == None and col == None:
            return True
        else:
            for value_to_insert in range(1, 10):
                if self.check_if_safe_to_insert(value_to_insert, row, col):
                    self.sudoku[row][col] = value_to_insert
                    if(self.solve_sudoku(self.sudoku)):
                        return True
                    else:
                        self.sudoku[row][col] = 0
                        continue
                else:
                    continue


if __name__ == '__main__':
    X = CreateSudokuPuzzle()
    X.populate_first_three_random_blocks()
    X.solve_sudoku(X.sudoku)
    X.display()
