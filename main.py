import pygame

class Tetromino:
    def __init__(self, GRID):
        self.shape = [pygame.Rect(0 * GRID, 0 * GRID, GRID, GRID),
                      pygame.Rect(1 * GRID, 0 * GRID, GRID, GRID),
                      pygame.Rect(0 * GRID, 1 * GRID, GRID, GRID),
                      pygame.Rect(1 * GRID, 1 * GRID, GRID, GRID)]
        self.color = 'red'

def main():
    FRAMERATE = 60
    WIDTH, HEIGHT = 320, 512
    GRID = 32
    
    pygame.init()
    
    # Display
    W = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')
    
    # Timers
    TIMER = pygame.event.custom_type()
    pygame.time.set_timer(TIMER, 100)
    
    # Other
    font = pygame.font.SysFont('notomono', 20)
    clock = pygame.time.Clock()
    t = Tetromino(GRID)
    
    run = True
    while run:
        # Limit framerate
        clock.tick(FRAMERATE)
        
        # Handle events
        event_timer = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == TIMER:
                event_timer = True
              
        # Logic
        fps = round(clock.get_fps())
        text_fps = font.render(f'{fps}', True, 'yellow')
        if event_timer:
            for rect in t.shape:
                rect.move_ip(0, 32)
        
        # Draw
        W.fill((16, 16, 16)) # Background
        
        for rect in t.shape: 
            W.fill(t.color, rect)
        
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