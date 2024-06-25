from flask import Flask, jsonify, request, make_response
import pika, json, threading


# Initialization
app = Flask(__name__)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()
channel.queue_declare(queue='survey')

# Variables
result = []  # when use the keyword global in python?


@app.route('/result', methods=['GET'])
def get_result():
    #TODO
    # Should return the results of the survey
    return None

@app.route('/survey', methods=['POST'])
def set_survey():
    survey = request.form
    distribute_survey(survey)

    print(survey) # DELETE THIS PRINT, ONLY FOR DEBUGGING!
    
    return make_response(
        jsonify({'status': 'working'})  # TODO: Make appropriated response.
    )


def distribute_survey(survey):
    message = json.dumps(survey)
    channel.basic_publish(exchange='',
                          routing_key='survey',
                          body=message)


# JUST FOR TESTING RABBITMQ
#survey_example = {'hello' : 'a survey will be here'}
#distribute_survey(survey_example)
#### END OF RABBITMQ TESTING


app.run(port=4997)
connection.close()



