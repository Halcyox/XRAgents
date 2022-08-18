import os
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
import time
from pathlib import Path

def generate_wav(text, speaker, style, outputPath):

    speech_config = speechsdk.SpeechConfig(subscription="bfc08e214f6c48cebcde668a433196d3", region="eastus")
    # audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    audio_config = speechsdk.audio.AudioOutputConfig(filename="./wav/output.wav")

    # Set either the `SpeechSynthesisVoiceName` or `SpeechSynthesisLanguage`.
    speech_config.speech_synthesis_language = "en-US" 
    speech_config.speech_synthesis_voice_name ="en-US-TonyNeural"
    speech_config.speech_synthesis_voice_name

    # Creates a speech synthesizer.
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text(text)

    # AudioSegment.converter = r"C:/Python310/Lib/site-packages/ffmpeg"

    return outputPath

def cleanup(wavPath, outputPath):
    os.remove(wavPath)
    os.remove(outputPath)