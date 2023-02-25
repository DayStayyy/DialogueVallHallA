import glob
import os
import time
from Dialogue import Dialogue
from PIL import Image, ImageDraw, ImageFont
import cv2


def write_text(text, x, y, pathFont, sizeFont=None):
    if sizeFont : 
        font = ImageFont.truetype(pathFont, sizeFont)
    else:
        font = ImageFont.truetype(pathFont)
    I1.text((x, y), text, font=font)

def writeLetterByLetter(text, x, y, pathFont, timeToDisplay, background, sizeFont=None, indexOfImage=0):
    timeToDisplay = timeToDisplay/len(text)
    if indexOfImage == 0:
        background.save(f'Results/{0}.png')
    for letter in text:
        write_text(letter, x, y, pathFont, sizeFont)
        x += 5
        background.save(f'Results/{indexOfImage+1}.png')
        indexOfImage += 1

def imagesToVideo(pathImages, pathVideo, fps):
    img_array = []
    for filename in sorted(glob.glob(pathImages), key=os.path.getmtime):
        print(filename)
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    out = cv2.VideoWriter(pathVideo,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in img_array :
        out.write(i)
    out.release()

indexOfImage = 0
xFont = 100
yFont = 200
font = ImageFont.truetype('Fonts/va-11-hall-a-6px-non-mono.ttf')
DIALOGUES_PATH = './Dialogues'
ASSETS_PATH = './Assets'
with open(os.path.join(DIALOGUES_PATH, 'test.csv'), 'r', encoding='utf-8') as f:
    all = f.read()

dial = Dialogue(all)
dialIter = iter(dial)
background = Image.open(os.path.join(ASSETS_PATH,dial.backgroundImage+'.png'))
I1 = ImageDraw.Draw(background)

for ligne in dialIter :
    writeLetterByLetter(ligne.text, xFont, yFont, 'Fonts/va-11-hall-a-6px-non-mono.ttf', ligne.timeToDisplay, background, 6,indexOfImage)
    # use imagesToVideo to create a vide
    imagesToVideo('Results/*.png', 'Results/Video.mp4', 10)