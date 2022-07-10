import pygame

def main():
    FRAMERATE = 60
    WIDTH, HEIGHT = 320, 512
    GRID = 32
    
    pygame.init()
    
    clock = pygame.time.Clock()
    
    W = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')
    
    run = True
    while run:
        clock.tick(FRAMERATE)
        
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    run = False
                    
        W.fill((16, 16, 16))
        
        # Draw grid.
        for x in range(0, WIDTH, GRID):
            for y in range(0, HEIGHT, GRID):
                rect = pygame.Rect(x, y, GRID, GRID)
                pygame.draw.rect(W, 'gray10', rect, 1)
        
        # Update screen.
        pygame.display.update()
                    
    pygame.quit()

if __name__ == '__main__':
    main()