import pygame
import random

class Tetromino:
    def __init__(self, G):
        self.shape = ()
        self.color = 'white'
        
    def move(self, x, y):
        for rect in self.shape:
            rect.move_ip(x, y)
    
    def set_random_shape(self, G):
        shapes = (((0, 0), (1, 0), (2, 0), (3, 0)),
                  ((0, 0), (1, 0), (0, 1), (1, 1)),
                  ((0, 0), (1, 0), (2, 0), (1, 1)),
                  ((0, 0), (1, 0), (2, 0), (2, 1)),
                  ((0, 0), (1, 0), (1, 1), (2, 1)))
        colors = ('cyan', 'yellow', 'magenta', 'orange', 'green')
        
        rng = random.randint(0, 4)
        self.shape = [pygame.Rect(rect[0] * G, rect[1] * G, G, G) for rect in shapes[rng]]
        self.color = colors[rng]
        
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
    pygame.time.set_timer(TIMER, 500)

    # Other
    font = pygame.font.SysFont('notomono', 20)
    clock = pygame.time.Clock()

    t = Tetromino(G)
    t.set_random_shape(G)
    
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
            if t.is_move_down_allowed(HEIGHT):
                t.move(0, G)
        
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