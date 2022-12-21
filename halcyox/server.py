from halcyox.classes.character import Character
from .functions import nlp, audio, db, anim
# import ast
# from classes import character, context

class Params:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def restart():
    db.clear()

def initialize():
    db.initialize()


def create_character(characterName, characterDescription):

    params = Params()

    params.characterName = characterName
    params.characterDescription = characterDescription


    characterSchema = { # Create character schema
        "characterName": params.characterName,
        "characterDescription": params.characterDescription,
#         "parameterValues": params.parameterValues
                    }

    db.save_character_schema(characterSchema) # Save character schema in DB

    responseDict = characterSchema # Format response to schema
#     response.data = {
#         "characterID": characterSchema["characterID"],
#         "characterDescription": characterSchema["characterDescription"],
#         "parameterValues": characterSchema["parameterValues"]
#                     }

    return responseDict



# def create_session(sessionName, sessionDescription, characterIDList):
#
#     params = Params()
#
#     params.sessionName = sessionName
#     params.sessionDescription = sessionDescription
#     params.characterIDList = characterIDList
#
#     # Create session data
# #     characterDescriptions = [dict(db.fetch_character_schema(characterID))["characterDescription"] for characterID in params.characterIDList]
#     characterDescriptions = [db.fetch_character_schema(characterID)["characterDescription"] for characterID in params.characterIDList]
#     for characterID in params.characterIDList:
#         print(characterID)
#         print(db.fetch_character_schema(characterID))
#     sessionData = {
#         "sessionName": params.sessionName,
#         "sessionDescription": params.sessionDescription,
#         "characterIDList": params.characterIDList,
#         "initialHistory": params.sessionDescription + " " + " ".join(characterDescriptions)
#                     }
#
#     db.save_session_data(sessionData) # Save character schema in DB
#
#     responseDict = sessionData # Format response
#
#     return responseDict

def get_history(sessionID):
    return db.fetch_session_data(sessionID)["history"]