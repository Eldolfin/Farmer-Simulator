import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((960, 540))

import assets

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(assets.grass,(0,0))
    pygame.display.update()
    pygame.time.delay(10)
