import json, requests
from os import getcwd, chdir 
from lightphe import LightPHE


URL_SURVEY_HANDLER = 'http://localhost:4997'
ENDPOINT_SEND_SURVEY = '/survey'
ENDPOINT_GET_RESULT = '/result'
# Relative to /survey-designer directory.
ADDITIVE_KEY_PATH = 'public_keys/additive_public_key.key'
MULTIPLICATIVE_KEY_PATH = 'public_keys/multiplicative_public_key.key'

def exit_program():
    print('Exiting program...')
    exit()

if getcwd()[-20:] == '/ElGamal-Application':
    chdir(getcwd() + '/services/survey-designer')
else:
    print('WARNING:')
    print('Make sure you are executing this .py either from the root directory either from the /survey-designer directory!')


# Creating ElGamal keys.
print('Creating keys...')
additive_keys = LightPHE(algorithm_name = 'Exponential-ElGamal') # Additively homomorphic
multiplicative_keys = LightPHE(algorithm_name = 'ElGamal') # Multiplicative homomorphic

# Export public keys and send them in the POST request. (It depends on the CWD of the process.)
additive_keys.export_keys(ADDITIVE_KEY_PATH, True)
multiplicative_keys.export_keys(MULTIPLICATIVE_KEY_PATH, True)


# It depends on the CWD of the process.
with open('survey.json', 'r') as json_file:
    survey = json.load(json_file)
    with open(ADDITIVE_KEY_PATH, 'r') as additive_key_file:
        survey['additive_key'] = additive_key_file.read()
    with open(MULTIPLICATIVE_KEY_PATH, 'r') as multiplicative_key_file:
        survey['multiplicative_key'] = multiplicative_key_file.read()

# For debugging, prints the json in a "fancy" way.
#print(json.dumps(survey, indent=4)) 

if (input('You want to send the survey? y/n\n') not in ['y', 'yes']):
    exit_program()

print('Sending survey...')
print(survey)
try:
    response = requests.post(
            URL_SURVEY_HANDLER + ENDPOINT_SEND_SURVEY, json=survey)
    if response.status_code == 200:
        data = response.json()
        print("Response data: ", data)
    else:
        print(f"Request failed with status code: {response.status_code}\n")
        exit_program()

except requests.exceptions.RequestException as e:
    print(f'An error occurred: {e}\n')
    exit_program()



print('Want the result?')
'''
TODO:
    Request asking for results.
    Decrypt and parse the data received.
    Show the results.
'''



