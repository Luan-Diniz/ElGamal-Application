import pika


def callback(ch, method, properties, body):
    #TODO: Logic of dealing with surveys here.
    print(f"Received message: {body}")

def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='survey')

    channel.basic_consume(queue='survey', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        exit()

