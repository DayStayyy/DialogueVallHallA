from PIL import Image, ImageDraw
import os
from Variation import Variation

class Character :
    path_assets = os.path.join('Assets', 'Characters')
    mainImages = {}
    bodyPartVariantesImages = {}
    imageConsructor = None
    principaleImageName = None
    def __init__(self, name, firstMainImageName = None):
        self.name = name
        self.path_assets = os.path.join(self.path_assets, f'{name}')
        if firstMainImageName:
            self.addMainImage(firstMainImageName)
            self.principaleImageName = firstMainImageName
        else :
            self.addMainImage('main')
            self.principaleImageName = 'main'
         
    
    def addMainImage(self, image_name):
        if image_name not in self.mainImages:
            try : 
                self.mainImages[image_name] = Image.open(os.path.join(self.path_assets, f'{image_name}.png'))
            except FileNotFoundError:
                self.mainImages[image_name] = None
        return self.mainImages[image_name]
    
    def addBodyPartVariantes(self, variantesName, x, y, pathToAssets):
        if variantesName not in self.bodyPartVariantesImages:
            pathToAssets = os.path.join(self.path_assets, pathToAssets)
            self.bodyPartVariantesImages[variantesName] = Variation(variantesName, pathToAssets)

    def addVariation(self, name, variationName):
        if name in self.bodyPartVariantesImages:
            self.bodyPartVariantesImages[name].addVariation(variationName)
        else:
            raise Exception(f'Variation {name} does not exist')
        
    def createCharacterImage(self, mainImageName, bodyPartVariantes):
        if mainImageName in self.mainImages:
            img = self.mainImages[mainImageName]
            I1 = ImageDraw.Draw(img)
            for bodyPart, variation in bodyPartVariantes.items():
                if bodyPart in self.bodyPartVariantesImages:
                    if variation in self.bodyPartVariantesImages[bodyPart].VariationsImages:
                        img.paste(self.bodyPartVariantesImages[bodyPart].VariationsImages[variation], (self.bodyPartVariantesImages[bodyPart].x, self.bodyPartVariantesImages[bodyPart].y), self.bodyPartVariantesImages[bodyPart].VariationsImages[variation])
            return img
        else:
            raise Exception(f'Main image {mainImageName} does not exist')
