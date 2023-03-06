from dataclasses import dataclass
import time
import enum
import logging
import sys

from contextlib import contextmanager
import os
from typing import Optional, Any # This is support for type hints
from log_calls import log_calls # For logging errors and stuff

from . import nlp, audio, anim

@dataclass
class Scene:
    """This represents a scene. We can have multiple scenes in a setting.
    Each scene has an id, name, description, and a list of characters involved."""
    id: int
    name: str
    description: str # conversation description
    characters: list[Any]
    text_only: bool
    history: str = ""

    def __post_init__(self):
        self.history = self.description

    def prompt_for_gpt3(self) -> str:
        """Return the entire prompt to GPT3"""
        char_descs = '\n'.join(c.desc for c in self.characters)
        return f"{char_descs}\n{self.history}"

    def animate(self, character, charLine: str):
        """Used to animate a specific character based on the text input
        onto a specific animation node's audio stream listener"""
        # Generate response
        updatedHistory = self.history+f"\n{character.name}:{charLine}\n"
        responseEmotion = nlp.get_emotion(charLine)
        # Generate wav, selecting wav file
        wavPath = audio.generate_wav(charLine, responseEmotion, lang="en-US", outputPath=f"/scripts/ai/ai_{self.name}")

        # Execute animation
        anim.animate(wavPath, character.primitivePath)

        # audio.cleanup(wavPath, outputPath)

        # Format response
        responseData = {"responseText": charLine}

    def user_provided_input(self, said_what):
        """Add the user's input (as a ListenRecord) to the history"""
        self.history += f"\nYou: {said_what}"


    def make_speak(self, character, primitivePath=None) -> str:
        """Tell a character something, returning what the character spoke as text"""
        char_descs = '\n'.join(c.desc for c in self.characters)
        prompt = f"{char_descs}\n{self.history}"
        #print(prompt)
        prevlen = len(prompt)
        if len(prompt)/4 > (2048-150):
            logging.info(f"Prompt too long ({len(prompt)} chars), autosummarizing!\n{prompt}")
            prompt = nlp.summarize(prompt)
            compression_ratio = 0
            lp = len(prompt)
            if lp != 0:
                compression_ratio = prevlen/lp
            logging.info(f"Continuing with:\n{prompt}\nnew ratio: ({compression_ratio}).")
        else:
            logging.debug("not summarizing!")
        textResponse, updatedHistory = self._model_does_reply_thingy(prompt, character) # Generate response
        #responseEmotion = nlp.get_emotion(textResponse)
        # print(f"textResponse: {textResponse}", file=sys.stderr)
        self.history = updatedHistory
        print(f"history rn: {self.history}", file=sys.stderr)
        #
        # print("#################")

        # print(f"history rn: {self.history}", file=sys.stderr)

        # print("#################")

        if not self.text_only:
            wavPath = audio.generate_wav(textResponse, "en-US-TonyNeural") # Generate wav for animation

        print(f"{character.name}: {textResponse}")
        
        if not self.text_only:
            anim.animate(wavPath, primitivePath) # Execute animation
        # audio.cleanup(wavPath, outputPath) # Erases after speaking

        return textResponse

    def save_history(self, outputDir="recording/script_output/"):
        """Save the conversation to a history file in recording/script_output/{hid}_history.txt"""
        dirname = os.path.dirname(__file__)
        histdir = os.path.join(dirname,f"../{outputDir}")
        if not os.path.exists(histdir):
            os.mkdir(histdir)
        historyPath = os.path.join(histdir, f"{str(self.id) + str(time.time())}_history.txt")
        with open(historyPath, "w") as historyFile:
            historyFile.write(self.history)
            #print(f"just wrote the history:\n{self.history}")

    def _model_does_reply_thingy(self, promptText:str, character):
        """User gives an input to GPT3, and gets a response and the updated history."""
        #print(character)
        #narrative_next = f"\nYou: {promptText}\n{character.name}:"

        #narrative_next = f"\n{promptText}\n{character.name}:"
        newHistoryChunk = f"\n{character.name}:"
        logging.debug(f"responsePrompt: {newHistoryChunk}")
        
        #     responsePrompt = f"""
        #     {sessionData[sessionDescription]}
        #     {characterDescription}
        #     You: {promptText}
        #     {characterName}:"""

        response = None
        
        while response is None or response == "":
            response = nlp.get_completion(promptText+newHistoryChunk)
            time.sleep(1)  # delay by one second

        newHistoryChunk += response
        
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
        with open(f"prompt-{int(time.time())}.txt", "w") as f:
            f.write(newHistoryChunk)

        return response, newHistoryChunk

    def __str__(self):
        return repr(self)


@contextmanager
def make_scene(id, name, description, characters, text_only):
    """makes sure a scene's save history is always saved!"""
    # resource = Scene(*args, **kwds)
    resource = Scene(id,name,description,characters, text_only)
    try:
        yield resource
    finally:
        # ALWAYS save the history, no matter what.
        resource.save_history()