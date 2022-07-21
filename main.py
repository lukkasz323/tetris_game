import pygame
import random

class Tetromino:
    def __init__(self, G):
        self.type = None
        self.shape = []
        self.color = 'white'
        self.set_random_shape(G)
        self.move(3 * G, 0)
        
    def move(self, x, y):
        for rect in self.shape:
            rect.move_ip(x, y)
            
    def clone_and_move(self, x, y):
        clone = []
        for rect in self.shape:
            clone_rect = rect.move(x, y)
            clone.append(clone_rect)
        return clone
            
    def set_random_shape(self, G):
        types = ('I', 'O', 'T', 'J', 'L', 'S', 'Z')
        shapes = (((0, 0), (1, 0), (2, 0), (3, 0)), # I
                  ((1, 0), (2, 0), (1, 1), (2, 1)), # O
                  ((0, 0), (1, 0), (2, 0), (1, 1)), # T
                  ((0, 0), (1, 0), (2, 0), (2, 1)), # J
                  ((0, 1), (1, 1), (2, 1), (2, 0)), # L
                  ((0, 1), (1, 1), (1, 0), (2, 0)), # S
                  ((0, 0), (1, 0), (1, 1), (2, 1))) # Z
        colors = ('cyan', 'yellow', 'magenta', 'blue', 'orange', 'green', 'red')
        
        rng = random.randint(0, 6)
        self.type = types[rng]
        self.shape = [pygame.Rect(rect[0] * G, rect[1] * G, G, G) for rect in shapes[rng]]
        self.color = colors[rng]
        
    def is_move_allowed(self, direction, G, WIDTH, HEIGHT, old_tetro_list):
        # Check for tetrominoes collision
        shadow_shape = None
        match direction:
            case 'down': shadow_shape = self.clone_and_move(0, G)
            case 'left': shadow_shape = self.clone_and_move(-G, 0)
            case 'right': shadow_shape = self.clone_and_move(G, 0)
            case _: raise NotImplementedError()
        for shadow_rect in shadow_shape:
            for tetro in old_tetro_list:
                for foreign_rect in tetro.shape:
                    if shadow_rect.colliderect(foreign_rect):
                        return False    
        # Check for border collision
            match direction:
                case 'down':
                    for rect in self.shape:
                        if rect.bottom >= HEIGHT:
                            return False
                case 'left':
                    for rect in self.shape:
                        if rect.left <= 0:
                            return False
                case 'right':
                    for rect in self.shape:
                        if rect.right >= WIDTH:
                            return False
        # Allow move if there's no collision
        return True 

def respawn_tetro(current_tetro, old_tetro_list, G):
    if current_tetro:
        old_tetro_list.append(current_tetro)
    return Tetromino(G)

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
    pygame.time.set_timer(TIMER, 1000)

    # Other
    font = pygame.font.SysFont('notomono', 20)
    clock = pygame.time.Clock()
    old_tetro_list = []
    
    current_tetro = respawn_tetro(None, old_tetro_list, G)
    
    run = True
    while run:
        # Limit framerate
        clock.tick(FRAMERATE)
        
        # Handle events
        event_timer = False
        event_keyup = False
        key_left = False
        key_right = False
        key_down = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == TIMER:
                event_timer = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    key_left = True
                if event.key == pygame.K_RIGHT:
                    key_right = True
                if event.key == pygame.K_DOWN:
                    key_down = True
            if event.type == pygame.KEYUP:
                event_keyup = True
                
        # Logic
        fps = round(clock.get_fps())
        text_fps = font.render(f'{fps}', True, 'white')

        if event_timer:
            if current_tetro.is_move_allowed('down', G, WIDTH, HEIGHT, old_tetro_list):
                current_tetro.move(0, G)
            else:
                current_tetro = respawn_tetro(current_tetro, old_tetro_list, G)
                
        if not event_timer:
            if key_left:
                if current_tetro.is_move_allowed('left', G, WIDTH, HEIGHT, old_tetro_list):
                    current_tetro.move(-G, 0)
            if key_right:
                if current_tetro.is_move_allowed('right', G, WIDTH, HEIGHT, old_tetro_list):
                    current_tetro.move(G, 0)

        if key_down:
            pygame.time.set_timer(TIMER, 50)
        if event_keyup:
            pygame.time.set_timer(TIMER, 1000)
                
        # Draw
        W.fill((16, 16, 16)) # Background

        for tetro in old_tetro_list: # Old tetrominoes
            for rect in tetro.shape:
                W.fill(tetro.color, rect)
                
        for rect in current_tetro.shape: # Current tetromino
            W.fill(current_tetro.color, rect)
        
        for x in range(0, WIDTH, G): # Grid
            for y in range(0, HEIGHT, G):
                rect = pygame.Rect(x, y, G, G)
                pygame.draw.rect(W, 'gray10', rect, 1)
                
        W.blit(text_fps, (WIDTH - 26, 0)) # FPS counter
        
        # Update screen
        pygame.display.update()
                    
    pygame.quit()

if __name__ == '__main__':
    main()
    
# TODO: Improve rng
# Bug: Move down not working when spamming move left/right.