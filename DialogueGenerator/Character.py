from PIL import Image, ImageDraw
import os
from Variation import Variation
import json 

class Character :
    path_assets = os.path.join('Assets', 'Characters')
    json_path = os.path.join('Data', 'Characters.json')

    def __init__(self, name, firstMainImageName = None):
        self.mainImages = {}
        self.bodyPartVariantesImages = {}
        self.imageConsructor = None
        self.principaleImageName = None
        self.name = name
        self.path_assets = os.path.join(self.path_assets, f'{name}')
        if firstMainImageName:
            self.addMainImage(firstMainImageName)
            self.principaleImageName = firstMainImageName
        else :
            self.addMainImage('main')
            self.principaleImageName = 'main'
        self.getAllVariations()

    def getAllVariations(self):
        with open(self.json_path, 'r') as f:
            data = json.load(f)
        for bodyPart, data in data[self.name].items():
            self.addBodyPartVariantes(bodyPart, bodyPart, data["x"], data["y"])
    
    def addMainImage(self, image_name):
        if image_name not in self.mainImages:
            try : 
                self.mainImages[image_name] = Image.open(os.path.join(self.path_assets, f'{image_name}.png'))
            except FileNotFoundError:
                self.mainImages[image_name] = None
        return self.mainImages[image_name]
    
    def addBodyPartVariantes(self, variantesName, pathToAssets, x, y):
        if variantesName not in self.bodyPartVariantesImages:
            pathToAssets = os.path.join(self.path_assets, pathToAssets)
            self.bodyPartVariantesImages[variantesName] = Variation(variantesName, pathToAssets, x, y)

    def addVariation(self, name, variationName):
        if name in self.bodyPartVariantesImages:
            self.bodyPartVariantesImages[name].addVariation(variationName)
        else:
            raise Exception(f'Variation {name} does not exist')
        
    def createCharacterImage(self, mainImageName, bodyPartVariantes):
        if mainImageName in self.mainImages:
            img = self.mainImages[mainImageName]
            I1 = ImageDraw.Draw(img)
            print(bodyPartVariantes)
            for bodyPart, variation in bodyPartVariantes.items():
                if bodyPart in self.bodyPartVariantesImages:
                    print(variation)
                    if variation not in self.bodyPartVariantesImages[bodyPart].VariationsImages:
                        self.addVariation(bodyPart, variation)
                    img.paste(self.bodyPartVariantesImages[bodyPart].VariationsImages[variation], (self.bodyPartVariantesImages[bodyPart].x, self.bodyPartVariantesImages[bodyPart].y), self.bodyPartVariantesImages[bodyPart].VariationsImages[variation])
            return img
        else:
            raise Exception(f'Main image {mainImageName} does not exist')
