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

    # need a way to have sess
        