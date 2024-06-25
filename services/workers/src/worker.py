import pika, json
from flask import Flask
from os import chdir, getcwd
from lightphe import LightPHE

app = Flask(__name__)
#TODO: Create unique id for each worker, so the .key will not be overwritten for diferent workers!
ADDITIVE_KEY_PATH = 'src/public_keys/additive_public_key.key'
MULTIPLICATIVE_KEY_PATH = 'src/public_keys/multiplicative_public_key.key'


#TODO: ENDPOINT TO RECEIVE ANSWER FROM THE FRONTEND.
# SHOULD ENCRYPT AND SEND THE SURVEY ANSWERS TO AN ENDPOINT FROM SURVEY HANDLER



def callback(ch, method, properties, body):
    print(f"Received message: {body}")
    channel.stop_consuming()
    
    message = json.loads(body.decode())
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

    
    # TEST: read the public key from the file and test if that works. (THIS SHOULD NOT BE HERE, DELETE THIS TEST)
    #mul_publickey = LightPHE(
    #    algorithm_name = "Exponential-ElGamal", key_file= ADDITIVE_KEY_PATH)
    #add_publickey = LightPHE(
    #    algorithm_name = "Exponential-ElGamal", key_file= MULTIPLICATIVE_KEY_PATH)
    
    
    #TODO: Logic of dealing with surveys here.
    # Send to front end
        
        


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

    app.run()


    



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        exit()

