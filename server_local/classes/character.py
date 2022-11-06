# This is a class for the character object to represent a character
class Character():
    def __init__(self,characterID,characterName,characterDescription,primitivePath,voice):
        """
        :param characterID: the ID of the character
        :type characterID: int
        :param characterName: the name of the character
        :type characterName: str
        :param characterDescription: the description of the character
        :type characterDescription: str
        :param primitivePath: the path to the primitive file
        :type primitivePath: str
        """
        self.characterID = characterID
        self.characterName = characterName
        self.characterDescription = characterDescription
        self.primitivePath = primitivePath
        self.voice = voice

    def __str__(self):
        return str(self.characterID) + " " + self.characterName + " " + self.characterDescription + " " + self.voice + " " + self.primitivePath
   
    def get_voice(self):
        return self.voice

        

