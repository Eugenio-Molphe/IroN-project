#### Eugenio Perez Molphe Montoya ####
#### 25.06.2024 ####
#### This script takes the results of my BProm run and transform it into a dataframe with absence/presence ####
# The columns of the dataframe are the promoters and the indexes are the genomes' names

# First, let's import the libraries
import pandas as pd
import sys
import os

# Let's get the arguments
inputDir = sys.argv[1]
outputDf = sys.argv[2]

# Functions, baby

def get_promoters(file, promotersDict):
    """
    This function reads the file and returns a new item for the dictionary: 
    genomeName:promoters for iroN in that genome
    """

    # First, let's open the file

    with open(file, 'r') as f:
        # Let's get the genome name
        fileLines = f.readlines()

    # This file contains an identified position and the promotor that may be there
    # So, let's get a list with the promoters

    # First, I'll filter the lines before the first promoter
    startProcessing = False
    filteredLines = []
    for line in fileLines:
        if line.startswith("For promoter"):
            startProcessing = True
        if startProcessing:
            filteredLines.append(line)

    # Then, I'll get the promoters
    promoters = []
    currentPromoter = []
    # Iterate over the lines and dump the possible promoters into the currentPromoter list
    for line in filteredLines:
        if line.startswith("For promoter"):
            promoters.append(currentPromoter)
            currentPromoter = []
            continue
        # Skip adding the "For promoter" line to the current section, we only care about the identified promoters
        currentPromoter.append(line)

    # Don't forget to add the last section if it exists
    if currentPromoter:
        promoters.append(currentPromoter)
    
    # The first one is the name of the genome, we don't need it in the list per se
    genomeName = fileLines[0].split(".")[0].strip('>')

    # Now, let's get the list of the most possible promoters per each identified promoters
    # In other words, the promoters influencing iroN
    iroNpromoters = []

    for promoter in promoters:
        # I'll create a dictionary to store the information: keys as scores and values as the name of the promoter
        promoterDict = {}
        for oligo in promoter:
            oligo = oligo.strip().split(" ")
            namePromoter = oligo[0].strip(':') # We've got the name of the promoter
            if oligo[-1] != 'sites':
                score = int(oligo[-1])
                promoterDict[score] = namePromoter

        # Now, let's get the promoter with the highest score
        if promoterDict:
            maxScore = max(promoterDict.keys())
            bestPromoter = promoterDict[maxScore]
            iroNpromoters.append(bestPromoter)

    # Finally, let's save the result in the dictionary
    if iroNpromoters:
        promotersDict[genomeName] = iroNpromoters
        
    return promotersDict



### Main ###

# Let's create a dictionary that will store the promoters for each genome
promotersDict = {}

# Let's iterate over the files in the directory and save the promoters in the dictionary
fileList = os.listdir(inputDir)

for file in fileList:
    get_promoters(inputDir + '/' + file, promotersDict)

## Finally, let's create the pandas dataframe

# Extract all the unique promoters from all the genomes to get the columns of the dataframe
allPromoters = set()
for promoter in promotersDict.values():
    allPromoters.update(promoter)
allPromoters = sorted(list(allPromoters))

# Create the dataframe with the genomes as rows and promoters as columns
df = pd.DataFrame(0, index = promotersDict.keys(), columns = allPromoters)

# Let's fill the dataframe
for genome, promoters in promotersDict.items():
    for promoter in promoters:
        df.loc[genome, promoter] = 1

# Save the dataframe
df.to_csv(outputDf, sep = '\t', index=True, header=True)