#### Eugenio Perez Molphe Montoya ####
#### 03.06.2024 ####
#### This script allows me to use BProm for my files ####
#### The website option, not the software we purchased ####
#### Thing is that we have to many sequences to analyze in the website ####
#### So we decided to use the locally installed software (run_bprom.sh) ####


### Import packages
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

# Functions made by Nico
sys.path.append('/mnt/mnemo5/eugenio/IroN_project/Scripts/IroN-project/Scripts_BlastN/')
from extract_sequence import read_fasta_file

### Now let's define the path to the fasta file and the output directory
fasta = sys.argv[1] # The fasta file with the upstream sequences
outputDir = sys.argv[2] # The output directory where the results will be stored

### Let's extract the sequence
seq = read_fasta_file(fasta)
if len(seq.keys()) == 1:
    sequenceInput = ''
    for key, value in seq.items():
        sequenceInput += '>' + key + "\n" + value + '\n'

        # Let's prepare the output file
        outputFileName = outputDir + '/' + key + '.txt'
else:
    print('There is more than one sequence in the fasta file. Please provide a fasta file with only one sequence.')
    sys.exit()

### Now let's start my Webdriver
service = Service()
options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(service=service, options=options)

### Now let's open the BProm website and get its results

try:
    # Open the target website
    driver.get('http://www.softberry.com/berry.phtml?topic=bprom&group=programs&subgroup=gfindb')

    # Wait until the input field is present and paste the sequence
    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/table/tbody/tr/td/form/p[1]/textarea"))  # Locate the filed to paste the sequence
    )
    input_field.send_keys(sequenceInput)

    # Click the 'Process' button
    process_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/table/tbody/tr/td/form/p[3]/input[1]")  # Click the button to process the sequence
    process_button.click()

    # Wait until the result is present and retrieve the processed text
    result_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body"))  # Get the output text
    )
    processed_text = result_field.text

    # Print or store the processed text
    print(processed_text)

    # And save the results in a file
    with open(outputFileName, 'w') as f:
        f.write(processed_text)

finally:
    # Close the WebDriver
    driver.quit()
