import os
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
import time
from pathlib import Path

def generate_wav(text, speaker, style, outputPath):
    # curlRequest = f"""curl --location --request POST "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1" --header "Ocp-Apim-Subscription-Key: bfc08e214f6c48cebcde668a433196d3" --header "Content-Type: application/ssml+xml" --header "X-Microsoft-OutputFormat: riff-24khz-16bit-mono-pcm" --header "User-Agent: curl" --data-raw "<speak version='\''1.0'\'' xml:lang='\''en-US'\''><voice xml:lang='\''en-US'\'' name='\''{speaker}'\''>{text}</voice></speak>" > {outputPath}"""
    
    # curlRequest = f"""
    # curl --location --request POST "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1" \
    # --header "Ocp-Apim-Subscription-Key: bfc08e214f6c48cebcde668a433196d3" \
    # --header "Content-Type: application/ssml+xml" \
    # --header "X-Microsoft-OutputFormat: audio-16khz-128kbitrate-mono-mp3" \
    # --header "User-Agent: curl" \
    # --data-raw "<speak version='\\''1.0'\\'' xml:lang='\\''en-US'\\''>
    #     <voice xml:lang='\\''en-US'\\'' xml:style='\\''{style}'\\'' xml:styledegree='\\''2'\\'' name='\\''{speaker}'\\''>
    #         {text}
    #     </voice>
    # </speak>" > {outputPath}
    # """
    # print("before curl: " + outputPath)
    # wavPath = "C:/Users/phn431/Desktop/digital-humans-backend/wav"
    # print(wavPath)

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