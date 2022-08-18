import os

def generate_mp3(text, speaker, style, outputPath):

    curlRequest = f"""
    curl --location --request POST "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1" \
    --header "Ocp-Apim-Subscription-Key: bfc08e214f6c48cebcde668a433196d3" \
    --header 'Content-Type: application/ssml+xml' \
    --header 'X-Microsoft-OutputFormat: audio-16khz-128kbitrate-mono-mp3' \
    --header 'User-Agent: curl' \
    --data-raw '<speak version='\\''1.0'\\'' xml:lang='\\''en-US'\\''>
        <voice xml:lang='\\''en-US'\\'' xml:style='\\''{style}'\\'' xml:styledegree='\\''2'\\'' name='\\''{speaker}'\\''>
            {text}
        </voice>
    </speak>' > {outputPath}
    """
#     print("curlRequest:\n", curlRequest)

    os.system(curlRequest)
