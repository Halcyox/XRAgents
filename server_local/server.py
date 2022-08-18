from .functions import nlp, audio, db, anim
# import ast
# from classes import character, context
primitivePath = "/World/audio2face/PlayerStreaming"
# primitivePath = "/World/LazyGraph/PlayerStreaming"
# outputPath = r"C:/Users/phn431/Desktop/digital-humans-backend/wav/output.wav"
# outputPath = r"C:\Users\Alif Jakir\Documents\GitHub\digital-humans-backend\wav\output.wav"
outputPath = fr"../../wav/output.wav"

class Params:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)    

def restart():
    db.clear()    

def initialize():
    db.initialize()

def get_response(promptText, sessionID, characterID):

    params = Params()

    params.promptText = promptText
    params.sessionID = sessionID
    params.characterID = characterID
    
    # Fetch character schema from DB
    characterSchema = db.fetch_character_schema(params.characterID)
    
    # Fetch session data from DB
    sessionData = db.fetch_session_data(params.sessionID)
    
    # Generate response
    textResponse, updatedHistory = nlp.generate_response(params.promptText, characterSchema, sessionData)
    responseEmotion = nlp.get_emotion(textResponse)
    # Update history
    db.update_session_data(params.sessionID, updatedHistory)
    
    # Generate wav
    wavPath = audio.generate_wav(textResponse, "en-US-TonyNeural", responseEmotion, outputPath)
    
    # Execute animation
    anim.animate(wavPath, primitivePath)

    # audio.cleanup(wavPath, outputPath)

    # Format response
    responseData = {"responseText": textResponse}
#     response = send_from_directory(directory='data', filename='audio.mp3')
#     response.data = responseData
    
    return responseData


def create_character(characterName, characterDescription):

    params = Params()

    params.characterName = characterName
    params.characterDescription = characterDescription
        
    # Create character schema
    characterSchema = {
        "characterName": params.characterName,
        "characterDescription": params.characterDescription,
#         "parameterValues": params.parameterValues
                    }
    
    # Save character schema in DB
    db.save_character_schema(characterSchema)
    
    # Format response
    responseDict = characterSchema
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
    
    # Save character schema in DB
    db.save_session_data(sessionData)
    
    # Format response
    responseDict = sessionData
    
    return responseDict
