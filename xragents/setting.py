from dataclasses import dataclass
import typing
import io

from .types import Character
from . import scene, utils, audio

import ZODB, ZODB.FileStorage  # Database storage of objects

from ZODB.blob import Blob

@dataclass
class DialogRound:
   """Placeholder for more granular information about each dialog round."""
   who_spoke: Character
   what_they_said: str
   mental_state_before_round: typing.Any
   private_information: typing.Any

@dataclass
class DialogHistory:
    """A class for storing a single phrase said by a single agent."""
    dialog_history : str


@dataclass
class SettingDescription:
    """High level description of all of the scenes inside of an individual setting."""

    names: list[str]
    characters: list[Character]
    #descs: dict[typing.Any,typing.Any]

@dataclass
class InfiniteTelevision:
    """
    This file holds functions that allow for the user
    to listen to 'n' number of AIs talk about things.

    The user can also step in and break the fourth
    wall at any time under a chosen character.

    Current limit is 9 supported animation nodes.
    However you can have unlimited text AI talking in a scene.
    """
    characters_: list[Character]
    history: list[DialogHistory]
    setting_description: SettingDescription

    def __init__(self):
        pass

    def n_convo(self, chars: list[Character], setting_description: SettingDescription): # Given a list of characters, have those characters talk to each other under a specific session description.
        pass

    def get_history(self):
        """This will provide the history so far."""
        return self.history


