import pygame

def main():
    WIDTH, HEIGHT = 512, 512
    
    pygame.init()
    
    W = pygame.display.set_mode((WIDTH, HEIGHT))
    
    run = True
    while run:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    run = False
                    
    pygame.quit()

if __name__ == '__main__':
    main()