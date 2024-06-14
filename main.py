import pygame
import sys
from SudokuModel import SudokuModel
from SudokuView import WHITE, SudokuView
from SudokuGeneticAlgorithmController import SudokuGeneticAlgorithmController
from SudokuCSPController import SudokuCSPController

pygame.init()

WIDTH, HEIGHT = 540, 660
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

def main():
    model = SudokuModel()
    view = SudokuView(screen)
    genetic_controller = SudokuGeneticAlgorithmController(model, view)
    csp_controller = SudokuCSPController(model, view)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if view.draw_genetic_button().collidepoint(mouse_pos):
                    genetic_controller.solve()
                if view.draw_csp_button().collidepoint(mouse_pos):
                    csp_controller.solve()

        screen.fill(WHITE)
        view.draw_grid()
        view.draw_numbers(model.get_grid())
        view.draw_genetic_button()
        view.draw_csp_button()
        pygame.display.flip()

if __name__ == "__main__":
    main()
