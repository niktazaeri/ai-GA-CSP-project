import pygame

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (220, 220, 220)
BLUE = (0, 0, 255)
BUTTON_COLOR = (50, 150, 255)
BUTTON_HOVER_COLOR = (70, 170, 255)
SHADOW_COLOR = (150, 150, 150)

class SudokuView:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()

    def draw_grid(self):
        block_size = self.WIDTH // 9
        for row in range(9):
            for col in range(9):
                rect = pygame.Rect(col * block_size, row * block_size, block_size, block_size)
                if (row // 3 + col // 3) % 2 == 0:
                    pygame.draw.rect(self.screen, LIGHT_GRAY, rect)
                pygame.draw.rect(self.screen, BLUE, rect, 1)

        for i in range(0, 10):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLUE, (0, i * block_size), (self.WIDTH, i * block_size), line_width)
            pygame.draw.line(self.screen, BLUE, (i * block_size, 0), (i * block_size, self.HEIGHT - 120), line_width)

    def draw_numbers(self, grid):
        font = pygame.font.SysFont(None, 55)
        for row in range(9):
            for col in range(9):
                num = grid[row][col]
                if num != 0:
                    text = font.render(str(num), True, BLACK)
                    text_rect = text.get_rect(center=(col * 60 + 30, row * 60 + 30))
                    pygame.draw.rect(self.screen, LIGHT_GRAY, text_rect)  # پاک کردن پس زمینه قبل از رسم عدد
                    self.screen.blit(text, text_rect)

    def draw_genetic_button(self):
        button_rect = pygame.Rect(self.WIDTH // 4, self.HEIGHT - 100, self.WIDTH // 2, 40)
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            color = BUTTON_HOVER_COLOR
        else:
            color = BUTTON_COLOR
        pygame.draw.rect(self.screen, color, button_rect)
        font = pygame.font.SysFont(None, 25)
        text = font.render("Solve with Genetic Algorithm", True, WHITE)
        shadow = font.render("Solve with Genetic Algorithm", True, SHADOW_COLOR)

        text_rect = text.get_rect(center=button_rect.center)
        shadow_rect = shadow.get_rect(center=(button_rect.centerx + 2, button_rect.centery + 2))

        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(text, text_rect)
        return button_rect

    def draw_csp_button(self):
        csp_button_rect = pygame.Rect(self.WIDTH // 4, self.HEIGHT - 50, self.WIDTH // 2, 40)
        mouse_pos = pygame.mouse.get_pos()
        if csp_button_rect.collidepoint(mouse_pos):
            color = BUTTON_HOVER_COLOR
        else:
            color = BUTTON_COLOR
        pygame.draw.rect(self.screen, color, csp_button_rect)
        font = pygame.font.SysFont(None, 25)
        text = font.render("Solve with CSP", True, WHITE)
        shadow = font.render("Solve with CSP", True, SHADOW_COLOR)

        text_rect = text.get_rect(center=csp_button_rect.center)
        shadow_rect = shadow.get_rect(center=(csp_button_rect.centerx + 2, csp_button_rect.centery + 2))

        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(text, text_rect)
        return csp_button_rect
