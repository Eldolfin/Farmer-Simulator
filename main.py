import pygame
import sys
import yamlManager
import random

pygame.init()
# pour la taille de la fenêtre, on va voir dans la config yaml les valeurs
screen = pygame.display.set_mode(
    (yamlManager.config["screen_settings"]["size_x"], yamlManager.config["screen_settings"]["size_y"]))


def game_quit():
    #     mettre ici une sauvegarde du jeu
    pygame.quit()
    sys.exit()


# Importé après avoir init et ouvert le screen sinon il y a une erreur
import assets
import classes

# Liste de boutons
buttons = [
    classes.Button(screen.get_width() // 4 - 30, screen.get_height() // 4 * 3, "Play", 2, 2, True),
    classes.Button(screen.get_width() // 4 * 3 - 30, screen.get_height() // 4 * 3, "Quit", 2, 2, True,
                   lambda: game_quit())
]

# On crée le fond en mettant de la grass random
background = pygame.surface.Surface(screen.get_size())
background.set_colorkey((0, 0, 0))
for x in range(screen.get_width() // 30 + 1):
    for y in range(screen.get_height() // 27 + 1):
        r = random.random()
        if r < .24:
            background.blit(assets.grass, (x * 30, y * 30))
        elif r < .30:
            background.blit(assets.short_grass, (x * 30, y * 30))
        elif r < .31:
            background.blit(assets.haybale, (x * 30, y * 30))

interface = classes.Interface(buttons, True, screen,
                              background_color=(47, 129, 54))
interface.addElement((background, (0, 0)))
interface.addElement((assets.title_font.render("Farmer Simulator", False, (219, 215, 101)),
                      (screen.get_width() // 2 - 400, 50, 100, 100)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            interface.click()

    # J'ai créé une methode dans la class Interface qui update tout ses boutons
    interface.update()

    pygame.display.update()
    pygame.time.delay(10)
