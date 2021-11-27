import yaml


# Cette partie lis le fichier de configuration config et le mets dans la variable config


with open("config", "r") as file:
    try:
        config = yaml.load(file, Loader=yaml.UnsafeLoader)
        # print(config)
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
