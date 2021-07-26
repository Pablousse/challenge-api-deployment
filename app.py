import os
from flask import Flask
from flask import request

app = Flask(__name__)

print("Hello world!")

@app.route('/')
def home():
    return 'alive'


@app.route('/predict', methods=['POST'])
def postJsonHandler():
    print(request.is_json)
    content = request.get_json()
    print(content)
    return 'JSON posted'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Threaded option to enable multiple instances for
    # multiple user access support
    # You will also define the host to "0.0.0.0" because localhost will only be reachable from inside de server.
    app.run(host="0.0.0.0", threaded=True, port=port)
