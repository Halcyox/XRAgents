from dataclasses import dataclass
import enum
from halcyox.functions import nlp, audio, db, anim
from .session import Session
from typing import Optional

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

    def animate(self, action: str, session: Session, primitivePath: str):
        """Used to animate a specific character based on the text input onto a specific animation node's audio stream listener"""
        # Fetch session data from DB
        sessionData = db.fetch_session_data(session)

        # Generate response
        CharacterName = db.fetch_character_schema(self.id)["characterName"]
        # print(sessionData)
        updatedHistory = sessionData["history"]+f"\n{CharacterName}:{action}\n"
        responseEmotion = nlp.get_emotion(action)
        # Update history
        db.update_session_data(session, updatedHistory)
        # Generate wav, selecting wav file
        wavPath = audio.generate_wav(action, responseEmotion, lang="en-US", outputPath="/scripts/ai/ai_")

        # Execute animation
        anim.animate(wavPath, primitivePath)

        # audio.cleanup(wavPath, outputPath)

        # Format response
        responseData = {"responseText": action}

Avatar = Character("Avatar",
                   1,
                   desc="Avatar is a wise philosopher who understands the world in complex yet beautiful, meta-cognitive and cross-paradigmatic ways. He speaks with the eloquence of a great writer, weaving connections through networks of intricate ideas.",
                   wiki_link="https://en.wikipedia.org/wiki/Avatar",
                   primitivePath="/World/audio2face/PlayerStreaming",
                   )

print(Avatar)