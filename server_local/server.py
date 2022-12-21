from server_local.classes.character import Character
from .functions import nlp, audio1, db, anim
# import ast
# from classes import character, context

class Params:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)    

def restart():
    db.clear()    

def initialize():
    db.initialize()


def animate_character(text,sessionID,characterID, primitivePath):
    """Used to animate a specific character based on the text input onto a specific animation node's audio stream listener"""
    # Fetch session data from DB
    sessionData = db.fetch_session_data(sessionID)
    
    # Generate response
    CharacterName = db.fetch_character_schema(characterID)["characterName"]
    # print(sessionData)
    updatedHistory = sessionData["history"]+f"\n{CharacterName}:{text}\n"
    responseEmotion = nlp.get_emotion(text)
    # Update history
    db.update_session_data(sessionID, updatedHistory)
    # Generate wav, selecting wav file
    wavPath = audio1.generate_wav(text, responseEmotion,lang="en-US",outputPath="/scripts/ai/ai_")
    
    # Execute animation
    anim.animate(wavPath, primitivePath)

    # audio1.cleanup(wavPath, outputPath)

    # Format response
    responseData = {"responseText": text}

def get_response(promptText, sessionID, characterID, primitivePath):
    """Given a input promptText, will give you"""
    params = Params()
    params.promptText = promptText
    params.sessionID = sessionID
    params.characterID = characterID
    
    characterSchema = db.fetch_character_schema(params.characterID) # Fetch character schema from DB
    
    sessionData = db.fetch_session_data(params.sessionID) # Fetch session data from DB

    textResponse, updatedHistory = nlp.generate_response(params.promptText, characterSchema, sessionData) # Generate response
    responseEmotion = nlp.get_emotion(textResponse)
    db.update_session_data(params.sessionID, updatedHistory) # Update history

    wavPath = audio1.generate_wav(textResponse, "en-US-TonyNeural", responseEmotion) # Generate wav
    
    # Execute animation
    anim.animate(wavPath, primitivePath)

    # audio1.cleanup(wavPath, outputPath)

    responseData = {"responseText": textResponse} # Format response
#     response = send_from_directory(directory='data', filename='audio1.mp3')
#     response.data = responseData

    return responseData

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


def create_session(sessionName, sessionDescription, characterIDList):

    params = Params()

    params.sessionName = sessionName
    params.sessionDescription = sessionDescription
    params.characterIDList = characterIDList

    # Create session data
#     characterDescriptions = [dict(db.fetch_character_schema(characterID))["characterDescription"] for characterID in params.characterIDList]
    characterDescriptions = [db.fetch_character_schema(characterID)["characterDescription"] for characterID in params.characterIDList]
    for characterID in params.characterIDList:
        print(characterID)
        print(db.fetch_character_schema(characterID))
    sessionData = {
        "sessionName": params.sessionName,
        "sessionDescription": params.sessionDescription,
        "characterIDList": params.characterIDList,
        "initialHistory": params.sessionDescription + " " + " ".join(characterDescriptions)
                    }
    
    db.save_session_data(sessionData) # Save character schema in DB
    
    responseDict = sessionData # Format response
    
    return responseDict

def get_history(sessionID):
    return db.fetch_session_data(sessionID)["history"]