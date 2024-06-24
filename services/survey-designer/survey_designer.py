import json, requests 
from lightphe import LightPHE

URL_SURVEY_HANDLER = 'http://localhost:4997'
ENDPOINT_SEND_SURVEY = '/survey'
ENDPOINT_GET_RESULT = '/result'

def exit_program():
    print('Exiting program...')
    exit()


# Creating ElGamal keys.
print('Creating keys...')
additive_keys = LightPHE(algorithm_name = "Exponential-ElGamal") # Additively homomorphic
multiplicative_keys = LightPHE(algorithm_name = "ElGamal") # Multiplicative homomorphic
# TODO: Export public keys and send them in the POST request.


# It depends on the CWD of the process.
try:       
    with open('services/survey-designer/survey.json', 'r') as json_file:
        survey = json.load(json_file)
except FileNotFoundError:
    with open('survey.json', 'r') as json_file:
        survey = json.load(json_file)

# For debugging, prints the json in a "fancy" way.
#print(json.dumps(survey, indent=4)) 

if (input('You want to send the survey? y/n\n') not in ['y', 'yes']):
    exit_program()

print('Sending survey...')
try:
    response = requests.post(
            URL_SURVEY_HANDLER + ENDPOINT_SEND_SURVEY, survey)
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



