class CreatePicture :
    
    def __init__(self, path) :
        self.pathToAssets = path


    def insertImage(self, imageToModify,imageToInsert, x, y):
        imageToModify.paste(imageToInsert, (x, y), imageToInsert)
        return imageToModify
