from PIL import Image
import os

class Variation :
    def __init__(self, pathToAssets, x, y):
        self.VariationsImages = {}
        self.pathToAssets = pathToAssets
        self.x = x
        self.y = y

    def addVariation(self, name):
        try : 
            self.VariationsImages[name] = Image.open(os.path.join(self.pathToAssets, f'{name}.png'))
        except FileNotFoundError:
            self.VariationsImages[name] = None
