import pygame
import assets


class Button:
    def __init__(self, x, y, text, flag, resize_x=1, resize_y=1, ombre=False, on_click=lambda: print("unregistred button click")):
        # on_click est une fonction elle s'execute lorsqu'un click est détecté (regardez les lambdas)
        self.on_click = on_click
        self.flag = flag
        self.screen = None
        self.sprite_list = [pygame.transform.scale(assets.button1, (60 * resize_x, 30 * resize_y)),
                            pygame.transform.scale(assets.button2, (60 * resize_x, 30 * resize_y))]
        self.sprite = self.sprite_list[0]
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text
        self.clicked = False
        self.ombre = ombre
        self.button_text = assets.button_font.render(self.text, False, (255, 255, 255))
        self.button_text = pygame.transform.scale(self.button_text, (
            self.button_text.get_width() * resize_x, self.button_text.get_height() * resize_y))
        self.button_text_ombre = assets.button_font.render(self.text, False, (0, 0, 0))
        self.button_text_ombre = pygame.transform.scale(self.button_text_ombre, (
            self.button_text_ombre.get_width() * resize_x, self.button_text_ombre.get_height() * resize_y))

    def update(self, interfaceClicked):
        # Le offset sert à ce que le text recule quand le bouton est cliqué... à voir
        offset = 2
        """Verification des valeurs"""
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.sprite = self.sprite_list[1]
            if interfaceClicked:
                self.on_click()
                self.clicked = True
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
    def __init__(self, button_list, flag, state, screen, background_sprite):
        self.button_list = button_list
        self.flag = flag
        self.flagchange = -1
        self.active = state
        self.clicked = False
        self.screen = screen
        for button in button_list:
            button.screen = screen
        #     les éléments sont stockés dans une liste de tuple (surface, pos)
        self.elements = []
        self.background_sprite = background_sprite

    def update(self):
        # Si le background n'a pas été défini, on n'affiche pas de background
        #if self.background_color != (-1, -1, -1):
            #self.screen.fill(self.background_color)
            # On affiche chaque éléments

        self.screen.blit(self.background_sprite, (0, 0))

        for element in self.elements:
            self.screen.blit(element[0], element[1])

        for button in self.button_list:
            button.update(self.clicked)
            if button.clicked:
                self.flagchange = button.flag

        self.clicked = False

    def click(self):
        self.clicked = True
        self.update()

    # Methode pour ajouter des éléments à une interface, cet élément est un tuple (surface, pos)
    def addElement(self, element):
        self.elements.append(element)


class Aliments:
    """Carectèristique de chaque aliments"""

    def __init__(self, name, image_seed1, image_seed2, image_fertilizer, image_fertiliser_ground, image_natural, image_natural_ground, image_bag_natural, image_bag_fertilizer):
        self.name = name
        self.image_seed1 = image_seed1
        self.image_seed2 = image_seed2
        self.image_fertilizer = image_fertilizer
        self.image_fertilizer_ground = image_fertiliser_ground
        self.image_natural = image_natural
        self.image_natural_ground = image_natural_ground
        self.image_bag_natural = image_bag_natural
        self.image_bag_fertilizer = image_bag_fertilizer


class Case:
    def __init__(self, x, y, seed=None,):
        self.x = x
        self.y = y
        self.seed = seed

    def get_pose(self):
        return self.x, self.y

    def inventory(self):
        return self.seed

    def set_seed(self, seed):
        self.seed = seed

    def get_seed(self):
        return self.seed

# class MenuScreen:
#     def __init__(self, bestScore):
#         self.bestScore = bestScore
#         self.quitButton = Button(0, 0, 100, "Quit")
#
#     def update(self, screen):
#         screen.fill((47, 129, 54))
#         screen.blit(assets.title_font.render("Farmer Simulator", False, (237, 226, 108)), (100, 100))
#         self.quitButton.update()


#Création des cases
list_cases = []
for i in range(20):
    for j in range(12):
        list_cases.append(Case(360+i*30, 120+j*30))

Carotte = Aliments("carotte", assets.carrots_seed1, assets.carrots_seed2, assets.carrots_fertilizer, assets.carrots_fertilizer_ground, assets.carrots_natural, assets.carrots_natural_ground, assets.carrots_bag_natural, assets.carrots_bag_fertilizer)
Corn = Aliments("corn", assets.corn_seed1, assets.corn_seed2, assets.corn_fertilizer, assets.corn_fertilizer_ground, assets.corn_natural, assets.corn_natural_ground, assets.corn_bag_natural, assets.corn_bag_fertilizer)
Potato = Aliments("potato", assets.potato_seed1, assets.potato_seed2, assets.potato_fertilizer, assets.potato_fertilizer_ground, assets.potato_natural, assets.potato_natural_ground, assets.potato_bag_natural, assets.potato_bag_fertilizer)
Tomato = Aliments("tomato", assets.tomato_seed1, assets.tomato_seed2, assets.tomato_fertilizer, assets.tomato_fertilizer_ground, assets.tomato_natural, assets.tomato_natural_ground, assets.tomato_bag_natural, assets.tomato_bag_fertilizer)
Turnip = Aliments("turnip", assets.turnip_seed1, assets.turnip_seed2, assets.turnip_fertilizer, assets.turnip_fertilizer_ground, assets.turnip_natural, assets.turnip_natural_ground, assets.turnip_bag_natural, assets.turnip_bag_fertilizer)
