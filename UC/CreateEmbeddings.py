import torch
from sentence_transformers import SentenceTransformer
import numpy as np
import json



def main():
    # I put this since the first time you run it, it needs to load the model which takes a while, so I know it's actually started
    print("Starting Code")
    

    # Open the data from the cleaned text
    verses = []
    sentences = []

    book = "Acts"
    textType = "Verses"     # Verses or Sentences (capitalized)
    #textType = "Sentences"

    with open(f"CleanTexts/{book}Clean.json") as jsonFile:
        data = json.load(jsonFile)
        
        verseDict = data["verses"]
        for v in verseDict:
            verses.append(v)

        sentences = data["sentences"]
    
    if(textType == "Verses"):
        text = verses
    else:
        text = sentences
    
    
    # Load the model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # Create the embeddings (this is running the SBERT model)
    embeddings = model.encode(text)
    
    # I then store the text and embeddings to a json so they can be used later
    data = {
        "text" : text,
        "embeddings" : embeddings.tolist()
    }
    # Change this to be what you actually want to save it as (for example, if it's for Mark, name it that so they don't overwrite eachother)
    with open(f"Embeddings/{book}{textType}.json", 'w') as jsonFile:
        json.dump(data, jsonFile)
    
    # The embeddings have been made and stored
    print("Finished Code")

    

if __name__ == "__main__":
    main()