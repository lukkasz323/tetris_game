import pygame
import random
from data import ROTATION


FRAMERATE = 60
WIDTH, HEIGHT = 320, 512
G = 32 # Grid size
LINE_LENGTH = WIDTH // G


class Tetromino:
    def __init__(self, bag):
        self.type: str
        self.color: str
        self.shape: list
        self.rotation = 0
        
        self.set_next_shape(bag)
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
            
    
    def rotate(self): 
        # Shift rects
        for rect, shift in zip(self.shape, ROTATION[self.type][self.rotation]):
            rect.topleft = rect.topleft[0] + shift[0] * G, rect.topleft[1] + shift[1] * G
        # Update rotation info
        if self.rotation >= 3:
            self.rotation = 0
        else:
            self.rotation += 1
    
    
    def set_next_shape(self, bag):
        types = ('I', 'O', 'T', 'J', 'L', 'S', 'Z')
        shapes = (((0, 0), (1, 0), (2, 0), (3, 0)), # I
                  ((1, 0), (2, 0), (1, 1), (2, 1)), # O
                  ((0, 1), (1, 1), (2, 1), (1, 0)), # T
                  ((0, 1), (1, 1), (2, 1), (0, 0)), # J
                  ((0, 1), (1, 1), (2, 1), (2, 0)), # L
                  ((0, 1), (1, 1), (1, 0), (2, 0)), # S
                  ((0, 0), (1, 0), (1, 1), (2, 1))) # Z
        colors = ('cyan', 'yellow', 'magenta', 'blue', 'orange', 'green', 'red')
        
        if bag.index > 6:
            bag.index = 0
            random.shuffle(bag.bag)
        next = bag.bag[bag.index]
        bag.index += 1
        
        self.type = types[next]
        self.shape = [pygame.Rect(rect[0] * G, rect[1] * G, G, G) for rect in shapes[next]]
        self.color = colors[next]
        
        
    def is_move_allowed(self, direction, abandoned):
        # Check for tetrominoes collision
        shadow_shape = None
        
        match direction:
            case 'down': shadow_shape = self.clone_and_move(0, G)
            case 'left': shadow_shape = self.clone_and_move(-G, 0)
            case 'right': shadow_shape = self.clone_and_move(G, 0)
            case _: raise NotImplementedError()
            
        if is_tetro_collision(shadow_shape, abandoned):
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
    
        
    def is_rotate_allowed(self, abandoned):
        # Shadow shape for testing collision
        shadow_shape = []
        for rect in self.shape:
            shadow_shape.append(rect.copy())
        
        # Rotate shadow shape
        for shadow_rect, shift in zip(shadow_shape, ROTATION[self.type][self.rotation]):
            shadow_rect.topleft = shadow_rect.topleft[0] + shift[0] * G, shadow_rect.topleft[1] + shift[1] * G
        
        # Check for collision with other tetrominoes
        if is_tetro_collision(shadow_shape, abandoned):
            return False
        
        # Check for collision with the border
        for shadow_rect in shadow_shape:
            if shadow_rect.bottom > HEIGHT or\
                shadow_rect.left < 0 or\
                shadow_rect.right > WIDTH:
                    return False
        
        # Allow rotate if there's no collision  
        return True
        
        
class Bag:
    def __init__(self):
        self.bag = [0, 1, 2, 3, 4, 5, 6]
        self.index = 7
        

def respawn_tetro(current_tetro, abandoned, bag):
    if current_tetro:
        abandoned.append(current_tetro)
    return Tetromino(bag)


def clear_lines(clear, abandoned):
    for cleared_rect in clear:
        for tetro in abandoned:
            try:
                tetro.shape.remove(cleared_rect)
            except ValueError:
                pass
    
    lines_amount = len(clear) // LINE_LENGTH
    for _ in range(lines_amount):
        for tetro in abandoned:
            tetro.move(0, G)


def is_tetro_collision(shape, abandoned):
    for rect in shape:
        for foreign_tetro in abandoned:
            for foreign_rect in foreign_tetro.shape:
                if rect.colliderect(foreign_rect):
                    return True
    return False


def get_rects_to_clear(abandoned):
    clear = []
    rects = []
    rects_values = []
    
    for tetro in abandoned:
        for rect in tetro.shape:
            rects.append(rect)
            rects_values.append(rect.top)
            
    for i, value in enumerate(rects_values):
        if rects_values.count(value) >= 10:
            clear.append(rects[i])
    
    return clear


def main():
    # Init
    pygame.init()
    
    # Display
    W = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')
    
    # Timers
    TIMER = pygame.event.custom_type()
    ACCELERATE = pygame.event.custom_type()
    pygame.time.set_timer(TIMER, 1000)

    # Other 
    font = pygame.font.SysFont('notomono', 20)
    clock = pygame.time.Clock()
    bag = Bag()
    abandoned = []
    score = 0
    
    current_tetro = respawn_tetro(None, abandoned, bag)
    
    # Loop every frame
    run = True
    while run:
        # Limit framerate
        clock.tick(FRAMERATE)
        
        # Handle events
        event_timer = False
        event_accelerate = False
        event_keyup = False
        key_w = False
        key_s = False
        key_a = False
        key_d = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == TIMER:
                event_timer = True
            elif event.type == ACCELERATE:
                event_timer = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    key_w = True
                elif event.key == pygame.K_s:
                    key_s = True
                elif event.key == pygame.K_a:
                    key_a = True
                elif event.key == pygame.K_d:
                    key_d = True
            elif event.type == pygame.KEYUP:
                event_keyup = True
                
        # Logic
        fps = round(clock.get_fps())
        text_score = font.render(f'Score: {score}', True, 'white')
        
        print(f'FPS: {fps}') # Somehow prevents crash?

        if event_timer or event_accelerate:
            if current_tetro.is_move_allowed('down', abandoned):
                current_tetro.move(0, G)
            else:
                current_tetro = respawn_tetro(current_tetro, abandoned, bag)
                clear = get_rects_to_clear(abandoned)
                if len(clear) >= LINE_LENGTH:
                    clear_lines(clear, abandoned)
                    
                # Handle game over
                if is_tetro_collision(current_tetro.shape, abandoned):
                    bag = Bag()
                    abandoned = []
                    score = 0
                    current_tetro = respawn_tetro(None, abandoned, bag)
                
        if (not event_timer) and (not event_accelerate):
            if key_a:
                if current_tetro.is_move_allowed('left', abandoned):
                    current_tetro.move(-G, 0)
            if key_d:
                if current_tetro.is_move_allowed('right', abandoned):
                    current_tetro.move(G, 0)
            if key_w:
                if current_tetro.is_rotate_allowed(abandoned):
                    current_tetro.rotate()

        if key_s:
            pygame.time.set_timer(ACCELERATE, 50)
        if event_keyup:
            pygame.time.set_timer(ACCELERATE, 0)
            
        
        
        # Draw
        W.fill((16, 16, 16)) # Background

        for tetro in abandoned: # Old tetrominoes
            for rect in tetro.shape:
                W.fill(tetro.color, rect)
                
        for rect in current_tetro.shape: # Current tetromino
            W.fill(current_tetro.color, rect)
        
        for x in range(0, WIDTH, G): # Grid
            for y in range(0, HEIGHT, G):
                rect = pygame.Rect(x, y, G, G)
                pygame.draw.rect(W, 'gray10', rect, 1)
                
        W.blit(text_score, (4, 0)) # FPS counter
        
        # Update screens
        pygame.display.update()
                     
    pygame.quit()


if __name__ == '__main__':
    main()