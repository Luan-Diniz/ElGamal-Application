import pika, json, sys, uuid, requests, pickle, base64
from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from os import chdir, getcwd
from lightphe import LightPHE

try:
    FLASK_PORT = sys.argv[1]
except IndexError:
    print('You can pass a arg to worker.py that will configure the PORT that this backend will run on.')
    FLASK_PORT = 5000   # The default FLASK PORT

UNIQUE_ID = uuid.uuid4()    
ADDITIVE_KEY_PATH = f'src/public_keys/additive_public_key_{UNIQUE_ID}.key'
MULTIPLICATIVE_KEY_PATH = f'src/public_keys/multiplicative_public_key_{UNIQUE_ID}.key'
ENDPOINT_SURVEY_HANDLER = 'http://localhost:4997/answer'
app = Flask(__name__)
CORS(app)


@app.route('/answer_form', methods=['GET','POST'])
def get_answer():
    if request.method == 'GET':
        return jsonify(message)
    
    elif request.method == 'POST':
        answer = request.form.to_dict()
        send_answer_to_survey_handler(answer)
        return jsonify({'status': 'working'})
        

def send_answer_to_survey_handler(answer: dict):
    # Encrypts the answers and send it to SurveyHandler Endpoint.
    encrypted_answers = {}

    additive_publickey = LightPHE(
        algorithm_name = "Exponential-ElGamal", key_file= ADDITIVE_KEY_PATH)
    mulplicative_publickey = LightPHE(
       algorithm_name = "ElGamal", key_file= MULTIPLICATIVE_KEY_PATH)


    for id_question in answer.keys():
        for key in message.keys():
            if str(message[key][0]) == id_question:
                if (message[key][1]) == "average":
                    ciphertext = additive_publickey.encrypt(int(answer[id_question]))
                    encrypted_answers[id_question] = [base64.b64encode(
                        pickle.dumps(ciphertext)).decode('utf-8'), "average"]
                elif (message[key][1] == "multiple choice"):
                    ciphertext = mulplicative_publickey.encrypt(int(answer[id_question]))
                    encrypted_answers[id_question] = [base64.b64encode(
                        pickle.dumps(ciphertext)).decode('utf-8'), "multiple choice"]
                elif (message[key][1] == "text"):
                    encrypted_answers[id_question] = [answer[id_question], "text"]  
                else:
                    assert False, "This else SHOULD'NT be executed!"
                break

    response = requests.post(
        ENDPOINT_SURVEY_HANDLER, json=encrypted_answers 
    )
    if response.status_code == 200:
        data = response.json()
        print("Response data: ", data)
    else:
        print(f"Request failed with status code: {response.status_code}\n")
        print('Exiting program...')
        exit()

def callback(ch, method, properties, body):
    global message

    channel.stop_consuming()
    message = json.loads(body.decode('utf-8'))  # Returns a dict.
    print(f"Received message: {message}")
    # Store received public keys  (Write the raw dictionary)
    # Note that we delete the public keys from the messages,
    # after writing the files, because it will be send to the front end
    # to parse the survey.
    with open(ADDITIVE_KEY_PATH, 'w') as additive_public_key:
        additive_public_key.write(str(message['additive_key']))   
        del message['additive_key']    
    with open(MULTIPLICATIVE_KEY_PATH, 'w') as multiplicative_key:
        multiplicative_key.write(str(message['multiplicative_key']))
        del message['multiplicative_key']


def main():
    global channel

    if getcwd()[-20:] == '/ElGamal-Application':
        chdir(getcwd() + '/services/workers')
    else:
        print('WARNING:')
        print('Make sure you are executing this .py either from the root directory either from the /workers directory!')


    # Based on https://www.rabbitmq.com/tutorials/tutorial-three-python
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='survey', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='survey', queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print('Waiting for messages')
    channel.start_consuming()

    app.run(port=FLASK_PORT)
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        exit()

