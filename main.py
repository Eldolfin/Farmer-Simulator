from turtle import color

import pygame
import sys

import self as self

import yamlManager
import random

pygame.init()
# pour la taille de la fenêtre, on va voir dans la config.yml yaml les valeurs
screen = pygame.display.set_mode(
    (yamlManager.config["screen_settings"]["size_x"], yamlManager.config["screen_settings"]["size_y"]))

# Importé après avoir init et ouvert le screen sinon il y a une erreur
import assets
import classes

Day = 1

palier_camps = [0, 100, 500, 1000, 2500, 5000]


def save_game():
    yamlManager.dump_PlayerData(classes.player_data)
    yamlManager.log_save()
    # change_interface(interface_list, 0)
    game_quit()

def game_quit():
    #     mettre ici une sauvegarde du jeu
    pygame.quit()
    sys.exit()

def load_save():
    stored_player_data = yamlManager.load_PlayerData()
    classes.player_data.player_inventory.elements = stored_player_data.player_inventory.elements
    for i in range(len(classes.player_data.list_cases)):
        classes.player_data.list_cases[i].aliment_type = stored_player_data.list_cases[i].aliment_type
        classes.player_data.list_cases[i].fertilized = stored_player_data.list_cases[i].fertilized
        classes.player_data.list_cases[i].growth = stored_player_data.list_cases[i].growth
        # classes.player_data.list_cases[i].
    print(classes.player_data.player_inventory.elements)
    change_interface(interface_list, 1)



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


def randomize_shop():
    item_list = []
    compt = 0
    coords_bag = 0
    coords = [(5, -15), (5, 15), (35, -15), (35, 15)]
    r = 4
    l1 = random.sample([classes.Carotte, classes.Potato, classes.Corn, classes.Tomato, classes.Turnip], r)
    l2 = random.sample([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5], r)

    def buy_function(button):
        can_pay = classes.playerInventory.try_pay(button.anydata[0].price_buy)
        if can_pay:
            classes.playerInventory.elements[button.anydata[0].name + " seeds"] += 1
        return can_pay

    for item in l1:
        item_list.append(
            classes.Button_counter(40 + coords_bag * 75, 80,
                                   item.ui_element[0], 10, 1, 1, on_click=lambda x: buy_function(x),
                                   use_custom_onclick=True, anydata=[item]))
        coords.remove(coords[0])
        shop_screen.add_element(
            (assets.button_font.render(str(item.price_buy), False, (0, 0, 0)), (55 + coords_bag * 75, 160)))
        coords_bag += 1
        # print(classes.playerInventory.elements)

    item_list.append(classes.Button(321, 18, assets.leave_button, on_click=lambda: change_interface(interface_list, 1)))
    return item_list


nb_camps = 0


def update_camps():
    global nb_camps
    if nb_camps < 6 and classes.playerInventory.elements["money"] >= palier_camps[nb_camps]:
        main_screen.add_element((assets.camps, (2 + (nb_camps % 3) * 100, 340 + 100 * (nb_camps // 3))))
        nb_camps += 1


# Classe nutural tois fertilizer un choix sur 2

interface_list = []
# Liste de boutons
title_screen_buttons = [
    classes.Button_text(screen.get_width() // 4 - 30, screen.get_height() // 4 * 3, "New Game", 2, 2, ombre=True,
                        on_click=lambda: change_interface(interface_list, 5)),
    classes.Button_text(screen.get_width() // 4 * 3 - 30, screen.get_height() // 4 * 3, "Quit", 2, 2, ombre=True,
                        on_click=lambda: game_quit())
]

if yamlManager.config["last_save"] != "None":
    title_screen_buttons.append(
        classes.Button_text(screen.get_width() // 2 - 30, screen.get_height() // 4 * 3, yamlManager.config["last_save"], 2, 2,text_resize=0.5, ombre=True,
                            on_click=lambda: load_save()))


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
title_screen.add_element((assets.title_font.render("Apocalyptic Farmer", False, (0, 0, 0)),
                          (screen.get_width() // 2 - 450 + 3, 50 + 3)))
title_screen.add_element((assets.title_font.render("Apocalyptic Farmer", False, (219, 215, 101)),
                          (screen.get_width() // 2 - 450, 50)))

main_screen_buttons = [
    classes.Button_text(screen.get_width() // 100, screen.get_height() // 50, "Save & Quit", 4, 2, ombre=True,
                        on_click=lambda:save_game()),
    classes.Button_text(screen.get_width() // 100, screen.get_height() // 50 + 70, "Shop", 4, 2, ombre=True,
                        on_click=lambda: change_interface(interface_list, 2)),
    # classes.Button(screen.get_width()//10*4,screen.get_height()//50,assets.)
]

menu_ValueText_list = []
for i in range(len(classes.aliment_list)):
    main_screen_buttons.append(
        classes.Button_aliment(screen.get_width() // 10 * (5 + i), screen.get_height() // 50, classes.aliment_list[i]))

    menu_ValueText_list.append(classes.ValueText(screen.get_width() // 10 * (5 + i) + 65, screen.get_height() // 20,
                                                 str(classes.playerInventory.elements[
                                                         classes.aliment_list[i].name + " seeds"]), color=(0, 0, 0)))
menu_ValueText_list.append(
    classes.ValueText(screen.get_width() // 100, screen.get_height() // 50 + 140, "$0", 2, True, color=(0, 255, 0)))

main_screen = classes.main_interface(main_screen_buttons, 1, False, screen)
main_screen.add_element((assets.field_background, (0, 0)))
for elt in classes.list_cases:
    main_screen.add_element(elt)

for elt in menu_ValueText_list:
    main_screen.add_element(elt)

shop_screen = classes.Interface([], 2, False,
                                screen)
shop_screen.add_element((assets.shop_background, (50, 20)))

intro_screen = classes.Interface([classes.Button_text(screen.get_width() - 70, screen.get_height() - 60, "Next", 1, 1,
                                                      on_click=lambda: change_interface(interface_list, 1))], 5, False,
                                 screen, (0, 0, 0))

intro_screen.add_element((assets.intro_background, (0, 0)))
intro_screen.add_element((assets.button_font.render("The year is 2071. Humanity as we know it is in a state of", False,
                                                    (219, 215, 101)), (5, 100)))
intro_screen.add_element((assets.button_font.render("fading, as the post apocalyptic era has settled for decades,",
                                                    False, (219, 215, 101)), (5, 125)))
intro_screen.add_element((assets.button_font.render("ending civilization in the process. Having only known ruined",
                                                    False, (219, 215, 101)), (5, 150)))
intro_screen.add_element((
    assets.button_font.render("cities, you chose to live in an old farm you found so as to", False,
                              (219, 215, 101)), (5, 175)))
intro_screen.add_element((assets.button_font.render("learn to live by yourself, in hopes of surviving and maybe", False,
                                                    (219, 215, 101)), (5, 200)))
intro_screen.add_element((assets.button_font.render("a better future...", False, (219, 215, 101)), (5, 225)))

interface_list = [title_screen, main_screen, shop_screen, intro_screen]

growth_event = pygame.USEREVENT + 1
# pygame.time.set_timer(growth_event, 1000)
pygame.time.set_timer(growth_event, 300)

daylight_event = pygame.USEREVENT + 2
# pygame.time.set_timer(daylight_event, 180000)
pygame.time.set_timer(daylight_event, 7000)

shop_screen.set_buttons(randomize_shop())


# place_elt_shop = 0
# for elt in shop_screen.button:
#     shop_screen.add_element((elt.image, (40+place_elt_shop*30, 80)))
#     place_elt_shop += 2

def update_ValueTexts():
    for i in range(len(classes.aliment_list)):
        menu_ValueText_list[i].set_text(classes.playerInventory.elements[classes.aliment_list[i].name + " seeds"])
    menu_ValueText_list[5].set_text("$"+str(classes.playerInventory.elements["money"]))


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
                    if interface == shop_screen:
                        main_screen.update()

        if event.type == growth_event:
            if main_screen.active:
                for case in classes.list_cases:
                    case.dotick()
                main_screen.update_grid()

        if event.type == daylight_event:
            shop_screen.reset_elts(True)
            shop_screen.set_buttons(randomize_shop())
            Day += 1

    for interface in interface_list:
        if interface.active:
            interface.update()

    update_camps()

    update_ValueTexts()

    # J'ai créé une methode dans la class Interface qui update tout ses boutons
    pygame.display.update()
    pygame.time.delay(10)
