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
    
    # Get the embeddings and stuff from Matthew (change this to your json)
    with open("MatthewEmbedding.json", 'r') as jsonFile:
        data = json.load(jsonFile)
        matt = len(data["embeddings"])
        print(matt)
        embeddings += data["embeddings"]
        sentences += data["sentences"]
     
    # Get the embeddings and stuff from Mark (change this to your json)
    # I just concatenate the vectors since the similarity function takes a single vector input    
    with open("MarkEmbedding.json", 'r') as jsonFile:
        data = json.load(jsonFile)
        mark = len(data["embeddings"])
        print(mark)
        embeddings += data["embeddings"]
        sentences += data["sentences"]
    
    # Use SBERT's built in similarity function
    # This creates a matrix  
    similarities = model.similarity(embeddings, embeddings)
    #print(similarities)
    
    # Go through the section of the matrix that is matthew compared to mark
    for i in range(matt):
        for j in range(matt, matt + mark):
            if similarities[i][j] > 0.85: # This value can be changed to filter different similarity levels
                print(f"i:{i}\tj:{j}\tval:{similarities[i][j]}\n")
                print(f"{sentences[i]}\n\n{sentences[j]}\n\n")

                
    # # Creates the heatmap graph thing, which can be kind of cool, but not needed so it's commented out
    # im = sns.heatmap(similarities, cmap="YlGnBu")
    # plt.savefig('testEmbeddings', dpi=1200, bbox_inches='tight')
    

    


if __name__ == "__main__":
    main()