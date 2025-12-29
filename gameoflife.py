import pygame
import numpy as np

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
TILE_SIZE = 10
FPS = 60

COLOUR_BG = (10, 10, 10)       
COLOUR_GRID = (40, 40, 40)
COLOUR_DIE_NEXT = (170, 170, 170) 
COLOUR_ALIVE_NEXT = (255, 255, 255) 

def update_grid(grid):
    neighbor_count = (
        np.roll(grid, 1, axis=0) +  # N
        np.roll(grid, -1, axis=0) + # S
        np.roll(grid, 1, axis=1) +  # W
        np.roll(grid, -1, axis=1) + # E
        np.roll(np.roll(grid, 1, axis=0), 1, axis=1) +   # NW
        np.roll(np.roll(grid, 1, axis=0), -1, axis=1) +  # NE
        np.roll(np.roll(grid, -1, axis=0), 1, axis=1) +  # SW
        np.roll(np.roll(grid, -1, axis=0), -1, axis=1)   # SE
    )

    # Rules:
    # 1. Birth: Neighbors == 3
    # 2. Survive: Alive AND (Neighbors == 2 OR Neighbors == 3)
    new_grid = np.zeros(grid.shape)
    
    birth_mask = (neighbor_count == 3)
    survival_mask = (grid == 1) & ((neighbor_count == 2) | (neighbor_count == 3))
    
    new_grid[birth_mask | survival_mask] = 1
    
    return new_grid

def draw_grid(screen, grid):
    rows, cols = grid.shape
    
    for row in range(rows):
        for col in range(cols):
            x = col * TILE_SIZE
            y = row * TILE_SIZE

            if grid[row, col] == 1:
                pygame.draw.rect(screen, COLOUR_ALIVE_NEXT, (x, y, TILE_SIZE - 1, TILE_SIZE - 1))
            
    if TILE_SIZE > 5:
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            pygame.draw.line(screen, COLOUR_GRID, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            pygame.draw.line(screen, COLOUR_GRID, (0, y), (SCREEN_WIDTH, y))

def main():
    pygame.init()
    pygame.display.set_caption("Conway's Game of Life - Paused (Space to Run)")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    rows = SCREEN_HEIGHT // TILE_SIZE
    cols = SCREEN_WIDTH // TILE_SIZE
    
    grid = np.random.choice([0, 1], size=(rows, cols), p=[0.8, 0.2])
    
    running = True
    playing = False
    
    while running:
        screen.fill(COLOUR_BG)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                    title = "Running" if playing else "Paused"
                    pygame.display.set_caption(f"Conway's Game of Life - {title}")
                
                if event.key == pygame.K_c: # 'C' to clear grid
                    grid = np.zeros((rows, cols))
                    playing = False
                    pygame.display.set_caption("Conway's Game of Life - Paused (Cleared)")

                if event.key == pygame.K_r: # 'R' to randomise
                    grid = np.random.choice([0, 1], size=(rows, cols), p=[0.8, 0.2])

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                col = pos[0] // TILE_SIZE
                row = pos[1] // TILE_SIZE
                if 0 <= row < rows and 0 <= col < cols:
                    grid[row, col] = 1

        if playing:
            grid = update_grid(grid)
            pygame.time.delay(50) 

        draw_grid(screen, grid)
        pygame.display.update()
        
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()