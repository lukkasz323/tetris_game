import pygame

class Tetromino:
    def __init__(self):
        pass

def main():
    FRAMERATE = 60
    WIDTH, HEIGHT = 320, 512
    GRID = 32
    
    pygame.init()
    
    clock = pygame.time.Clock()
    
    font = pygame.font.SysFont('notomono', 20)
    
    W = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')
    
    run = True
    while run:
        # Limit framerate
        clock.tick(FRAMERATE)
        
        # Handle events
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    run = False
              
        # Logic
        fps = round(clock.get_fps())
        text_fps = font.render(f'{fps}', True, 'yellow')
        
        # Draw
        W.fill((16, 16, 16)) # Background
        
        for x in range(0, WIDTH, GRID): # Grid
            for y in range(0, HEIGHT, GRID):
                rect = pygame.Rect(x, y, GRID, GRID)
                pygame.draw.rect(W, 'gray10', rect, 1)
                
        W.blit(text_fps, (WIDTH - 26, 0))
        
        # Update screen
        pygame.display.update()
                    
    pygame.quit()

if __name__ == '__main__':
    main()