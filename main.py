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


def changeInterface(interfacelist, flag):
    for interface in interfacelist:
        if interface.flag == flag:
            interface.active = True
        else:
            interface.active = False

def change_food(aliment):
    """fonction qui place les images correspondant a l'aliment selectionné """
    for elt in classes.list_cases:
        elt.set_seed(aliment.image_seed1)
        screen.blit(elt.get_seed(), elt.get_pose())


# Liste de boutons
ttle_screen_buttons = [
    classes.Button(screen.get_width() // 4 - 30, screen.get_height() // 4 * 3, "Play", 1, 2, 2, True),
    classes.Button(screen.get_width() // 4 * 3 - 30, screen.get_height() // 4 * 3, "Quit", (-1), 2, 2, True,
                   lambda: game_quit())
]

main_screen_buttons = [
    classes.Button(screen.get_width() // 100, screen.get_height() // 50, "Sav&Quit", 0, 2, 2, True)
]

fields_buttons = []

#Liste des interfaces
title_screen = classes.Interface(ttle_screen_buttons, 0, True, screen, assets.title_background)
                                 #background_color=(47, 129, 54))

# On crée le fond en mettant de la grass random
#title_background = pygame.surface.Surface(screen.get_size())
#title_background.set_colorkey((0, 0, 0))
#for x in range(screen.get_width() // 30 + 1):
#    for y in range(screen.get_height() // 27 + 1):
#        r = random.random()
#        if r < .24:
#            title_background.blit(assets.grass, (x * 30, y * 30))
#        elif r < .30:
#            title_background.blit(assets.short_grass, (x * 30, y * 30))
#        elif r < .31:
#            title_background.blit(assets.haybale, (x * 30, y * 30))

#title_screen.addElement((title_background, (0, 0)))
title_screen.addElement((assets.title_font.render("Farmer Simulator", False, (219, 215, 101)),
                      (screen.get_width() // 2 - 400, 50, 100, 100)))


main_screen = classes.Interface([main_screen_buttons], 1, False, screen, assets.field_background)
interface_list = [title_screen, main_screen]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for interface in interface_list:
                if interface.active:
                    interface.click()
                if interface.flagchange>=0:
                    changeInterface(interface_list, interface.flagchange)


    # J'ai créé une methode dans la class Interface qui update tout ses boutons
    pygame.display.update()
    pygame.time.delay(10)



