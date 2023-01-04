from dataclasses import dataclass
import time
import enum
import logging
from . import nlp, audio, anim
import os
from typing import Optional # This is support for type hints
from log_calls import log_calls # For logging errors and stuff
#from setting import SettingDescription

@dataclass
class Scene:
    """This represents a scene. We can have multiple scenes in a setting.
    Each scene has an id, name, description, and a list of characters involved."""
    def __init__(self, id: int, name: str, desc: str):
        self.id_ = id
        self.name_ = name
        self.desc_ = desc

    # NOTE: dataclasses solve this constructor. ember knew what they were doing and louis is dumb
    # revisit this and unbreak it

    from contextlib import contextmanager
    @contextmanager
    def make_scene(id, name, desc, description):
        """makes sure a scene's save history is always saved!"""
        # resource = Scene(*args, **kwds)
        resource = Scene(id,name,desc)
        try:
            yield resource
        finally:
            # Code to release resource, e.g.:
            resource.save_history()

    def prompt_for_gpt3(self):
        """Return the entire prompt to GPT3"""
        #return f"{self.scene.descs}{' '.join(c.desc for c in self.scene.characters)}\n{self.history}"

    @log_calls()
    def animate(self, character, charLine: str):
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

    def make_speak(self, character, primitivePath) -> str:
        """Tell a character something and speak its response to primitivePath, returning what we spoke as text"""
        prompt = self.prompt_for_gpt3()
        textResponse, updatedHistory = self._model_does_reply_thingy(prompt, character) # Generate response
        responseEmotion = nlp.get_emotion(textResponse)
        self.description_.append(textResponse)
        print(self.description_)

        wavPath = audio.generate_wav(textResponse, "en-US-TonyNeural", responseEmotion) # Generate wav

        print(f"{character.name}: {textResponse}")
        anim.animate(wavPath, primitivePath) # Execute animation
        # audio.cleanup(wavPath, outputPath) # Erases after speaking

        return textResponse

    def save_history(self, outputDir="recording/script_output/"):
        """Save the conversation to a history file in recording/script_output/{hid}_history.txt"""
        dirname = os.path.dirname(__file__)
        histdir = os.path.join(dirname,f"../{outputDir}")
        if not os.path.exists(histdir):
            os.mkdir(histdir)
        historyPath = os.path.join(histdir, f"{str(self.id_) + str(time.time())}_history.txt")
        with open(historyPath, "w") as historyFile:
            historyFile.write(self.desc_)
            print(self.desc_)

    def _model_does_reply_thingy(self, promptText:str, character):
        """User gives an input to GPT3, and gets a response and the updated history."""
        #print(character)
        narrative_next = f"\nYou: {promptText}\n{character.name}:"
        responsePrompt = self.description_ + narrative_next
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
