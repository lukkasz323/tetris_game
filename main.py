import pygame

class Tetromino:
    def __init__(self, G):
        self.shape = [pygame.Rect(0 * G, 0 * G, G, G),
                      pygame.Rect(1 * G, 0 * G, G, G),
                      pygame.Rect(1 * G, 1 * G, G, G),
                      pygame.Rect(2 * G, 1 * G, G, G)]
        self.color = 'red'
        
    def is_move_down_allowed(self, border_bottom):
        result = None
        for rect in self.shape:
            if rect.bottom >= border_bottom:
                return False
        return True

def main():
    FRAMERATE = 60
    WIDTH, HEIGHT = 320, 512
    G = 32 # Grid size
    
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

    t = Tetromino(G)
    
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
            print(t.is_move_down_allowed(HEIGHT))
            if t.is_move_down_allowed(HEIGHT):
                for rect in t.shape:
                    rect.move_ip(0, G)
        
        # Draw
        W.fill((16, 16, 16)) # Background

        for rect in t.shape: # Tetromino
            W.fill(t.color, rect)
        
        for x in range(0, WIDTH, G): # Grid
            for y in range(0, HEIGHT, G):
                rect = pygame.Rect(x, y, G, G)
                pygame.draw.rect(W, 'gray10', rect, 1)
                
        W.blit(text_fps, (WIDTH - 26, 0))
        
        # Update screen
        pygame.display.update()
                    
    pygame.quit()

if __name__ == '__main__':
    main()