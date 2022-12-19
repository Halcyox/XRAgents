import os
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
import time
from pathlib import Path

import speech_recognition as sr
import pyttsx3
import time
import os

def generate_wav(text, speaker, style,lang=None,outputPath=None):
    """Generates a wav file from text using the Azure Cognitive Services Speech SDK."""
    if outputPath is None:
        outputPath = "/recording/ai/ai_"
    speech_config = speechsdk.SpeechConfig(subscription="bfc08e214f6c48cebcde668a433196d3", region="eastus")
    # audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    wavPath = outputPath + str(time.time()) + ".wav" # the path of the current audio file

    audio_config = speechsdk.audio.AudioOutputConfig(filename= "." + wavPath)

    # Set either the `SpeechSynthesisVoiceName` or `SpeechSynthesisLanguage`.
    speech_config.speech_synthesis_language = "en-US"
    speech_config.speech_synthesis_voice_name = speaker

    # Creates a speech synthesizer.
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    synthesizer.speak_text(text)

    return wavPath

def cleanup(wavPath, outputPath):
    """Deletes the temporary files in the wavPath and outputPath directories."""
    print("Cleaning up temporary files...")
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
        audio += AudioSegment.from_file(paths[i])

    if outputPath is None: # default output path
        outputPath = "recording/output/output_" + str(time.time()) + ".wav"
    audio.export(outputPath, format="wav")

    print("Concatenated audio files to " + outputPath)
    return audio

r = sr.Recognizer()
source = sr.Microphone()
with source as source2:
    print("Please be quiet while we calibrate for ambient noise...", end='')
    # wait for a second to let the recognizer
    # adjust the energy threshold based on
    # the surrounding noise level
    # TODO: this is probably broken, let's figure out why sometime?
    source2.adjust_for_ambient_noise(source2, duration=4)
    print("done!")

# Function to convert text to speech
def speakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def startListen():
    try:
        # this will prolly be busted too TODO
        with source as source2:
            #listens for the user's input
            print("Listening...")
            audio2 = r.listen(source2, timeout=5 )

            # save the audio file to a folder in /recording/ with the name being timestamped
            fileName = "recording/user/" + "Convo_" + str(time.time()) + ".wav"
            with open(fileName, "wb") as f:
                f.write(audio2.get_wav_data())

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()


            return MyText
	except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

	except sr.UnknownValueError:
        print("unknown value error")