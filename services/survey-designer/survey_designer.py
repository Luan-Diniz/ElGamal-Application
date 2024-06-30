import json, requests, base64, pickle
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


if (input('You want to send the survey? y/n\n').lower() not in ['y', 'yes']):
    exit_program()

print('Sending survey...')
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


if (input('You want the results? y/n\n').lower() not in ['y', 'yes']):
    exit_program()

response = requests.get(
    URL_SURVEY_HANDLER + ENDPOINT_GET_RESULT
)
if response.status_code == 200:
    data = response.json()
    print("Response data: ", data)
else:
    print(f"Request failed with status code: {response.status_code}\n")
    exit_program()

number_answers = data['number answers']
del data['number answers']

# Deserialize ciphertexts.
for id_question in data.keys():
    if type(data[id_question]) != list:
        data[id_question] = pickle.loads(base64.b64decode(data[id_question]))

# Decrypt ciphertext and show results.
print()
print("----------SURVEY RESULTS----------")
for id_question in data.keys():
    for question in survey.keys():
        if survey[question][0] == int(id_question):
            if survey[question][1] == "average":
                answer = additive_keys.decrypt(data[id_question])/number_answers

                print(question)
                print(f"Average answer: {answer}")
                print()

            elif survey[question][1] == "text":
                print(question)
                print("Answers: ")
                for answer in data[id_question]:
                    print(f"\t{answer}")

            elif survey[question][1] == "multiple choice":
                number_to_be_factored = multiplicative_keys.decrypt(data[id_question])
                #TODO: Factorize the number, count its primes factors,
                # and relate them with the prime numbers described in the 
                # multiple-choice question alternatives of a survey.
                
            else:
                assert False, "This else SHOULD'NT be executed!"
print("----------END OF SURVEY----------")