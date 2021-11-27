import carotte as carotte
import pygame
import assets
from assets import tomato_bag_fertilizer


class Button:
    def __init__(self, x, y, text, resize_x=1, resize_y=1, text_resize=1, ombre=False,
                 on_click=lambda: print("unregistred button click")):
        # on_click est une fonction elle s'execute lorsqu'un click est détecté (regardez les lambdas)
        self.on_click = on_click
        self.screen = None
        self.sprite_list = [pygame.transform.scale(assets.button1, (60 * resize_x, 30 * resize_y)),
                            pygame.transform.scale(assets.button2, (60 * resize_x, 30 * resize_y))]
        self.sprite = self.sprite_list[0]
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text
        self.ombre = ombre
        self.button_text = assets.button_font.render(self.text, False, (255, 255, 255))
        self.button_text = pygame.transform.scale(self.button_text, (
            self.button_text.get_width() * text_resize, self.button_text.get_height() * text_resize))
        self.button_text_ombre = assets.button_font.render(self.text, False, (0, 0, 0))
        self.button_text_ombre = pygame.transform.scale(self.button_text_ombre, (
            self.button_text_ombre.get_width() * text_resize, self.button_text_ombre.get_height() * text_resize))

    def update(self, interfaceClicked):
        # Le offset sert à ce que le text recule quand le bouton est cliqué... à voir
        offset = 2
        """Verification des valeurs"""
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.sprite = self.sprite_list[1]
            if interfaceClicked:
                self.on_click()
            if pygame.mouse.get_pressed()[0]:
                offset = 5
        else:
            self.sprite = self.sprite_list[0]

        self.screen.blit(self.sprite, (self.rect.x, self.rect.y))
        if self.ombre:
            self.screen.blit(self.button_text_ombre, (
                self.rect.x + (self.rect.width - self.button_text.get_width()) // 2 + 5,
                self.rect.y + (self.rect.height - self.button_text.get_height()) // 2 + 5))
        self.screen.blit(self.button_text, (
            self.rect.x + (self.rect.width - self.button_text.get_width()) // 2 + offset,
            self.rect.y + (self.rect.height - self.button_text.get_height()) // 2 + offset))


class Interface:
    def __init__(self, button_list, flag, state, screen, background_color=(-1, -1, -1), scale=1):
        self.button_list = button_list
        self.flag = flag
        self.active = state
        self.clicked = False
        self.screen = screen
        for button in button_list:
            button.screen = screen
        #     les éléments sont stockés dans une liste de tuple (surface, pos)
        self.elements = []
        self.background_color = background_color
        self.scale = scale
        self.case_grid = pygame.surface.Surface((600, 420))
        self.case_grid.set_colorkey((0, 0, 0))
        self.update_grid()

    def update(self):
        # Si le background n'a pas été défini, on n'affiche pas de background
        if self.background_color != (-1, -1, -1):
            self.screen.fill(self.background_color)

        # On affiche chaque éléments qui ne sont pas des cases
        for element in self.elements:
            if not isinstance(element, Case):
                self.screen.blit(element[0], element[1])

        self.screen.blit(self.case_grid, (360, 120))

        for button in self.button_list:
            button.update(self.clicked)

        self.clicked = False

    def click(self):
        self.clicked = True
        self.update()

    # Methode pour ajouter des éléments à une interface, cet élément est un tuple (surface, pos)
    def addElement(self, element):
        self.elements.append(element)

    def update_grid(self):
        self.case_grid.fill((0, 0, 0))
        for element in self.elements:
            if isinstance(element, Case):
                self.case_grid.blit(element.get_state(), element.get_pose())


# class main_interface(Interface):
#     def __init__(self):
#         super().__init__()



class Aliments:
    """Carectèristique de chaque aliments"""

    def __init__(self, name, growth_natural, growth_fertilizer, ui_element):
        self.name = name
        # self.image_seed1 = image_seed1
        # self.image_seed2 = image_seed2
        # self.image_fertilizer = image_fertilizer
        # self.image_fertilizer_ground = image_fertiliser_ground
        # self.image_natural = image_natural
        # self.image_natural_ground = image_natural_ground
        # self.image_bag_natural = image_bag_natural
        # self.image_bag_fertilizer = image_bag_fertilizer
        self.growth_natural = growth_natural
        self.growth_fertilizer = growth_fertilizer
        self.ui_element = ui_element


Carotte = Aliments("carotte",
                   [assets.carrots_seed1, assets.carrots_seed2, assets.carrots_natural_ground],
                   [assets.carrots_seed1, assets.carrots_seed2, assets.carrots_fertilizer_ground],
                   [assets.carrots_bag_natural, assets.carrots_bag_fertilizer, assets.carrots_natural,
                    assets.carrots_fertilizer])

Potato = Aliments("potato",
                  [assets.potato_seed1, assets.potato_seed2, assets.potato_natural_ground],
                  [assets.potato_seed1, assets.potato_seed2, assets.potato_fertilizer_ground],
                  [assets.potato_bag_natural, assets.potato_bag_fertilizer, assets.potato_natural,
                   assets.potato_fertilizer])

Corn = Aliments("corn",
                [assets.corn_seed1, assets.corn_seed2, assets.corn_natural_ground],
                [assets.corn_seed1, assets.corn_seed2, assets.corn_fertilizer_ground],
                [assets.corn_bag_natural, assets.corn_bag_fertilizer, assets.corn_natural,
                 assets.corn_fertilizer])

Tomato = Aliments("tomato",
                  [assets.tomato_seed1, assets.tomato_seed2, assets.tomato_natural_ground],
                  [assets.tomato_seed1, assets.tomato_seed2, assets.tomato_fertilizer_ground],
                  [assets.tomato_bag_natural, tomato_bag_fertilizer, assets.tomato_natural,
                   assets.tomato_fertilizer])

Turnip = Aliments("turnip",
                  [assets.turnip_seed1, assets.turnip_seed2, assets.turnip_natural_ground],
                  [assets.turnip_seed1, assets.turnip_seed2, assets.turnip_fertilizer_ground],
                  [assets.turnip_bag_natural, assets.turnip_bag_fertilizer, assets.turnip_natural,
                   assets.turnip_fertilizer])


class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.aliment = None
        self.growth = 0
        self.fertilized = False

    # def update(self):
    # if self.aliment is None:
    # self.compteur = 0
    # screen.blit(assets.trou, (self.x,self.y))
    # else:
    # if self.compteur < 500/self.fertilized:
    # screen.blit(self.aliment., (self.x,self.y))
    # elif self.compteur < 1000/self.fertilized:
    # screen.blit(assets.trou, (self.x,self.y))
    # elif self.compteur == 1000/self.fertilized:
    # screen.blit(assets.trou, (self.x,self.y))
    # if self.compteur < 1000/self.fertilized:
    # self.compteur += 1

    def get_pose(self):
        return self.x, self.y

    def inventory(self):
        return self.aliment

    def set_aliment(self, aliments):
        self.aliment = aliments

    def get_aliment(self):
        return self.aliment

    def get_state(self):
        if self.aliment is None:
            self.growth = 0

            return assets.trou
        else:
            if self.fertilized == False:
                return self.aliment.growth_natural[self.growth]
            else:
                return self.aliment.growth_fertilizer[self.growth]

    def next_state(self):
        if self.growth == 2:
            self.aliment = None
            self.growth = 0
        #     METTRE ICI DANS L'INVENTAIRE
        else:
            self.growth += 1

    def set_count(self, number):
        self.fertilized = number


# Création des cases
# list_cases = [[classes.Case(360+x*30, 120+y*30) for x in range(20)] for y in range(12)]
list_cases = []
for i in range(20):
    for j in range(14):
        list_cases.append(
            Case(i * 30, j * 30))
