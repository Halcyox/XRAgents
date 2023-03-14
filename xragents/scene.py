from __future__ import annotations

from dataclasses import dataclass
import time
import enum
import logging
import sys

from contextlib import contextmanager
import os
from typing import Optional, Any # This is support for type hints
from log_calls import log_calls # For logging errors and stuff

from .types import Character
from . import nlp, audio, anim

@dataclass
class Scene:
    id: int
    name: str
    description: str # conversation description
    characters: list[Character]
    text_only: bool
    history: str = ""

    def prompt_for_gpt3(self) -> str:
        """Return the entire prompt to GPT3."""
        char_descs = '\n'.join(c.desc for c in self.characters)
        return f"{char_descs}\n{self.history}"

    def animate(self, character, charLine: str):
        """Used to animate a specific character based on the text input
        onto a specific animation node's audio stream listener."""
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

    def report_histfrag(self, histfrag):
        """Add the user's input (as a ListenRecord) to the history."""
        self.history += '\n'+histfrag
        logging.info(f"fresh histfrag: {histfrag}")

    def user_provided_input(self, said_what):
        """Add the user's input (as a ListenRecord) to the history."""
        self.report_histfrag(f"You: {said_what}")

    def make_speak(self, character, primitivePath=None) -> str:
        """Speak, from a character's perspective."""
        char_descs = '\n'.join(c.desc for c in self.characters) # Get all character descriptions
        prompt = f"{self.description}\n{char_descs}{self.history}" # Generate prompt
        logging.error(f"{prompt}")
        prevlen = len(prompt) # Get length of prompt
        if len(prompt)/4 > (2048-800):
            print(f"Prompt too long ({len(prompt)} chars), autosummarizing!\n{prompt}")
            prompt = nlp.summarize(prompt)
            self.history = prompt # Update history, so we don't have to summarize again
            compression_ratio = 0
            lp = len(prompt)
            if lp != 0:
                compression_ratio = prevlen/lp
            logging.info(f"Continuing with:\n{prompt}\nnew ratio: ({compression_ratio}).")
        textResponse = self._model_does_reply_thingy(prompt, character) # Generate response
        #responseEmotion = nlp.get_emotion(textResponse)
        # print(f"textResponse: {textResponse}", file=sys.stderr)
        #print(f"updatedHistory: {updatedHistory}", file=sys.stderr)
        
        self.report_histfrag(f"{character.name}: {textResponse}")
        #
        # print("#################")

        # print(f"history rn: {self.history}", file=sys.stderr)

        # print("#################")

        if not self.text_only:
            wavPath = audio.generate_wav(textResponse, "en-US-TonyNeural") # Generate wav for animation
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
        #     responsePrompt = f"""
        #     {sessionData[sessionDescription]}
        #     {characterDescription}
        #     You: {promptText}
        #     {characterName}:"""

        response = None
        promptToChar = f"{promptText}\n{character.name}:"

        while response is None or response == "":
            logging.warn(f"asking the ai! {promptToChar}")
            response = nlp.get_completion(promptToChar)
            time.sleep(1)  # delay by one second

        logging.info(f"responded with (final): {response}")
        
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
            f.write(promptToChar)

        return response

    def __str__(self):
        return repr(self)


@contextmanager
def make_scene(id, name, description, characters, text_only):
    """Ensures a scene's save history is always saved!"""
    # resource = Scene(*args, **kwds)
    resource = Scene(id,name,description,characters, text_only)
    try:
        yield resource
    finally:
        # ALWAYS save the history, no matter what.
        resource.save_history()