import os
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
import time
from pathlib import Path

def generate_wav(text, speaker, style):

    speech_config = speechsdk.SpeechConfig(subscription="bfc08e214f6c48cebcde668a433196d3", region="eastus")
    # audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    wavPath = "/recording/ai/ai_" + str(time.time()) + ".wav" # the path of the current audio file

    audio_config = speechsdk.audio.AudioOutputConfig(filename= "." + wavPath)

    # Set either the `SpeechSynthesisVoiceName` or `SpeechSynthesisLanguage`.
    speech_config.speech_synthesis_language = "en-US" 
    speech_config.speech_synthesis_voice_name ="en-US-TonyNeural"

    # Creates a speech synthesizer.
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text(text)

    return wavPath

def cleanup(wavPath, outputPath):
    os.remove(wavPath)
    os.remove(outputPath)

# This will concatenate the files together
def concat_audio(aiPath, humanPath, outputPath=None):
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
    return audio


    
    