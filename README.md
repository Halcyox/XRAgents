# Metahumans Halcyox

## Todos
* emotional speech
Optimization
* change azure to streaming for lower latency

## LOCAL

1. mic input
2. speech to text
3. generate response
4. get .wav
5. run sh script

## SERVER

### Directory Structure
```
metahumans
├── LICENSE
├── README.md
├── server.py
├── digital-humans.db
├── functions
│   ├── audio.py
│   ├── db.py
│   └── nlp.py
|   └── anim.py
└── classes (unused)
```

### Example Post Requests

##### Create Chararacter
http://digital-humans.loca.lt/create-character
characterName: Tom
characterDescription: Tom is a wise old man who genuinely cares about people.

##### Create Session
http://digital-humans.loca.lt/create-session
sessionName: newSession
sessionDescription: The following is a conversation between you and Tom in the bookstore.
characterIDList: 1

##### Get Response
http://digital-humans.loca.lt/get-response
promptText: What should I do to heal from heartbreak?
sessionID: 1
characterID: 1


### Debug (ignore)
```
curl --location --request POST "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1" --header "Ocp-Apim-Subscription-Key: bfc08e214f6c48cebcde668a433196d3" --header "Content-Type: application/ssml+xml" --header "X-Microsoft-OutputFormat: audio-16khz-128kbitrate-mono-mp3" --header "User-Agent: curl" --data-raw "<speak version='\''1.0'\'' xml:lang='\''en-US'\''><voice xml:lang='\''en-US'\'' xml:styledegree='\''2'\'' name='\''en-US-JennyNeural'\''>I hate you! You ruined my life!</voice></speak>" > C:\Users\phn431\Desktop\digital-humans-backend\wav\test.mp3
```

```
curl --location --request POST "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken" --header "Ocp-Apim-Subscription-Key: bfc08e214f6c48cebcde668a433196d3" --header 'Content-Type: application/ssml+xml' --header 'X-Microsoft-OutputFormat: audio-16khz-128kbitrate-mono-mp3' --header 'User-Agent: curl' --data-raw '<speak version='\''1.0'\'' xml:lang='\''en-US'\''><voice xml:lang='\''en-US'\'' xml:style='\''angry'\'' xml:styledegree='\''2'\'' name='\''en-US-JennyNeural'\''>This is a test</voice></speak>' > C:\Users\phn431\Desktop\digital-humans-backend\wav\test.wav
```

```
curl --location --request POST "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1" --header "Ocp-Apim-Subscription-Key: bfc08e214f6c48cebcde668a433196d3" --header 'Content-Type: application/ssml+xml' --header 'X-Microsoft-OutputFormat: audio-16khz-128kbitrate-mono-mp3' --header 'User-Agent: curl' --data-raw '<speak version='\''1.0'\'' xml:lang='\''en-US'\''><voice xml:lang='\''en-US'\'' xml:gender='\''Female'\'' name='\''en-US-JennyNeural'\''>my voice is my passport verify me</voice></speak>' > C:\Users\phn431\Desktop\digital-humans-backend\wav\test.wav
```

```
curl --location --request POST "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1" --header "Ocp-Apim-Subscription-Key: bfc08e214f6c48cebcde668a433196d3" --header "Content-Type: application/ssml+xml" --header "X-Microsoft-OutputFormat: audio-16khz-128kbitrate-mono-mp3" --header "User-Agent: curl" --data-raw "<speak version='\''1.0'\'' xml:lang='\''en-US'\''><voice xml:lang='\''en-US'\'' xml:gender='\''Female'\'' name='\''en-US-JennyNeural'\''>my voice is my passport verify me</voice></speak>" > output.mp3
```

```
key="YourSubscriptionKey"
region="YourServiceRegion"

curl "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1" `
--header "Ocp-Apim-Subscription-Key: bfc08e214f6c48cebcde668a433196d3" `
--header 'Content-Type: application/ssml+xml' `
--header 'X-Microsoft-OutputFormat: audio-16khz-128kbitrate-mono-mp3' `
--header 'User-Agent: curl' `
--data-raw '<speak version='\''1.0'\'' xml:lang='\''en-US'\''>
    <voice xml:lang='\''en-US'\'' xml:gender='\''Female'\'' name='\''en-US-JennyNeural'\''>
        my voice is my passport verify me
    </voice>
</speak>' > output.mp3
```