import pygame
import sys
import yamlManager
import random

pygame.init()
# pour la taille de la fenêtre, on va voir dans la config yaml les valeurs
screen = pygame.display.set_mode(
    (yamlManager.config["screen_settings"]["size_x"], yamlManager.config["screen_settings"]["size_y"]))

# Importé après avoir init et ouvert le screen sinon il y a une erreur
import assets
import classes


def game_quit():
    #     mettre ici une sauvegarde du jeu
    pygame.quit()
    sys.exit()


def change_interface(interface_list, flag):
    for interface in interface_list:
        if interface.flag == flag:
            interface.active = True
        else:
            interface.active = False


def change_food(aliment):
    """fonction qui place les images correspondant a l'aliment selectionné """
    # print(aliment.name)
    for case in classes.list_cases:
        if case.get_aliment() is None:
            case.set_aliment(classes.Carotte)
        # screen.blit(assets.carrots_seed1, elt.get_pose())


interface_list = []
# Liste de boutons
title_screen_buttons = [
    classes.Button(screen.get_width() // 4 - 30, screen.get_height() // 4 * 3, "New Game", 2, 2, ombre=True,
                   on_click=lambda: change_interface(interface_list, 1)),
    classes.Button(screen.get_width() // 4 * 3 - 30, screen.get_height() // 4 * 3, "Quit", 2, 2, ombre=True,
                   on_click=lambda: game_quit())
]

if yamlManager.config["last_save"] != "null":
    title_screen_buttons.append(
        classes.Button(screen.get_width() // 2 - 30, screen.get_height() // 4 * 3, "Continue", 2, 2, ombre=True,
                       on_click=lambda: change_interface(interface_list, 1)))

# Liste des interfaces
title_screen = classes.Interface(title_screen_buttons, 0, True, screen, background_color=(132, 74, 14))
# background_color=(47, 129, 54))

# On crée le fond en mettant de la grass random
title_background = pygame.surface.Surface(screen.get_size())
title_background.set_colorkey((0, 0, 0))
for x in range(screen.get_width() // 30 + 1):
    for y in range(screen.get_height() // 27 + 1):
        r = random.random()
        if r < .01:
            title_background.blit(assets.trou, (x * 30, y * 30))
        elif r < .10:
            title_background.blit(assets.short_grass, (x * 30, y * 30))
        elif r < .105:
            title_background.blit(assets.haybale, (x * 30, y * 30))

title_screen.addElement((title_background, (0, 0)))
title_screen.addElement((assets.title_font.render("Farmer Simulator", False, (0, 0, 0)),
                         (screen.get_width() // 2 - 400 + 3, 50 + 3, 100, 100)))
title_screen.addElement((assets.title_font.render("Farmer Simulator", False, (219, 215, 101)),
                         (screen.get_width() // 2 - 400, 50, 100, 100)))

main_screen_buttons = [
    classes.Button(screen.get_width() // 100, screen.get_height() // 50, "Save & Quit", 4, 2, ombre=True,
                   on_click=lambda: change_interface(interface_list, 0)),
    classes.Button(screen.get_width() // 100 + 100, screen.get_height() // 50 + 100, "Carrot", 4, 2, True,
                   on_click=lambda: change_food(classes.Carotte))
]
main_screen = classes.Interface(main_screen_buttons, 1, False, screen)
main_screen.addElement((assets.field_background, (0, 0)))
for elt in classes.list_cases:
    main_screen.addElement(elt)

interface_list = [title_screen, main_screen]

growth_event = pygame.USEREVENT + 1
pygame.time.set_timer(growth_event, 5000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for interface in interface_list:
                if interface.active:
                    interface.click()
                    interface.update_grid()

        if event.type == growth_event:
            for cases in classes.list_cases:
                if not cases.get_aliment is None:
                    cases.next_state()
            main_screen.update_grid()

        for interface in interface_list:
            if interface.active:
                interface.update()

    # J'ai créé une methode dans la class Interface qui update tout ses boutons
    pygame.display.update()
    pygame.time.delay(10)

"""The year is 2071. Humanity as we know it is in a state of fading, as the post apocalyptic era has settled for decades, ending civilization in the process.
Having only known ruined cities, you chose to live in an old farm you found so as to learn to live by yourself, in hopes of surviving and maybe a better future..."""
