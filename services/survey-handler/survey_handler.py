import pika, json, base64, pickle
from flask import Flask, jsonify, request, make_response
from random import sample


# Initialization
app = Flask(__name__)

# https://www.rabbitmq.com/tutorials/tutorial-three-python
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()
channel.exchange_declare(exchange='survey', exchange_type='fanout')

# Variables
result = {}
number_answers = 0


@app.route('/result', methods=['GET'])
def get_result():
    # Should return the results of the survey.
    # Should serialize and convert to base64 all Ciphertexts
    # Should shuffle all answers with [str].
    # Should clean the result variable.
    
    serialized_results = {}
    for key in result.keys():
        if type(result[key]) == list:
            serialized_results[key] = sample(
                result[key], k = len(result[key]))  # Shuffles
        else:
            serialized_results[key] = base64.b64encode(
                        pickle.dumps(result[key])).decode('utf-8')
    result.clear()
    serialized_results['number answers'] = number_answers
    return make_response(
        jsonify(serialized_results)
    )

# This endpoint receives the encrypted answers from the workers.
@app.route('/answer', methods=['POST'])
def receive_answer():
    global number_answers
    answer = request.get_json()
    print(answer)

    for key in answer.keys():
        if answer[key][1] == "text":
            try:
                result[key].append(answer[key][0])
            except KeyError:
                result[key] = [answer[key][0]]
        else: 
            ciphertext = answer[key][0]
            ciphertext = pickle.loads(base64.b64decode(ciphertext))

            if answer[key][1] == "average":
                try:
                    result[key] += ciphertext
                except KeyError:
                    result[key] = ciphertext
            elif answer[key][1] == "multiple choice":
                try:
                    result[key] *= ciphertext
                except KeyError:
                    result[key] = ciphertext
            else:
                assert False, "This else SHOULD'NT be executed!"
    number_answers += 1

    return make_response(
        jsonify({'status': 'working'})  
    )    

@app.route('/survey', methods=['POST'])
def set_survey():
    survey = request.get_json()
    distribute_survey(survey)

    print(survey) # DELETE THIS PRINT, ONLY FOR DEBUGGING!

    return make_response(
        jsonify({'status': 'working'})  
    )


def distribute_survey(survey):
    message = json.dumps(survey)
    channel.basic_publish(exchange='survey',
                          routing_key='',
                          body=message) 


app.run(port=4997)
connection.close()



