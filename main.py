import pygame
import random

class Tetromino:
    def __init__(self, G):
        self.shape = []
        self.color = 'white'
        self.set_random_shape(G)
        
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
        shapes = (((0, 0), (1, 0), (2, 0), (3, 0)),
                  ((0, 0), (1, 0), (0, 1), (1, 1)),
                  ((0, 0), (1, 0), (2, 0), (1, 1)),
                  ((0, 0), (1, 0), (2, 0), (2, 1)),
                  ((0, 0), (1, 0), (1, 1), (2, 1)))
        colors = ('cyan', 'yellow', 'magenta', 'orange', 'green')
        
        rng = random.randint(0, 4)
        self.shape = [pygame.Rect(rect[0] * G, rect[1] * G, G, G) for rect in shapes[rng]]
        self.color = colors[rng]
        
    def is_move_down_allowed(self, G, HEIGHT, old_tetro_list):
        # Check for tetrominoes below
        shadow_shape = self.clone_and_move(0, G)
        for shadow_rect in shadow_shape:
            for tetro in old_tetro_list:
                for foreign_rect in tetro.shape:
                    if shadow_rect.colliderect(foreign_rect):
                        return False    
        # Check for border below
        for rect in self.shape:
            if rect.bottom >= HEIGHT:
                return False
        return True
    
    def is_move_left_allowed(self, G, WIDTH, old_tetro_list):
        # Check for tetrominoes left
        shadow_shape = self.clone_and_move(-G, 0)
        for shadow_rect in shadow_shape:
            for tetro in old_tetro_list:
                for foreign_rect in tetro.shape:
                    if shadow_rect.colliderect(foreign_rect):
                        return False    
        # Check for border left
        for rect in self.shape:
            if rect.left <= 0:
                return False
        return True
    
    def is_move_right_allowed(self, G, WIDTH, old_tetro_list):
        # Check for tetrominoes right
        shadow_shape = self.clone_and_move(G, 0)
        for shadow_rect in shadow_shape:
            for tetro in old_tetro_list:
                for foreign_rect in tetro.shape:
                    if shadow_rect.colliderect(foreign_rect):
                        return False    
        # Check for border right
        for rect in self.shape:
            if rect.right >= WIDTH:
                return False
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
    pygame.time.set_timer(TIMER, 100)

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == TIMER:
                event_timer = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if current_tetro.is_move_left_allowed(G, WIDTH, old_tetro_list):
                        current_tetro.move(-G, 0)
                if event.key == pygame.K_RIGHT:
                    if current_tetro.is_move_right_allowed(G, WIDTH, old_tetro_list):
                        current_tetro.move(G, 0)
                # Debug
                if event.key == pygame.K_SPACE:
                    current_tetro = respawn_tetro(current_tetro, old_tetro_list, G)
                if event.key == pygame.K_q:
                    pygame.time.set_timer(TIMER, 0)
                if event.key == pygame.K_w:
                    pygame.time.set_timer(TIMER, 500)
                if event.key == pygame.K_e:
                    pygame.time.set_timer(TIMER, 100)
                if event.key == pygame.K_r:
                    pygame.time.set_timer(TIMER, 1)
                    
        # Logic
        fps = round(clock.get_fps())
        text_fps = font.render(f'{fps}', True, 'yellow')

        if event_timer:
            if current_tetro.is_move_down_allowed(G, HEIGHT, old_tetro_list):
                current_tetro.move(0, G)
            else:
                current_tetro = respawn_tetro(current_tetro, old_tetro_list, G)
        
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
                
        W.blit(text_fps, (WIDTH - 26, 0))
        
        # Update screen
        pygame.display.update()
                    
    pygame.quit()

if __name__ == '__main__':
    main()