import menu_screen
import assets
import pygame, sys

pygame.init()
screen = pygame.display.set_mode((960, 540))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(assets.grass)
    pygame.display.update()
    pygame.time.delay(10)
