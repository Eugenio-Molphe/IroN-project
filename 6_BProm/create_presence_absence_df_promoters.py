#### Eugenio Perez Molphe Montoya ####
#### 25.06.2024 ####
#### This script takes the results of my BProm run and transform it into a dataframe with absence/presence ####
# The columns of the dataframe are the promoters and the indexes are the genomes' names
# If you want to get the highest scores promoters comment lines 88-96, 193-196 and 206-208, and keep lines 76-85 and 198-200
# If you want to get the closest promoters comment lines 76-85, 193-196 and 203-205, and keep lines 88-96 and 198-200
# If you want all, comment the necessary lines to either get the highest scores or the closest promoters, and keep lines 211-213 and 193-196, while commenting lines 198-200

# First, let's import the libraries
import pandas as pd
import sys
import os

# Let's get the arguments
inputDir = sys.argv[1]
outputDf = sys.argv[2]

# Functions, baby

def get_best_promoters(file, promotersDict):
    """
    This function reads the file and returns a new item for the dictionary: 
    genomeName:promoters for iroN in that genome
    This one filters the promoters to get only one per gene
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
    #### This lines are in case that you want to access the promoters with the highest scores
    #        if oligo[-1] != 'sites':
    #            score = int(oligo[-1])
    #            promoterDict[score] = namePromoter


        # Now, let's get the promoter with the highest score
    #    if promoterDict:
    #        maxScore = max(promoterDict.keys())
    #        bestPromoter = promoterDict[maxScore]
    #        iroNpromoters.append(bestPromoter)
    
    #### This line is in case that you want to access the first promoters
            if oligo[-1] != 'sites':
                try:
                    distance = int(oligo[10])
                except:
                    distance = int(oligo[11])
                promoterDict[distance] = namePromoter
        
        # Now, let's get the promoter with the highest score
        if promoterDict:
            minDistance = min(promoterDict.keys())
            bestPromoter = promoterDict[minDistance]
            iroNpromoters.append(bestPromoter)

    # Finally, let's save the result in the dictionary
    if iroNpromoters:
        promotersDict[genomeName] = iroNpromoters
        
    return promotersDict

def get_promoters(file, promotersDict):
    """
    This function reads the file and returns a new item for the dictionary: 
    genomeName:promoters for iroN in that genome
    This one doesn't filter the promoters, it gets all of them  
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
        for oligo in promoter:
            oligo = oligo.strip().split(" ")
            namePromoter = oligo[0].strip(':') # We've got the name of the promoter
            if oligo[-1] != 'sites':
                iroNpromoters.append(namePromoter)
    # Finally, let's save the result in the dictionary
    if iroNpromoters:
        promotersDict[genomeName] = iroNpromoters
        
    return promotersDict



### Main ###

# Let's create a dictionary that will store the promoters for each genome
allPromotersDict = {}
bestPromotersDict = {}

# Let's iterate over the files in the directory and save the promoters in the dictionary
fileList = os.listdir(inputDir)

# This line gets all the promoters available in the files
for file in fileList:
    get_promoters(inputDir + '/' + file, allPromotersDict)

# This line gets only the promoters with the highest score
for files in fileList:
    get_best_promoters(inputDir + '/' + files, bestPromotersDict)



## Finally, let's create the pandas dataframe

# Extract all the unique promoters from all the genomes to get the columns of the dataframe
allPromoters = set()

for promoterList in allPromotersDict.values():  # For a dataframe with all the promoters
    for promoter in promoterList:
        allPromoters.add(promoter)
allPromoters = sorted(list(allPromoters))

#for promoter in bestPromotersDict.values():  # For a dataframe with only the best promoters
#    allPromoters.update(promoter)
#allPromoters = sorted(list(allPromoters))

# Create the dataframe with the genomes as rows and promoters as columns
df = pd.DataFrame(0, index = allPromotersDict.keys(), columns = allPromoters)

# Let's fill the dataframe, the same applies with allPromotersDict or bestPromotersDict
for genome, promoters in allPromotersDict.items():
    for promoter in promoters:
        df.loc[genome, promoter] = 1

# This extra line add one to the promoters that were judged to be the ones with the highest score
for genome, promoters in bestPromotersDict.items():
    for promoter in promoters:
        df.loc[genome, promoter] += 1

# Save the dataframe
df.to_csv(outputDf, sep = '\t', index=True, header=True)