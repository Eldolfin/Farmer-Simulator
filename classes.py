import assets

class Button:
    def __init__(self, text, x, y):
        self.x = x;
        self.y = y;
        self.sprite = assets.button;
        self.text = text;
