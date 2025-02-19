import pygame
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 700
GRID_SIZE = 5
CELL_SIZE = 70
GRID_OFFSET_X = (WIDTH - GRID_SIZE * CELL_SIZE) // 2
GRID_OFFSET_Y = 100

COLORS = {
    'background': (240, 240, 240),
    'grid': (200, 200, 200),
    'text': (50, 50, 50),
    'game_colors': ['red', 'blue', 'green', 'yellow']
}

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        
    def color_cell(self, row, col, color):
        if self.grid[row][col] is None:
            self.grid[row][col] = color
            self.score += 1
            return True
        return False
    
    def is_game_over(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] is not None:
                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                            if self.grid[row][col] == self.grid[nr][nc]:
                                return True
        return False
    
    def is_board_filled(self):
        return all(all(cell is not None for cell in row) for row in self.grid)

def draw_game(screen, board, selected_cell=None):
    screen.fill(COLORS['background'])
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {board.score}", True, COLORS['text'])
    screen.blit(score_text, (20, 20))
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = GRID_OFFSET_X + col * CELL_SIZE
            y = GRID_OFFSET_Y + row * CELL_SIZE
            color = COLORS['grid'] if board.grid[row][col] is None else pygame.Color(board.grid[row][col])
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, COLORS['text'], (x, y, CELL_SIZE, CELL_SIZE), 1)
    for i, color in enumerate(COLORS['game_colors']):
        pygame.draw.rect(screen, pygame.Color(color),
                        (GRID_OFFSET_X + i * (CELL_SIZE + 10),
                         HEIGHT - 100,
                         CELL_SIZE,
                         CELL_SIZE))

def show_message(screen, message):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    font = pygame.font.Font(None, 48)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)
    restart_text = font.render("Click to restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
    screen.blit(restart_text, restart_rect)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Color Fill")
    clock = pygame.time.Clock()
    board = Board()
    game_state = "playing"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state != "playing":
                    board = Board()
                    game_state = "playing"
                    continue
                x, y = event.pos
                if (GRID_OFFSET_X <= x <= GRID_OFFSET_X + GRID_SIZE * CELL_SIZE and
                    GRID_OFFSET_Y <= y <= GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE):
                    grid_x = (x - GRID_OFFSET_X) // CELL_SIZE
                    grid_y = (y - GRID_OFFSET_Y) // CELL_SIZE
                    selected_cell = (grid_y, grid_x)
                if HEIGHT - 100 <= y <= HEIGHT - 100 + CELL_SIZE:
                    color_index = (x - GRID_OFFSET_X) // (CELL_SIZE + 10)
                    if 0 <= color_index < len(COLORS['game_colors']):
                        if selected_cell:
                            if board.color_cell(selected_cell[0], selected_cell[1], 
                                             COLORS['game_colors'][color_index]):
                                selected_cell = None
                                if board.is_game_over():
                                    game_state = "game_over"
                                elif board.is_board_filled():
                                    game_state = "won"
        draw_game(screen, board)
        if game_state == "game_over":
            show_message(screen, "Game Over!")
        elif game_state == "won":
            show_message(screen, "You Won!")
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
