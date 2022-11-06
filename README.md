# Metahumans Halcyox

# Next time:
* Work on the batch generation of videos for two characters, and see how far you get.
* Also, work on the front end with Alice.

## Priority TODO:
* SSML for voice style modification stuff

~~* Selection backend for voice options~~
* Set up simple server client app to get people to be able to access a server of talking to ai instance
* Screen record video
* Avatar creation/importing
* Record + stream blendshapes

~~* Convert input script batch pipeline to work with our video generation scripts~~
* Make VidGen Server -> rendering server distribute accross mult computers
* Methods to upload videos to youtube -> google api integration

~~* Multi-character (n-entity) scene methods, just give prim paths~~
* Talk to multiple AI simultaneously


## Non-Priority TODO:
* emotional speech
* Optimization
* change azure to streaming for lower latency
* Connect your own camera to the output video with the AI
* Unreal integration

## Web TODO:
* Figure out dependencies, Docker stuff, versions
* How to put on Amplify?
* Should we use EC2 instances or what?
* Website should have registration and billing
* Token system for AI voice credits

## Marketing TODO:
* Affiliate marketing application to get other people to grow our software





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