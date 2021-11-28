import pygame
import yaml

pygame.init()
screen = pygame.display.set_mode((500, 500))

import classes
# import assets
# print(yamlManager.config.yml["screen_settings"]["size_x"])

# print(assets.title_font.render("azazdazdazdaz",False,(0,0,0)).get_width())

# print(pygame.rect.Rect((0,0,30,30)))

# print(assets.button.get_size())

# print(main.randomize_shop)

# print(classes.Button_text(screen.get_width() // 100, screen.get_height() // 50, "Save & Quit", 4, 2, ombre=True,).rect.height)

player_data = classes.player_data()

yaml.