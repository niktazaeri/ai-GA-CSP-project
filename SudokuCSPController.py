import time
import pygame

class SudokuCSPController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def solve(self):
        grid = self.model.get_grid()
        variables = [(r, c) for r in range(9) for c in range(9)]
        domains = {var: [grid[var[0]][var[1]]] if grid[var[0]][var[1]] != 0 else list(range(1, 10)) for var in variables}
        neighbors = {(r, c): self.get_neighbors(r, c) for r in range(9) for c in range(9)}

        def sudoku_constraints(A, a, B, b):
            return a != b

        def mrv(assignment, csp):
            unassigned_vars = [v for v in csp['variables'] if v not in assignment]
            return min(unassigned_vars, key=lambda var: len(csp['domains'][var]))

        def lcv(var, assignment, csp):
            return sorted(csp['domains'][var], key=lambda val: sum(1 for neighbor in csp['neighbors'][var] if val in csp['domains'][neighbor]))

        def forward_checking(csp, var, value, assignment):
            csp['domains'][var] = [value]
            for neighbor in csp['neighbors'][var]:
                if neighbor not in assignment:
                    for val in csp['domains'][neighbor][:]:
                        if not sudoku_constraints(var, value, neighbor, val):
                            csp['domains'][neighbor].remove(val)
                    if not csp['domains'][neighbor]:
                        return False
            return True

        def backtracking_search(csp):
            def backtrack(assignment):
                if len(assignment) == len(csp['variables']):
                    return assignment
                var = mrv(assignment, csp)
                for value in lcv(var, assignment, csp):
                    if 0 == sum(1 for neighbor in csp['neighbors'][var] if value == assignment.get(neighbor)):
                        assignment[var] = value
                        if forward_checking(csp, var, value, assignment):
                            self.update_view(assignment)  # به روز رسانی ویو
                            result = backtrack(assignment)
                            if result is not None:
                                return result
                        del assignment[var]
                return None

            return backtrack({})

        csp = {'variables': variables, 'domains': domains, 'neighbors': neighbors}
        solution = backtracking_search(csp)

        if solution:
            solved_grid = [[solution[(r, c)] for c in range(9)] for r in range(9)]
            self.model.set_grid(solved_grid)
            self.view.draw_numbers(self.model.get_grid())
            print("Sudoku solved successfully!")
        else:
            print("No solution found for the Sudoku puzzle.")

    def update_view(self, assignment):
        temp_grid = [[0 for _ in range(9)] for _ in range(9)]
        for (r, c), v in assignment.items():
            temp_grid[r][c] = v
        self.model.set_grid(temp_grid)
        self.view.draw_numbers(self.model.get_grid())
        pygame.display.update()

        # چاپ وضعیت فعلی پازل در ترمینال
        for row in temp_grid:
            print(row)
        print("\n")

        time.sleep(0.5)  # اضافه کردن تاخیر برای نمایش بهتر

    def get_neighbors(self, row, col):
        neighbors = set()
        for r in range(9):
            if r != row:
                neighbors.add((r, col))
        for c in range(9):
            if c != col:
                neighbors.add((row, c))
        block_row_start = (row // 3) * 3
        block_col_start = (col // 3) * 3
        for r in range(block_row_start, block_row_start + 3):
            for c in range(block_col_start, block_col_start + 3):
                if r != row or c != col:
                    neighbors.add((r, c))
        return neighbors