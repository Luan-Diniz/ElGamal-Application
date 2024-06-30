import requests, sys

try:
    FLASK_PORT = sys.argv[1]
except IndexError:
    print('You can pass a arg to simulatefrontend.py that will configure the PORT of the backend endpoint.')
    FLASK_PORT = 5000   # The default FLASK PORT


ENDPOINT_WORKER = f"http://localhost:{FLASK_PORT}/answer_form"

sample_result = {
    "1": 30, 
    "2": "Uma frase qualquer",
    "3": 7
}

if (input("Send survey answer?") not in ["y", "yes"]):
    print('Exiting program...')
    exit()

response = requests.post(
    ENDPOINT_WORKER, sample_result
)

if response.status_code == 200:
        data = response.json()
        print("Response data: ", data)
else:
    print(f"Request failed with status code: {response.status_code}\n")
    exit()