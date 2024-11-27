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
numberBpUpstream = int(sys.argv[3])

# Functions, baby

def get_best_promoters(file, promotersDict, bpUsptream):
    """
    This function reads the file and returns a new item for the dictionary: 
    genomeName:promoters for iroN in that genome
    This one filters the promoters to get only one per gene
    """

    # First, let's open the file

    with open(file, 'r') as f:
        # Let's get the genome name
        fileLines = f.readlines()

    # Let' obtain the length of the sequence and then the maximum distance upstream in which were found the promoters
    seqLength = int(fileLines[1].split(" ")[-1].strip())

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
    genomeName = fileLines[0].split('.')[1].strip('>')

    # Now, let's get the list of the most possible promoters per each identified promoters
    # In other words, the promoters influencing iroN
    iroNpromoters = []

    for promoter in promoters:
        # I'll create a dictionary to store the information: keys as scores and values as the name of the promoter
        for oligo in promoter:
            oligo = oligo.strip().split(" ")
            namePromoter = oligo[0].strip(':') # We've got the name of the promoter
    
    #### Let's get the promoters that are closer to the iroN gene
            if oligo[-1] != 'sites':
                try:
                    distance = int(oligo[10])
                except:
                    try:
                        distance = int(oligo[11])
                    except:
                        try:
                            distance = int(oligo[9])
                        except:
                            distance = int(oligo[8])

    # Now, I'm going to include all the promoters that are inside the range
                distance = seqLength - distance
                if distance <= bpUsptream:
                    iroNpromoters.append(namePromoter)

    # Finally, let's save the result in the dictionary
    if iroNpromoters:
        promotersDict[genomeName] = iroNpromoters
        
    return promotersDict





### Main ###

# Let's create a dictionary that will store the promoters for each genome
promotersDict = {}

# Let's iterate over the files in the directory and save the promoters in the dictionary
fileList = os.listdir(inputDir)

# This line gets only the promoters with the highest score
for files in fileList:
    get_best_promoters(inputDir + '/' + files, promotersDict, numberBpUpstream)



## Finally, let's create the pandas dataframe

# Extract all the unique promoters from all the genomes to get the columns of the dataframe
allPromoters = set()

for promoterList in promotersDict.values():  # For a dataframe with all the promoters
    for promoter in promoterList:
        allPromoters.add(promoter)
allPromoters = sorted(list(allPromoters))

# Create the dataframe with the genomes as rows and promoters as columns
df = pd.DataFrame(0, index = promotersDict.keys(), columns = allPromoters)

# Let's fill the dataframe, the same applies with allPromotersDict or bestPromotersDict
for genome, promoters in promotersDict.items():
    for promoter in promoters:
        df.loc[genome, promoter] = 1

# Save the dataframe
df.to_csv(outputDf, sep = '\t', index=True, header=True)