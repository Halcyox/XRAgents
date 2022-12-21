from dataclasses import dataclass
from .functions import nlp, audio, anim
from dataclasses import dataclass
import enum
from halcyox.functions import nlp, audio, anim
from typing import Optional
import os
class NeuralTTSSelector(enum.Enum):
    TONY = "en-US-TonyNeural"

@dataclass
class Character():
    """This is a character, we can have multiple characters in a scene.
    Characters have names, id, descriptions, primitive path, and voice from TTS."""
    name: str
    id: int # uuid

    desc: str

    wiki_link: str = ""
    voice: NeuralTTSSelector = NeuralTTSSelector.TONY
    primitivePath: Optional[str] = None

    def __str__(self):
        return repr(self)

Avatar = Character("Avatar",
                   1,
                   desc="Avatar is a wise philosopher who understands the world in complex yet beautiful, meta-cognitive and cross-paradigmatic ways. He speaks with the eloquence of a great writer, weaving connections through networks of intricate ideas.",
                   wiki_link="https://en.wikipedia.org/wiki/Avatar",
                   primitivePath="/World/audio2face/PlayerStreaming",
                   )

@dataclass
class Session():
    """This represents a session. We can have multiple sessions in a scene.
    Each session has an id, name, description, and a list of characters involved."""
    id : int
    name : str
    desc : str
    history: str = ""

    def animate(self, character: Character, charLine: str):
        """Used to animate a specific character based on the text input
        onto a specific animation node's audio stream listener"""
        # Generate response
        updatedHistory = self.history+f"\n{character.name}:{charLine}\n"
        responseEmotion = nlp.get_emotion(charLine)
        # Generate wav, selecting wav file
        wavPath = audio.generate_wav(charLine, responseEmotion, lang="en-US", outputPath="/scripts/ai/ai_")

        # Execute animation
        anim.animate(wavPath, character.primitivePath)

        # audio.cleanup(wavPath, outputPath)

        # Format response
        responseData = {"responseText": charLine}

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

    def save_history(self, outputDir="recording/script_output/"):
        """Save the conversation to a history file in recording/script_output/{hid}_history.txt"""
        dirname = os.path.dirname(__file__)
        historyPath = os.path.join(dirname,f"../../{outputDir}", f"{str(self.id)}_history.txt")
        with open(historyPath, "w") as historyFile:
            historyFile.write(self.history)


    def _model_does_reply_thingy(self, promptText:str, character: Character):
        """User gives an input to GPT3, and gets a response and the updated history."""
        # format users input into the narrative metaformat
        narrative_next = f"\nYou: {promptText}\n{character.name}:"
        responsePrompt = self.history + narrative_next
        #     responsePrompt = f"""
        #     {sessionData[sessionDescription]}
        #     {characterDescription}
        #     You: {promptText}
        #     {characterName}:"""
        response = nlp.get_completion(self.desc + responsePrompt)

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
    