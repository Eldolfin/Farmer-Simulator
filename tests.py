import pygame

import assets
import yamlManager
import random

pygame.init()
screen = pygame.display.set_mode((yamlManager.config["screen_settings"]["size_x"], yamlManager.config["screen_settings"]["size_y"]))

# import classes
# import assets
# print(yamlManager.config["screen_settings"]["size_x"])

# print(assets.title_font.render("azazdazdazdaz",False,(0,0,0)).get_width())

# print(pygame.rect.Rect((0,0,30,30)))

print(assets.button.get_size())