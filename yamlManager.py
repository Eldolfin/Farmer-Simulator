import yaml
from datetime import datetime
import os

# Cette partie lis le fichier de configuration config.yml et le mets dans la variable config.yml


with open("config.yml", "r") as file:
    try:
        config = yaml.load(file, Loader=yaml.UnsafeLoader)
        # print(config.yml)
    except yaml.YAMLError as exc:
        print(exc)


def log_save():
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    config["last_save"] = date
    with open("config.yml", "w") as file:
        yaml.dump(config, file)


def load_PlayerData():
    with open("playerdata.yml", "r") as file:
        try:
            return yaml.load(file, Loader=yaml.Loader)
        except yaml.YAMLError as exc:
            print(exc)


def dump_PlayerData(player_data):
    if os.path.exists("playerdata.yml"):
        os.remove("playerdata.yml")
    with open("playerdata.yml", "w") as file:
        try:
            yaml.dump(player_data, file)
        except yaml.YAMLError as exc:
            print(exc)

# Cette class était une idée d'implementation qui converti les données de la class
# PlayerData en un fichier yaml, les methodes yaml.dump et yaml.load peuvent etre
# très utiles pour stocker toutes les données d'une classe facilement
# class PlayerData:
#     def __init__(self, best_score):
#         self.best_score = best_score
#
#     def serialize(self):
#         return yaml.dump(self)
#
#     def deserialize(self, yaml_obj):
#         self = yaml.load(yaml_obj)
