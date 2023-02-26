from PIL import ImageDraw, ImageFont

def write_text(text, x, y, pathFont, background, sizeFont=None):
    if sizeFont : 
        font = ImageFont.truetype(pathFont, sizeFont)
    else:
        font = ImageFont.truetype(pathFont)
    imageToModify = ImageDraw.Draw(background)
    imageToModify.text((x, y), text, font=font)

def pastImage(image, background, x=0, y=0, resize=1):
    if resize < 0:
        resize = 1/-resize
    resizeImage = image.resize((int(image.width*resize), int(image.height*resize)))
    background.paste(resizeImage, (x, y), resizeImage)