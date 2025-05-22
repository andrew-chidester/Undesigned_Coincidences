import torch
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import re

# I'm using this to try and get verse references (doesn't actually work yet)
verseDict = {}


def getSentences(filename):
    # Hold all the sentences (in case the file doesn't open)
    sentences = []
    
    # Open the file
    with open(filename, 'r', encoding='utf-8') as file:
        
        # Read in the entire text
        entireText = file.read()

        # This part is for cleaning the GA text

        # The double newline is how each header starts
        splitText = entireText.split('\n\n')

        cleanText = ""
        
        # So for each section under the header
        for chunk in splitText:
            # Each header ends with a parenthesis and a newline, so if there isn't that, then its the end of the document and should be ignored
            if(len(chunk.split(')\n')) > 1):
                # Start after the header
                cleanChunk = chunk.split(')\n')[1]
                
                # Remove verse references (will be removed once the verse reference part works)
                cleanChunk = re.sub(r'\d+', '', cleanChunk)
                
                # This removes special spaces that are after the verse references
                cleanChunk = cleanChunk.replace('\xa0', '')
                
                # The special Windows quotes would be fine, but they make it hard to use regex
                # So I just replaced them with the standard quotation marks
                cleanChunk = cleanChunk.replace('\u201c', '"')
                cleanChunk = cleanChunk.replace('\u201d', '"')
                cleanChunk = cleanChunk.replace('\u2019', '\'')
                cleanChunk = cleanChunk.replace('\u2018', '\'')
                
                # Remove the newlines
                cleanChunk = cleanChunk.replace('\n', ' ')
                # And finally, this section can be concatenated to the clean text
                cleanText += cleanChunk
        
        # With the clean text, it is now split into sentences
        index = 0
        chapter = 1
        verse = 0        
        
        # Loop through the clean text, removing each sentence
        # This does work as a one line regex function, but I changed it to this to try and get verse references
        while(len(cleanText) > index):
            # Find the next sentence ending (including ending quotation marks as part of the sentence)
            match = re.search(r'[.!?]((\' ")|\'|")?', cleanText)
            if match:
                # Get the next sentence from the text
                sentence = cleanText[:match.end()]
                
                # # Try to get verse references (doesn't work yet, so I commented it out)
                # # I didn't think about not every verse is at the start of a sentence
                # num = re.search(r'\d+', sentence)
                # if num:
                #     if (verse + 1) == num.group():
                #         verse = num.group()
                #     else:
                #         verse = 0
                #         chapter += 1
                #     sentence = sentence[num.end():]
                # verseDict[sentence] = f"{chapter}:{verse}"
                

                # Add the sentence to the vector
                sentences.append(sentence)
                # Remove the sentence from the text
                index = match.end()
                cleanText = cleanText[index:]
                
                # Loop through each sentence

            # If a sentence ending can't be found, then break out of the loop
            else:
                break
        # After looping through the text, make sure the last part is added to the sentences (this is probably empty, which is removed later, but in case something went wrong)
        sentences.append(cleanText[index:])

        # Now with all the sentences, I wanted to clean them up a little since there were some that were broken (and this was easier than finding what's wrong with my code)
        for i in range(len(sentences)):
            # Remove any spaces at the front of the sentences
            sentences[i] = sentences[i].lstrip()
            # Some 'sentences' were just a double quote, so those are moved back to the previous sentence
            if(sentences[i] == '"'):
                print(i)
                sentences[i-1] += ' "'
        # Remove all the single quote 'sentences'
        while '"' in sentences:
            sentences.remove('"')

        # If the last 'sentence' is just blank, then remove it
        if sentences[-1] == "":
            sentences = sentences[0:-1]
        
    # And now, the text has been cleaned to just sentences
    
    #print(sentences)
    return sentences

def main():
    # I put this since the first time you run it, it needs to load the model which takes a while, so I know it's actually started
    print("Starting Code")
    
    # Get the sentences from the texts (only tested for Matthew and Mark, but it should work for all of GA)
    sentences = getSentences("Matthew(NRSV).txt") # Switch this to point to the text you want
    
    # Load the model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # Create the embeddings (this is running the SBERT model)
    embeddings = model.encode(sentences)
    
    # I then store the text and embeddings to a json so they can be used later
    data = {
        "sentences" : sentences,
        "embeddings" : embeddings.tolist(),
        "verseDict" : verseDict
    }
    # Change this to be what you actually want to save it as (for example, if it's for Mark, name it that so they don't overwrite eachother)
    with open("FirstEmbedding.json", 'w') as jsonFile:
        json.dump(data, jsonFile)
    
    # The embeddings have been made and stored
    print("Finished Code")

    

if __name__ == "__main__":
    main()