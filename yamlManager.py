import yaml

with open("config", "r") as file:
    try:
        config = yaml.load(file,Loader=yaml.UnsafeLoader)
    except yaml.YAMLError as exc:
        print(exc)


class PlayerData:
    def __init__(self, best_score):
        self.best_score = best_score

    def serialize(self):
        return yaml.dump(self)

    def deserialize(self, yaml_obj):
        self = yaml.load(yaml_obj)
