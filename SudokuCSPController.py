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

        def AC3(csp, queue=None):
            if queue is None:
                queue = [(Xi, Xk) for Xi in csp['variables'] for Xk in csp['neighbors'][Xi]]
            support_pruning(csp)
            while queue:
                (Xi, Xj) = queue.pop()
                if revise(csp, Xi, Xj):
                    if not csp['curr_domains'][Xi]:
                        return False
                    for Xk in csp['neighbors'][Xi]:
                        if Xk != Xi:
                            queue.append((Xk, Xi))
            return True

        def revise(csp, Xi, Xj):
            revised = False
            for x in csp['curr_domains'][Xi][:]:
                if all(not sudoku_constraints(Xi, x, Xj, y) for y in csp['curr_domains'][Xj]):
                    csp['curr_domains'][Xi].remove(x)
                    revised = True
            return revised

        def support_pruning(csp):
            if csp['curr_domains'] is None:
                csp['curr_domains'] = {v: list(csp['domains'][v]) for v in csp['variables']}

        def first_unassigned_variable(assignment, csp):
            for var in csp['variables']:
                if var not in assignment:
                    return var

        def mrv(assignment, csp):
            unassigned_vars = [v for v in csp['variables'] if v not in assignment]
            return min(unassigned_vars, key=lambda var: len(csp['curr_domains'][var]))

        def lcv(var, assignment, csp):
            return sorted(csp['curr_domains'][var], key=lambda val: sum(1 for neighbor in csp['neighbors'][var] if val in csp['curr_domains'][neighbor]))

        def forward_checking(csp, var, value, assignment):
            csp['curr_domains'][var] = [value]
            for neighbor in csp['neighbors'][var]:
                if neighbor not in assignment:
                    for val in csp['curr_domains'][neighbor][:]:
                        if not sudoku_constraints(var, value, neighbor, val):
                            csp['curr_domains'][neighbor].remove(val)
                    if not csp['curr_domains'][neighbor]:
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
                            print_grid(assignment)  # چاپ وضعیت فعلی پازل
                            self.view.draw_numbers(self.model.get_grid())  # رسم اعداد روی پازل
                            pygame.display.update()
                            time.sleep(0.5)  # اضافه کردن تاخیر برای نمایش بهتر

                            result = backtrack(assignment)
                            if result is not None:
                                return result
                        del assignment[var]
                return None

            return backtrack({})

        def print_grid(assignment):
            temp_grid = [[0 for _ in range(9)] for _ in range(9)]
            for (r, c), v in assignment.items():
                temp_grid[r][c] = v
            for row in temp_grid:
                print(row)
            print("\n")

        csp = {'variables': variables, 'domains': domains, 'neighbors': neighbors, 'curr_domains': None}
        support_pruning(csp)
        AC3(csp)
        solution = backtracking_search(csp)

        if solution:
            solved_grid = [[solution[(r, c)] for c in range(9)] for r in range(9)]
            self.model.set_grid(solved_grid)
            self.view.draw_numbers(self.model.get_grid())
            print("Sudoku solved successfully!")
        else:
            print("No solution found for the Sudoku puzzle.")

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
