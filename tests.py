import pygame
import yamlManager
import random

pygame.init()
screen = pygame.display.set_mode((yamlManager.config["screen_settings"]["size_x"], yamlManager.config["screen_settings"]["size_y"]))

import classes
import assets
# print(yamlManager.config["screen_settings"]["size_x"])

# print(assets.title_font.render("azazdazdazdaz",False,(0,0,0)).get_width())

print(random.random())