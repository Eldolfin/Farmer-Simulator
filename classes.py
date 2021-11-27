import pygame
import assets


class Button:
    def __init__(self, x, y, text, resize_x=1, resize_y=1):
        self.x = x
        self.y = y
        self.sprite_list = [assets.button1, assets.button2]
        self.sprite = self.sprite_list[0]
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.length = self.rect.width
        self.text = text
        self.text_x = self.x + self.length / 2 - (len(text) / 2) * 15
        self.text_y = self.y
        self.clicked = False

    def update(self, screen):
        """Verrificaton des valeurs"""
        button_text = assets.button_font.render(self.text, False, (255, 255, 255))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.sprite = self.sprite_list[1]
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("fin du monde")
        else:
            self.sprite = self.sprite_list[0]

        screen.blit(self.sprite, (self.x, self.y))
        screen.blit(button_text, (self.text_x , self.text_y))


class Interface:
    def __init__(self, button_list, state):
        self.button_list = button_list
        self.active = state


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
