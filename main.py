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

Day = 1

palier_camps = [0, 100, 500, 1000, 2500, 5000]

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


def change_food(case, aliment):
    """fonction qui place les images correspondant a l'aliment selectionné """
    # print(aliment.name)
    if not main_screen.selected_case is None and case.get_aliment() is None:
        case.set_aliment(aliment)
        # screen.blit(assets.carrots_seed1, elt.get_pose())


def addToInventory(element):
    classes.playerInventory.elements[element] += 1


def randomize_shop():
    item_list = []
    coords = [(5, -15), (5, 15), (35, -15), (35, 15)]
    r = random.randint(0, 3)
    l1 = random.sample([classes.Carotte, classes.Potato, classes.Corn, classes.Tomato, classes.Turnip], r)
    l2 = random.sample([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5], r)
    for item in l1:
        item_list.append(
            classes.Button_counter(screen.get_width() // 100 + coords[0][0], screen.get_height() // 2 + coords[0][1],
                                   item.ui_element[random.randint(0, 1)], 0.5, 1, l2[l1.index(item)],
                                   on_click=lambda: addToInventory(item.name)))
        coords.remove(coords[0])
    return item_list


def add_camps(number):
    main_screen.screen.add_element((assets.camps, (2 + (number % 3) * 100, 440 + 100 * (number // 3))))


# Classe nutural tois fertilizer un choix sur 2

interface_list = []
# Liste de boutons
title_screen_buttons = [
    classes.Button_text(screen.get_width() // 4 - 30, screen.get_height() // 4 * 3, "New Game", 2, 2, ombre=True,
                        on_click=lambda: change_interface(interface_list, 1)),
    classes.Button_text(screen.get_width() // 4 * 3 - 30, screen.get_height() // 4 * 3, "Quit", 2, 2, ombre=True,
                        on_click=lambda: game_quit())
]

if yamlManager.config["last_save"] != "null":
    title_screen_buttons.append(
        classes.Button_text(screen.get_width() // 2 - 30, screen.get_height() // 4 * 3, "Continue", 2, 2, ombre=True,
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

title_screen.add_element((title_background, (0, 0)))
title_screen.add_element((assets.title_font.render("Farmer Simulator", False, (0, 0, 0)),
                          (screen.get_width() // 2 - 400 + 3, 50 + 3, 100, 100)))
title_screen.add_element((assets.title_font.render("Farmer Simulator", False, (219, 215, 101)),
                          (screen.get_width() // 2 - 400, 50, 100, 100)))

main_screen_buttons = [
    classes.Button_text(screen.get_width() // 100, screen.get_height() // 50, "Save & Quit", 4, 2, ombre=True,
                        on_click=lambda: change_interface(interface_list, 0)),
    classes.Button_text(screen.get_width() // 100, screen.get_height() // 4, "Shop", 4, 2, ombre=True,
                        on_click=lambda: change_interface(interface_list, 2)),
    # classes.Button(screen.get_width()//10*4,screen.get_height()//50,assets.)
]
for i in range(len(classes.aliment_list)):
    main_screen_buttons.append(
        classes.Button_aliment(screen.get_width() // 10 * (5 + i), screen.get_height() // 50, classes.aliment_list[i]))

main_screen = classes.main_interface(main_screen_buttons, 1, False, screen)
main_screen.add_element((assets.field_background, (0, 0)))
for elt in classes.list_cases:
    main_screen.add_element(elt)

shop_screen = classes.Interface([], 2, False, screen)
shop_screen.add_element((assets.shop_background, (20, 20)))

interface_list = [title_screen, main_screen, shop_screen]

growth_event = pygame.USEREVENT + 1
pygame.time.set_timer(growth_event, 1000)

daylight_event = pygame.USEREVENT + 2
pygame.time.set_timer(daylight_event, 180000)

shop_screen.set_buttons(randomize_shop())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for interface in interface_list:
                if interface.active:
                    interface.click()
                    if isinstance(interface, classes.main_interface):
                        interface.update_grid()

        if event.type == growth_event:
            for case in classes.list_cases:
                case.dotick()
            main_screen.update_grid()

        if event.type == daylight_event:
            shop_screen.set_buttons(randomize_shop())
            Day += 1

        for interface in interface_list:
            if interface.active:
                interface.update()

    # J'ai créé une methode dans la class Interface qui update tout ses boutons
    pygame.display.update()
    pygame.time.delay(10)

"""The year is 2071. Humanity as we know it is in a state of fading, as the post apocalyptic era has settled for decades, ending civilization in the process.
Having only known ruined cities, you chose to live in an old farm you found so as to learn to live by yourself, in hopes of surviving and maybe a better future..."""
