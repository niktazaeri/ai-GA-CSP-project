class SudokuModel:
    def __init__(self):
        self.grid = [
            [0, 2, 0, 0, 8, 0, 0, 7, 0],
            [4, 7, 0, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 5, 2, 0],
            [0, 9, 2, 3, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 7, 0, 0, 3, 5],
            [0, 0, 7, 9, 0, 5, 6, 0, 0],
            [7, 0, 4, 0, 0, 0, 2, 0, 6],
            [0, 0, 0, 6, 3, 4, 0, 0, 0],
            [0, 0, 0, 0, 9, 0, 0, 5, 3]
        ]

    def get_grid(self):
        return self.grid

    def set_grid(self, grid):
        self.grid = grid
