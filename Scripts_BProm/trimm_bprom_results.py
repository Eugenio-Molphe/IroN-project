#### Eugenio Perez Molphe Montoya ####
#### 27.06.2024 ####
#### So, BProm couldn't detect the promoter in some sequences, I'll remove them ####

# Import packages and functions
import os
import sys

# Arguments
dir = sys.argv[1] # The directory with the BProm results
outputReport = sys.argv[2] # The output report, where I report which sequences were removed

# Functions
def read_results_remove_if_empty(file, listRemovedFiles):
    '''
    This function takes a file and checks if it has promoters, if not, it gets removed and reported as empty
    by including it into a list.
    '''
    with open(file) as f:
        lines = f.readlines()
    if len(lines) <= 4: ### Check the number of lines that a failed file has <-----------------
        basename = os.path.basename(file)
        listRemovedFiles.append(basename)
        os.remove(file)
    return listRemovedFiles


### Main ###
# Get the files
files = [f"{dir}/{f}" for f in os.listdir(dir)]

# Check if the files are empty
removedFiles = []
for file in files:
    removedFiles = read_results_remove_if_empty(file, removedFiles)

# Report the removed files
with open(outputReport, "w") as f:
    f.write("The following files were removed because BProm couldn't detect the promoter:\n")
    for file in removedFiles:
        f.write(f"{file}\n")
print("Done :D")