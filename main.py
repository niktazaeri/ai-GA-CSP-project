import pygame
import sys
from SudokuModel import SudokuModel
from SudokuView import WHITE, SudokuView
from SudokuGeneticAlgorithmController import SudokuGeneticAlgorithmController

# Initialize the pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 540, 600  # Height increased for button space
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

def main():
    model = SudokuModel()
    view = SudokuView(screen)
    controller = SudokuGeneticAlgorithmController(model, view)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_rect = view.draw_button()
                if button_rect.collidepoint(event.pos):
                    controller.solve()

        screen.fill(WHITE)
        view.draw_grid()
        view.draw_numbers(model.get_grid())
        view.draw_button()
        pygame.display.flip()

if __name__ == "__main__":
    main()
