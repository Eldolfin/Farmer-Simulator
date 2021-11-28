import pygame
import assets
from assets import tomato_bag_fertilizer


class Button:
    def __init__(self, x, y, image, resize_x=1, resize_y=1, on_click=lambda: print("unregistred button click")):
        # on_click est une fonction elle s'execute lorsqu'un click est détecté (regardez les lambdas)
        self.on_click = on_click
        self.screen = None
        self.spritebase = pygame.transform.scale(image, (image.get_width() * resize_x, image.get_height() * resize_y))
        self.darkmask = pygame.mask.from_surface(self.spritebase)
        self.sprite = self.spritebase
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, interface_clicked):
        # Le offset sert à ce que le text recule quand le bouton est cliqué... à voir
        """Verification des valeurs"""
        self.screen.blit(self.sprite, self.rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if interface_clicked:
                self.on_click()
            self.screen.blit(self.darkmask.to_surface(setcolor=(0, 0, 0, 50), unsetcolor=(0, 0, 0, 0)), self.rect)


class Button_text(Button):
    def __init__(self, x, y, text, resize_x=1, resize_y=1, text_resize=1, ombre=False,
                 on_click=lambda: print("unregistred button click")):
        super().__init__(x, y, assets.button, resize_x, resize_y, on_click=on_click)
        self.text = text
        self.ombre = ombre
        self.button_text = assets.button_font.render(self.text, False, (255, 255, 255))
        self.button_text = pygame.transform.scale(self.button_text, (
            self.button_text.get_width() * text_resize, self.button_text.get_height() * text_resize))
        self.button_text_ombre = assets.button_font.render(self.text, False, (0, 0, 0))
        self.button_text_ombre = pygame.transform.scale(self.button_text_ombre, (
            self.button_text_ombre.get_width() * text_resize, self.button_text_ombre.get_height() * text_resize))

    def update(self, interface_clicked):
        super().update(interface_clicked)
        offset = 2
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                offset = 5
        if self.ombre:
            self.screen.blit(self.button_text_ombre, (
                self.rect.x + (self.rect.width - self.button_text.get_width()) // 2 + 5,
                self.rect.y + (self.rect.height - self.button_text.get_height()) // 2 + 5))
        self.screen.blit(self.button_text, (
            self.rect.x + (self.rect.width - self.button_text.get_width()) // 2 + offset,
            self.rect.y + (self.rect.height - self.button_text.get_height()) // 2 + offset))


class Button_aliment(Button):
    def __init__(self, x, y, aliment, resize_x=1, resize_y=1):
        self.aliment = aliment
        self.interface = None
        lam = lambda: (self.interface.selected_case.set_aliment(self.aliment)) if (
            not self.interface.selected_case is None) else None
        super().__init__(x, y, aliment.ui_element[0], resize_x, resize_y, lam)


class Button_counter(Button):
    def __init__(self, x, y, image, count, resize_x=1, resize_y=1, on_click=lambda: print("unregistred button click")):
        super().__init__(x, y, image, resize_x, resize_y, lambda: on_click if self.count > 0 else None)
        self.count = count


class Interface:
    def __init__(self, button_list, flag, state, screen, background_color=(-1, -1, -1), scale=1):
        self.button_list = button_list
        self.flag = flag
        self.active = state
        self.clicked = False
        self.screen = screen
        #     les éléments sont stockés dans une liste de tuple (surface, pos)
        self.elements = []
        self.background_color = background_color
        self.scale = scale
        self.init_buttons()

    def update(self):
        # Si le background n'a pas été défini, on n'affiche pas de background
        if self.background_color != (-1, -1, -1):
            self.screen.fill(self.background_color)

        # On affiche chaque éléments qui ne sont pas des cases
        for element in self.elements:
            if not isinstance(element, Case):
                self.screen.blit(element[0], element[1])

        for button in self.button_list:
            button.update(self.clicked)

        self.clicked = False

    def click(self):
        self.clicked = True
        self.update()

    # Methode pour ajouter des éléments à une interface, cet élément est un tuple (surface, pos)
    def add_element(self, element):
        self.elements.append(element)

    def init_buttons(self):
        for button in self.button_list:
            button.screen = self.screen
            if isinstance(button, Button_aliment):
                button.interface = self

    def set_buttons(self, buttons):
        self.buttons = buttons
        self.init_buttons()


class main_interface(Interface):
    def __init__(self, button_list, flag, state, screen, background_color=(-1, -1, -1), scale=1):
        super().__init__(button_list, flag, state, screen, background_color, scale)
        self.case_grid = pygame.surface.Surface((600, 420))
        self.case_grid.set_colorkey((0, 0, 0))
        self.update_grid()
        self.selected_case = None

    def update(self):
        if self.clicked:
            for case in list_cases:
                if case.rect.collidepoint((pygame.mouse.get_pos()[0] - 360, pygame.mouse.get_pos()[1] - 120)):
                    self.selected_case = case
        super().update()
        self.screen.blit(self.case_grid, (360, 120))
        if not self.selected_case is None:
            selection_carre = pygame.Surface((self.selected_case.rect.width, self.selected_case.rect.height))
            selection_carre.set_alpha(50)
            selection_carre.fill((255, 255, 255))
            self.screen.blit(selection_carre, (self.selected_case.rect.x + 360, self.selected_case.rect.y + 120))

    def update_grid(self):
        self.case_grid.fill((0, 0, 0))
        for element in self.elements:
            if isinstance(element, Case):
                self.case_grid.blit(element.get_state(), element.get_pose())


class Aliments:
    """Carectèristique de chaque aliments"""

    def __init__(self, name, growth_natural, growth_fertilizer, ui_element, growth_cycle, price):
        self.name = name
        self.growth_natural = growth_natural
        self.growth_fertilizer = growth_fertilizer
        self.ui_element = ui_element
        self.growth_cycle = growth_cycle
        self.price = price

    def Get_price(self):
        return self.price


Carotte = Aliments("carotte",
                   [assets.carrots_seed1, assets.carrots_seed2, assets.carrots_natural_ground],
                   [assets.carrots_seed1, assets.carrots_seed2, assets.carrots_fertilizer_ground],
                   [assets.carrots_bag_natural, assets.carrots_bag_fertilizer, assets.carrots_natural,
                    assets.carrots_fertilizer], 10, 5)

Potato = Aliments("potato",
                  [assets.potato_seed1, assets.potato_seed2, assets.potato_natural_ground],
                  [assets.potato_seed1, assets.potato_seed2, assets.potato_fertilizer_ground],
                  [assets.potato_bag_natural, assets.potato_bag_fertilizer, assets.potato_natural,
                   assets.potato_fertilizer], 5, 2)

Corn = Aliments("corn",
                [assets.corn_seed1, assets.corn_seed2, assets.corn_natural_ground],
                [assets.corn_seed1, assets.corn_seed2, assets.corn_fertilizer_ground],
                [assets.corn_bag_natural, assets.corn_bag_fertilizer, assets.corn_natural,
                 assets.corn_fertilizer], 20, 12)

Tomato = Aliments("tomato",
                  [assets.tomato_seed1, assets.tomato_seed2, assets.tomato_natural_ground],
                  [assets.tomato_seed1, assets.tomato_seed2, assets.tomato_fertilizer_ground],
                  [assets.tomato_bag_natural, tomato_bag_fertilizer, assets.tomato_natural,
                   assets.tomato_fertilizer], 40, 25)

Turnip = Aliments("turnip",
                  [assets.turnip_seed1, assets.turnip_seed2, assets.turnip_natural_ground],
                  [assets.turnip_seed1, assets.turnip_seed2, assets.turnip_fertilizer_ground],
                  [assets.turnip_bag_natural, assets.turnip_bag_fertilizer, assets.turnip_natural,
                   assets.turnip_fertilizer], 60, 60)

aliment_list = [Potato, Carotte, Corn, Tomato, Turnip]


class Case:
    def __init__(self, x, y):
        # self.x = x
        # self.y = y
        # coordonées remplacées par un rect
        self.rect = pygame.rect.Rect((x, y, 30, 30))
        self.aliment = None
        self.growth = 0
        self.fertilized = 0
        self.tick = 0

    def get_pose(self):
        return self.rect.x, self.rect.y

    def inventory(self):
        return self.aliment

    def set_aliment(self, aliments):
        self.aliment = aliments

    def get_aliment(self):
        return self.aliment

    def get_state(self):
        if self.aliment is None:
            return assets.trou
        else:
            if self.fertilized > 0:
                return self.aliment.growth_fertilizer[self.growth]
            else:
                return self.aliment.growth_natural[self.growth]

    def dotick(self):
        if self.aliment is not None:
            self.tick += 1
            self.fertilized -= 1
            if self.tick % self.aliment.growth_cycle == 0:
                if self.growth == 2 :
                    #playerInventory.elements[self.aliment.name] += 1
                    playerInventory.add_money(self.aliment.price)
                    self.aliment = None
                    self.growth = 0
                #     METTRE ICI DANS L'INVENTAIRE
                else:
                    self.growth += 1

    def set_fertilizer(self, number):
        self.fertilized = number


class Inventory:
    def __init__(self):
        self.elements = {Carotte.name: 0, Tomato.name: 0, Corn.name: 0, Turnip.name: 0, Potato.name: 0,
                         "carrot seeds": 0, "tomato seeds": 0, "corn seeds": 0, "turnip seeds": 0, "potato seeds": 0,
                         "fertilizer": 0, "money": 0}

    def add_element(self, element):
        self.elements[element] += 1

    def try_pay(self, price):
        if self.elements["money"] >= price:
            self.elements["money"] -= price
            return True
        else:
            return False

    def try_sell(self, element, amount):
        if self.elements[element] >= amount:
            self.elements[element] -= amount
            return True
        else:
            return False

    def add_money(self, somme):
        self.elements["money"] += somme

    # Création des cases


# list_cases = [[classes.Case(360+x*30, 120+y*30) for x in range(20)] for y in range(12)]
list_cases = []
for i in range(20):
    for j in range(14):
        list_cases.append(
            Case(i * 30, j * 30))


playerInventory = Inventory()

