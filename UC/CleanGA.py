import re
import json




def getVerses(filename):
    
    verseDict = {}
    # Hold all the verses (in case the file doesn't open)
    verseVect = []
    
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
            # Each header ends with the newline and the first verse number
            if(len(re.split(r'(\n\d)', chunk)) > 1):
                # Start after the header
                cleanChunk = ''.join(re.split(r'(\n\d)', chunk)[1:])
                
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
        
        # With the clean text, it is now split into verses
        index = 0
        chapter = 1
        verse = 1
        
        #print(cleanText)

        # Start after the first verse reference
        match = re.search(r'\d+', cleanText)
        cleanText = cleanText[match.end():]
        

        # Loop through the clean text, finding each verse
        while(len(cleanText) > index):
            # Find the next number, which will be the start of the next verse
            match = re.search(r'\d+', cleanText)
            if match:
                # Get the next verse
                verseText = cleanText[:match.start()]
                
                # Add the verse and its reference
                verseDict[verseText.strip()] = f"{chapter}:{verse}"
                
                #print(f"{chapter}:{verse} - {match.group()}")
                
                # If the next number is the next in order, then it is a verse number
                if (verse + 1) == int(match.group()) or verse == 1:
                    verse += 1
                # Else, it is a chapter number
                elif (chapter + 1) == int(match.group()):
                    verse = 1
                    chapter += 1
                # A couple of verses aren't in NRSV
                else:  
                    verse += 2
                    print(f"{chapter}:{verse-1} - missing?") # If this is printing a lot, something is probably wrong
                    
                # Remove the verse from the text
                index = match.end()
                cleanText = cleanText[index:]
                
                # Loop through each verse

            # If there isn't a next verse
            else:
                break
            
        # After looping through the text, make sure the last verse is added
        verseDict[verseText] = f"{chapter}:{verse}"

        
    # And now, the text has been cleaned to be the verses
    
    #print(verseDict)
    return verseDict


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
                
                # Remove verse references
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
        
        # Loop through the clean text, removing each sentence
        while(len(cleanText) > index):
            # Find the next sentence ending (including ending quotation marks as part of the sentence)
            match = re.search(r'[.!?]((\' ")|\'|")?', cleanText)
            if match:
                # Get the next sentence from the text
                sentence = cleanText[:match.end()]

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
    print("Starting Code")
    
    # Switch this to book
    book = "Acts"
    
    fileName = f"CleanTexts/FullTexts/{book}(NRSV).txt" 
    
    # Create the dictionary of the verses
    verseDict = getVerses(fileName) 
    sentences = getSentences(fileName)


    data = {
        "verses" : verseDict,
        "sentences" : sentences
    }
    
    # The json it is stored as
    with open(f"CleanTexts/{book}Clean.json", 'w') as jsonFile:
        json.dump(data, jsonFile)
    
    print("Finished Code")

    

if __name__ == "__main__":
    main()
