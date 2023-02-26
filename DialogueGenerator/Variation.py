from PIL import Image
import os

class Variation :
    def __init__(self, name , pathToAssets, x, y):
        self.name = name
        self.VariationsImages = {}
        self.pathToAssets = pathToAssets
        self.x = x
        self.y = y

    def addVariation(self, name):
        try : 
            self.VariationsImages[name] = Image.open(os.path.join(self.pathToAssets, f'{name}.png'))
        except FileNotFoundError:
            raise Exception(f'Variation {name} does not exist')
