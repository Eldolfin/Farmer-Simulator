import pygame
import assets


class Button:
    def __init__(self, x, y, text, resize_x=1, resize_y=1, ombre=False, on_click=lambda: print("unregistred button click")):
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
            # ca ne marche pas d'itérer comme ca pck on get dejà les event dans le main, et si on get une autre fois on a rien de plus
            # for event in pygame.event.get():
            #     if event.type == pygame.MOUSEBUTTONDOWN:
            #         print("fin du monde")
            #     J'ai trouvé une autre manière de le faire:
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
    def __init__(self, button_list, state, screen, background_color=(-1, -1, -1)):
        self.button_list = button_list
        self.active = state
        self.clicked = False
        self.screen = screen
        for button in button_list:
            button.screen = screen
        #     les éléments sont stockés dans une liste de tuple (surface, pos)
        self.elements = []
        self.background_color = background_color

    def update(self):
        # Si le background n'a pas été défini, on n'affiche pas de background
        if self.background_color != (-1, -1, -1):
            self.screen.fill(self.background_color)
            # On affiche chaque éléments

        for element in self.elements:
            self.screen.blit(element[0], element[1])

        for button in self.button_list:
            button.update(self.clicked)

        self.clicked = False

    def click(self):
        self.clicked = True
        self.update()

    # Methode pour ajouter des éléments à une interface, cet élément est un tuple (surface, pos)
    def addElement(self, element):
        self.elements.append(element)


class Aliments:
    """Carectiristique de chaque aliments"""

    def __init__(self, name, image_empty, image_grown, image_end):
        self.nom = name
        self.image_vide = image_empty
        self.image_pousse = image_grown
        self.image_fin = image_end


class Case:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def get_pose(self):
        return self.x, self.y

# class MenuScreen:
#     def __init__(self, bestScore):
#         self.bestScore = bestScore
#         self.quitButton = Button(0, 0, 100, "Quit")
#
#     def update(self, screen):
#         screen.fill((47, 129, 54))
#         screen.blit(assets.title_font.render("Farmer Simulator", False, (237, 226, 108)), (100, 100))
#         self.quitButton.update()
