import torch
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path




def main():
    print("Starting Code")
    
    # Load the model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    embeddings = []
    sentences = []
    
    book1 = "Acts"
    book2 = "Luke"

    
    # Get the embeddings and stuff from first book
    with open(f"Embeddings/{book1}Verses.json", 'r') as jsonFile:
        data = json.load(jsonFile)
        bookLength1 = len(data["embeddings"])
        print(bookLength1)
        embeddings += data["embeddings"]
        sentences += data["text"]
    
    # Get the embeddings and stuff from second book
    # I just concatenate the vectors since the similarity function takes a single vector input    
    with open(f"Embeddings/{book2}Verses.json", 'r') as jsonFile:
        data = json.load(jsonFile)
        bookLength2 = len(data["embeddings"])
        print(bookLength2)
        embeddings += data["embeddings"]
        sentences += data["text"]
    
    # Use SBERT's built in similarity function
    # This creates a matrix  
    similarities = model.similarity(embeddings, embeddings)
    #print(similarities)
    

    # Getting the verses (comment out if you are just doing sentences)
    with open(f"CleanTexts/{book1}Clean.json", 'r') as jsonFile:
        book1Dict = json.load(jsonFile)["verses"]
    with open(f"CleanTexts/{book2}Clean.json", 'r') as jsonFile:
        book2Dict = json.load(jsonFile)["verses"]
    

    # Go through the section of the matrix that is comparing the two books
    for i in range(bookLength1):
        for j in range(bookLength1, bookLength1 + bookLength2):
            if similarities[i][j] > 0.85: # This value can be changed to filter different similarity levels
                print(f"i:{i}\tj:{j}\tval:{similarities[i][j]}\n")
                print(f"{book1} {book1Dict[sentences[i]]} - {sentences[i]}\n\n{book2} {book2Dict[sentences[j]]} - {sentences[j]}\n\n")

                
    # # Creates the heatmap graph thing, which can be kind of cool, but not needed so it's commented out
    # im = sns.heatmap(similarities, cmap="YlGnBu")
    # plt.savefig('testEmbeddings', dpi=1200, bbox_inches='tight')
    

    


if __name__ == "__main__":
    main()