class Result :
    def __init__(self, characterName, text, image, timeToDisplay):
        self.characterName = characterName
        self.text = text
        self.image = image
        self.timeToDisplay = timeToDisplay
    
    def __str__(self):
        return f"CharacterName: {self.characterName} \nText: {self.text} \nTimeToDisplay: {self.timeToDisplay}"