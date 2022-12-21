from dataclasses import dataclass
from .character import Character
from ..functions import nlp, audio, anim

@dataclass
class Session():
    """This represents a session. We can have multiple sessions in a scene.
    Each session has an id, name, description, and a list of characters involved."""
    id : int
    name : str
    desc : str
    characters: list[Character]
    history: str

    def get_response(self, character: Character, prompt: str, primitivePath) -> str:
        """Tell a character something and speak its response to primitivePath, returning what we spoke as text"""

        textResponse, updatedHistory = self._model_does_reply_thingy(prompt, character) # Generate response
        responseEmotion = nlp.get_emotion(textResponse)
        self.history += textResponse # ?
        #db.update_session_data(params.sessionID, updatedHistory) # Update history

        wavPath = audio.generate_wav(textResponse, "en-US-TonyNeural", responseEmotion) # Generate wav

        # Execute animation
        anim.animate(wavPath, primitivePath)

        # audio.cleanup(wavPath, outputPath)

        return textResponse

    def _model_does_reply_thingy(self, promptText:str, character: Character):
        # format users input into the narrative metaformat
        narrative_next = f"\nYou: {promptText}\n{character.name}:"
        responsePrompt = self.history + narrative_next
        #     responsePrompt = f"""
        #     {sessionData[sessionDescription]}
        #     {characterDescription}
        #     You: {promptText}
        #     {characterName}:"""
        response = nlp.get_completion(self.desc + responsePrompt)
        print(response + " The model does a reply thingy")

        #     print("DEBUG PROMPT: ", examplePrompt + responsePrompt)
        #     print("\n\n")
        #     print("DEBUG RESPONSE: ", response)

        #     responseEmotion = get_completion(f"""
        #     Sentence:
        #     Emotion:
        #     ###
        #     Sentence:
        #     Emotion:
        #     ###
        #     """)
        updatedHistory = responsePrompt + response
        return response, updatedHistory

    def __str__(self):
        return repr(self)