import re
from Character import Character
from Result import Result
from utils import splitterCommaNotInQuote

class Dialogue :
    """
    This class is a iterable object 
    This class receive a script, the script is a string of lines with the following format :
    The first line is a header line, the header contains different parameters :
    - MainImage:NameOfCharacter:NameOfMainImage
    - DefaultTimeToDisplay:Time
    - BackgroundImage:NameOfBackgroundImage
    - CharacterPresentAtTheStart:CharacterName1:CharacterName2:CharacterName3

    "CharacterName,Text and optional parameters"
    - The CharacterName is the name of the character
    - The Text is the text to display, is under quotes
    - The TimeToDisplay is the time to display the text, is optional
    - The MainImageName is the name of the main image of the character, is optional
    - The BodyPartVariantesName is the name of the body part variete image of the character, is optional

    The format of optional parameters is :
    - time:TimeToDisplay 
    - main:MainImageName
    - variation:BodyPartName:VarianteName

    The result of the each iteration is a tuple of 4 elements :
    - The first element is the character name
    - The second element is the text to display
    - The third element is a image of the character
    - The fourth element is the time to display the text
    """


    def __init__(self, script):
        self.line_index = 1
        self.characters = {}
        self.defaultTimeToDisplay = 0.5
        self.charactersPresent = []
        self.script = [splitterCommaNotInQuote(line) for line in script.split('\n')]
        self.getScriptParemeters()


    def __iter__(self):
        return self

    def __next__(self):
        try :
            line = self.script[self.line_index]
        except IndexError: 
            raise StopIteration
        CharacterName, Text, *optionalParameters = line
        Text = Text[1:-1] # remove quotes
        if CharacterName not in self.characters:
            self.characters[CharacterName] = Character(CharacterName)
        mainImageName = self.characters[CharacterName].principaleImageName
        bodyPartVariante = {}
        timeToDisplay = self.defaultTimeToDisplay
        for i in optionalParameters :
            if i.startswith('time'):
                timeToDisplay = float(i.split(':')[1])
            elif i.startswith('main'):
                mainImageName = i.split(':')[1]
            elif i.startswith('variation'):
                splitParameters = i.split(':')
                if len(splitParameters) != 3 : continue
                bodyPartVariante[splitParameters[1]] = splitParameters[2]
        finalImage = self.characters[CharacterName].createCharacterImage(mainImageName, bodyPartVariante)
        self.line_index += 1
        return Result(CharacterName, Text, finalImage, timeToDisplay)
    


    def getScriptParemeters(self):
        
        for parameters in self.script[0] :
            if parameters == '' : continue
            elif parameters.startswith('MainImage'):
                splitParameters = parameters.split(':')
                if len(splitParameters) != 3 : continue
                self.characters[splitParameters[1]] = Character(splitParameters[1], splitParameters[2])
            elif parameters.startswith('DefaultTimeToDisplay'):
                splitParameters = parameters.split(':')
                if len(splitParameters) != 2 : continue
                self.defaultTimeToDisplay = float(splitParameters[1])
            elif parameters.startswith('BackgroundImage'):
                splitParameters = parameters.split(':')
                if len(splitParameters) != 2 : continue
                self.backgroundImage = splitParameters[1]
            elif parameters.startswith('CharacterPresentAtTheStart'):
                print(parameters.split(':'))
                for characterName in parameters.split(':')[1:]:
                    if characterName not in self.characters:
                        self.characters[characterName] = Character(characterName)
                    self.charactersPresent.append(self.characters[characterName])
                    

