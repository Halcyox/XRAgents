# class to represent a session
class Session():
    def __init__(self,sessionID,sessionName,sessionDescription,characterIDs):
        """
        :param sessionID: the ID of the session
        :type sessionID: int
        :param sessionName: the name of the session
        :type sessionName: str
        :param sessionDescription: the description of the session
        :type sessionDescription: str
        :param characterIDs: the IDs of the characters in the session
        :type characterIDs: str
        """
        self.sessionID = sessionID
        self.sessionName = sessionName
        self.sessionDescription = sessionDescription
        self.characterIDs = characterIDs

    # getters for all the attributes
    def get_sessionID(self):
        return self.sessionID
    def get_sessionName(self):
        return self.sessionName
    def get_sessionDescription(self):
        return self.sessionDescription
    def get_characterIDs(self):
        return self.characterIDs
        
    # need a way to have sess
        