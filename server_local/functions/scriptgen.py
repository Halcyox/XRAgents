import os
import utils
import audio1

# This file holds methods for mass generation of audio files from scripts



# The file importing requires a .txt file with the following format (make sure to have a newline at the end of each line):
# The following is a conversation between two AIs. Blah blah blah <whatever you want here as context>.
# Hal:
# Sophia:

def parseScripts(inputDir=None, outputDir=None):
    if(inputDir is None):
        inputDir = "scripts/input/"
    if (outputDir is None):
        outputDir = "scripts/output/"
    utils.create_directory(inputDir, False) # verify the input directory exists
    utils.create_directory(outputDir, False) # verify the output directory exists
    scriptList = [] # create an empty list to hold the script objects


    for filename in os.listdir(inputDir):
        if filename.endswith(".txt"):
            with open(inputDir+filename) as f: # opens the input file
               content = f.readlines() # reads the input file
        content = [x.strip() for x in content] # strips the input file
        clipLength = len(content) - 1 # how many lines there are in the input file, excludes context

        voiceList = [] # create an empty list to hold the voice objects
        emotionList = [] # create an empty list to hold the emotion objects
        lineList = [] # create an empty list to hold the line objects

        for i in range(clipLength): # for each line in the input file
            print('Starting line [%d/%d] %s' % (i+1,clipLength,filename)) # prints the current line being processed
            actorLine = (content[i]).split(':', 1) # splits the line into the actor and the line
            lineList.append(actorLine[1]) # adds the line to the line list
            emotionList.append()
    

# return an object that holds one script, and the script object contains all the information with the actor, lines, and we return an array of script objects

    # The following is the code for generating the audio file
    # We want to be able to control the speaker and the emotion of the audio file quickly
    wavPath = audio1.generate_wav(textResponse, "en-US-TonyNeural", responseEmotion)





totalVid = len(content) # sets the total length of the video(lines)
for i in range(1, len(content)): # loops through the lines
    
    