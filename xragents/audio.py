import collections
import os
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
import time
from pathlib import Path
import io
from dataclasses import dataclass

import typing
import speech_recognition as sr
import pyttsx3
import time
import os


def generate_wav(text, speaker, lang=None,outputPath=None):
    print(f"Trying to write to {outputPath}")
    """Generates a wav file from text using the Azure Cognitive Services Speech SDK."""
    if outputPath is None:
        outputPath = "recording/ai/ai_bad_fixme"
    #TODO:API TOKEN
    speech_config = speechsdk.SpeechConfig(subscription="bfc08e214f6c48cebcde668a433196d3", region="eastus")
    # audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    wavname =  f"{int(time.time())}.wav" # the path of the current audio file
    wavPath = f"{outputPath}/{wavname}"#  os.path.join(outputPath,wavname)
    Path(outputPath).mkdir(parents=True, exist_ok=True)
    print(f"{wavPath} is the final destination")
    audio_config = speechsdk.audio.AudioOutputConfig(filename=wavPath)

    # Set either the `SpeechSynthesisVoiceName` or `SpeechSynthesisLanguage`.
    speech_config.speech_synthesis_language = "en-US"
    speech_config.speech_synthesis_voice_name = speaker

    # Creates a speech synthesizer
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text(text)

    return wavPath

def cleanup(wavPath, outputPath):
    """Deletes the temporary files in the wavPath and outputPath directories."""
    for f1,f2 in zip(os.listdir(wavPath), os.listdir(outputPath)):
        os.remove(wavPath + f1)
        os.remove(outputPath + f2)

def concat_audio_double_directory(aiPath, humanPath, outputPath=None):
    """Concatenates the audio files in the aiPath and humanPath directories into a single file."""
    print("Concatenating audio files...")
    aiPaths = [Path(aiPath) / f for f in os.listdir(aiPath) if f.endswith(".wav")]
    humanPaths = [Path(humanPath) / f for f in os.listdir(humanPath) if f.endswith(".wav")]
    # Concatenate the audio files, starting with the human Paths, alternating with the ai paths.
    audio = AudioSegment.empty()
    for i in range(len(humanPaths)-1):
        audio += AudioSegment.from_file(humanPaths[i])
        audio += AudioSegment.from_file(aiPaths[i])

    if outputPath is None: # default output path
        outputPath = "recording/output/output_" + str(time.time()) + ".wav"
    audio.export(outputPath, format="wav")

    print("Concatenated audio files to " + outputPath)
    return audio

def concat_audio_single_directory(path,outputPath=None):
    """Concatenates the audio files in the path directory into a single file."""
    print("Concatenating audio files...")
    paths = [Path(path) / f for f in os.listdir(path) if f.endswith(".wav")]
    # Concatenate the audio files, starting with the human Paths, alternating with the ai paths.
    audio = AudioSegment.empty()
    for i in range(len(paths)):
        time.sleep(0.1)
        audio += AudioSegment.from_file(paths[i])

    if outputPath is None: # default output path
        outputPath = "recording/output/output_" + str(time.time()) + ".wav"
    audio.export(outputPath, format="wav")

    print("Concatenated audio files to " + outputPath)
    return audio


# --------------------------------------------------------
# MICROPHONE INITIALIZATION
# --------------------------------------------------------

r = sr.Recognizer()
raw_source = sr.Microphone()
_calibrated_source = None
def calibrate():
    global _calibrated_source
    if _calibrated_source is None:
        _calibrated_source = raw_source.__enter__()
        print("Please be quiet while I calibrate for ambient noise...",)
        # wait for a second to let the recognizer
        # adjust the energy threshold based on
        # the surrounding noise level
        r.adjust_for_ambient_noise(_calibrated_source, duration=2)
        print("done initializing microphone!")
    return _calibrated_source

@dataclass
class ListenRecord:
    """Transcript of having listened to user input.

    :param file_handle:
      An open file object containing the raw audio data.
    :param path:
      A path where file_handle is stored.
    :param spoken_content:
      The text that was spoken by the user."""
    file_handle: typing.BinaryIO
    path: Path
    spoken_content: str

    def __str__(self):
        return self.spoken_content

def listen_until_quiet_again() -> ListenRecord:
    """This listens to one chunk of user input, returning file handle to """
    try:
        obj = calibrate()
        print("Listening...") # The microphone is now listening for input

        audio2 = r.listen(obj, timeout=5 )

        # save the audio file to a folder in ./recording/ with the name being timestamped
        fileName = "recording/user/" + "Convo_" + str(time.time()) + ".wav"
        f = open(fileName, "wb")
        f.write(audio2.get_wav_data())
        f.seek(0)
        # Using google to recognize audio
        # TODO, replace with whisper
        MyText = r.recognize_google(audio2)
        MyText = MyText.lower()

        return ListenRecord(file_handle=f, spoken_content=MyText, path=Path(fileName))

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        raise e