import pygame.image

grass = pygame.image.load("assets/tilesets/tallgrass.png").convert().subsurface((0, 162, 27, 30))
button1 = pygame.image.load("assets/tilesets/button1.png").convert()
button2 = pygame.image.load("assets/tilesets/button2.png").convert()
title_font = pygame.font.Font("assets/fonts/Terminus (TTF) Bold 700 (1).ttf", 100)
button_font = pygame.font.Font("assets/fonts/Terminus (TTF) Bold 700 (1).ttf", 30)
