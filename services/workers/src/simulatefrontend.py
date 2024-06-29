import requests

ENDPOINT_WORKER = "http://localhost:5000/answer"

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
    print("ALGUM ERRO OCORREU NO ENVIO DAS RESPOSTAS.")
