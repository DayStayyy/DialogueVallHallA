import copy
import glob
import os
import time

import numpy as np
from Dialogue import Dialogue
from PIL import Image, ImageDraw, ImageFont
import cv2

class DialogueCreator:
    DIALOGUES_PATH = './Dialogues'
    ASSETS_PATH = './Assets'

    xFont = 100
    yFont = 230
    font = ImageFont.truetype('Fonts/va-11-hall-a-6px-non-mono.ttf')
    indexOfImage = 0

    def __init__(self, dialogueName):
        with open(os.path.join(self.DIALOGUES_PATH, dialogueName), 'r', encoding='utf-8') as f:
            script = f.read()

        self.dialogueObject = Dialogue(script)
        self.dialogueIterator = iter(self.dialogueObject)
        self.background = Image.open(os.path.join(self.ASSETS_PATH,self.dialogueObject.backgroundImage+'.png'))

    def write_text(self,text, x, y, pathFont, background, sizeFont=None):
        if sizeFont : 
            font = ImageFont.truetype(pathFont, sizeFont)
        else:
            font = ImageFont.truetype(pathFont)
        imageToModify = ImageDraw.Draw(background)
        imageToModify.text((x, y), text, font=font)

    def writeLetterByLetter(self,text, x, y, pathFont, timeToDisplay, background, sizeFont=None):
        timeToDisplay = timeToDisplay/len(text)
        background.save(f'Results/{self.indexOfImage}.png')
        self.indexOfImage += 1
        for letter in text:
            self.write_text(letter, x, y, pathFont, background, sizeFont)
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
            self.writeLetterByLetter(ligne.text, self.xFont, self.yFont, 'Fonts/va-11-hall-a-6px-non-mono.ttf', ligne.timeToDisplay, copy.copy(self.background))
            # use imagesToVideo to create a vide
        self.imagesToVideo('Results/*.png', 'Results/Video.mp4', 10)


if __name__ == '__main__':
    dialogueCreator = DialogueCreator('test.csv')
    dialogueCreator.createVideo()