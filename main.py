import pygame
import sys
import yamlManager

pygame.init()
screen = pygame.display.set_mode((960, 540))

# Importé après avoir init et ouvert le screen sinon il y a une erreur
import assets
import classes

# Test d'interface
interface = classes.Interface([classes.Button(500, 250, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")], True)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for button in interface.button_list:
        button.update(screen)

    pygame.display.update()
    pygame.time.delay(10)
