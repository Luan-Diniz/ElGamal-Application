# ElGamal-Application

Setting up the virtual environment:

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate      # To exit the virtual environment

How to execute:
    docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management