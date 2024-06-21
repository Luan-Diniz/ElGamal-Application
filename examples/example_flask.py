from flask import Flask, make_response, jsonify, request
 
app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def get_hello():
    return make_response(
        jsonify(
            message='Hello',
        )
    )


app.run()