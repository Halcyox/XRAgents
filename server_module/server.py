from flask import Flask, send_file, request
from .functions import nlp, audio, db
# import ast
# from classes import character, context

class Params:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)        
app = Flask(__name__)

@app.route('/get-response', methods=["POST"])
def get_response():
    
    # Initialization
    print("\nget-response hit.")
    params = Params()

    # Get input variables
    rf = request.form
    try:
        params.promptText = rf.get("promptText")
        print("\npromptText: ", params.promptText)
    except:
        raise Exception("No promptText inputted.")
    try:
        params.sessionID = rf.get("sessionID")
        print("\nsessionID: ", params.sessionID)
    except:
        raise Exception("No sessionID inputted.")
    try:
        params.characterID = rf.get("characterID")
        print("\ncharacterID: ", params.characterID)
    except:
        raise Exception("No characterID inputted.")
    
    # Fetch character schema from DB
    characterSchema = db.fetch_character_schema(params.characterID)
    
    # Fetch session data from DB
    sessionData = db.fetch_session_data(params.sessionID)
    
    # Generate response
    textResponse, updatedHistory = nlp.generate_response(params.promptText, characterSchema, sessionData)
    responseEmotion = nlp.get_emotion(textResponse)
    # Update history
    db.update_session_data(params.sessionID, updatedHistory)
    
#     # Generate mp3
#     audioResponse = audio.generate_mp3(textResponse, characterSchema["characterVoice"], responseEmotion, "output.mp3")

    # Format response
    responseData = {"responseText": textResponse}
#     response = send_from_directory(directory='data', filename='audio.mp3')
#     response.data = responseData
    
    return responseData

@app.route('/create-character', methods=["POST"])
def create_character():
    
    # Initialization
    print("\ncreate-character endpoint hit.")
    params = Params()

    # Get input variables
    rf = request.form
    try:
        params.characterName = rf.get("characterName")
        print("\ncharacterName: ", params.characterName)
    except:
        raise Exception("No characterName inputted.")
    try:
        params.characterDescription = rf.get("characterDescription")
        print("\ncharacterDescription: ", params.characterDescription)
    except:
        raise Exception("No characterDescription inputted.")
        
      # ommitted for now
#     try:
#         params.parameterValues = rf.get("parameterValues")
#         print("\nparameterValues: ", params.parameterValues)
#     except:
#         raise Exception("No paramterValues inputted.")

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

@app.route('/create-session', methods=["POST"])
def create_session():
    
    # Initialization
    print("\ncreate-session endpoint hit.")
    params = Params()

    # Get input variables
    rf = request.form
    try:
        params.sessionName = rf.get("sessionName")
        print("\nsessionName: ", params.sessionName)
    except:
        raise Exception("No sessionName inputted.")
    try:
        params.sessionDescription = rf.get("sessionDescription")
        print("\nsessionDescription: ", params.sessionDescription)
    except:
        raise Exception("No sessionDescription inputted.")
    try:
#         params.characterIDList = ast.literal_eval(rf.get("characterIDList"))
        params.characterIDList = rf.get("characterIDList")
        print("\ncharacterIDList: ", params.characterIDList)
    except:
        raise Exception("No characterIDList inputted.")

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

# Server
if __name__ == '__main__':
    print("Enter Digital Humans")
    app.run(host='0.0.0.0', threaded=True)