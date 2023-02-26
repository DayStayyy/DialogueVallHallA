import copy
import glob
import json
import os
import time

import numpy as np
from Dialogue import Dialogue
from PIL import Image, ImageDraw, ImageFont
import cv2
from ImagesGenerator import write_text, pastImage

class DialogueCreator:
    DIALOGUES_PATH = './Dialogues'
    ASSETS_PATH = './Assets'
    PATH_TO_JSON = './Data'

    xFont = 100
    yFont = 230
    font = ImageFont.truetype('Fonts/va-11-hall-a-6px-non-mono.ttf')


    def __init__(self, dialogueName, JSONName):
        self.indexOfImage = 0
        with open(os.path.join(self.DIALOGUES_PATH, dialogueName), 'r', encoding='utf-8') as f:
            script = f.read()
    
        self.dialogueObject = Dialogue(script)
        self.dialogueIterator = iter(self.dialogueObject)
        self.background = Image.open(os.path.join(self.ASSETS_PATH,self.dialogueObject.backgroundImage+'.png'))

        with open(os.path.join(self.PATH_TO_JSON, JSONName), 'r', encoding='utf-8') as f:
            self.data = json.load(f)


    def writeLetterByLetter(self,text, x, y, pathFont, timeToDisplay, background, sizeFont=None):
        timeToDisplay = timeToDisplay/len(text)
        background.save(f'Results/{self.indexOfImage}.png')
        self.indexOfImage += 1
        for letter in text:
            write_text(letter, x, y, pathFont, background, sizeFont)
            x += 5
            background.save(f'Results/{self.indexOfImage}.png')
            self.indexOfImage += 1



    def imagesToVideo(self,pathImages, pathVideo, fps):
        img_array = []
        for filename in sorted(glob.glob(pathImages), key=os.path.getmtime):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)
        out = cv2.VideoWriter(pathVideo,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
        for i in img_array :
            out.write(i)
        out.release()

    def createVideo(self):
        for ligne in self.dialogueIterator :
            background = self.UpdateBackgroundWithCharacters(copy.copy(self.background))
            pastImage(ligne.image, background, self.data["Characters"][ligne.characterName]["x"], self.data["Characters"][ligne.characterName]["y"], self.data["Characters"][ligne.characterName]["resize"])
            self.writeLetterByLetter(ligne.text, self.xFont, self.yFont, 'Fonts/va-11-hall-a-6px-non-mono.ttf', ligne.timeToDisplay, background)
            # use imagesToVideo to create a vide
        self.imagesToVideo('Results/*.png', 'Results/Video.mp4', 10)

    def UpdateBackgroundWithCharacters(self, background):
        print(self.dialogueObject.charactersPresent)
        for character in self.dialogueObject.charactersPresent :
            pastImage(character.actualImage, background, self.data["Characters"][character.name]["x"], self.data["Characters"][character.name]["y"], self.data["Characters"][character.name]["resize"])
        return background
    
if __name__ == '__main__':
    dialogueCreator = DialogueCreator('test.csv', 'FirstBackground.json')
    dialogueCreator.createVideo()

    # first = dialogueCreator.dialogueIterator.__next__()
    # resize = 1/-(-2.2)
    # reduce = first.image.resize((int(first.image.width*resize), int(first.image.height*resize)))
    # dialogueCreator.background.paste(reduce, (95, 80), reduce)
    # # dialogueCreator.background.paste(reduce, (480, 80), reduce)


    # second = dialogueCreator.dialogueIterator.__next__()
    # print(second)
    # reduce = second.image.resize((int(second.image.width/2.2), int(second.image.height/2.2)))
    # dialogueCreator.background.paste(reduce, (480, 93), reduce)
    # dialogueCreator.background.show()

