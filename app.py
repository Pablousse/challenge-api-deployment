import os
from flask import Flask
from flask import request
import joblib

app = Flask(__name__)

@app.route('/')
def home() -> str:
    return 'alive'


@app.route('/predict', methods=['POST'])
def postJsonHandler():
    print(request.is_json)
    content = request.get_json()
    print(content)
    # prediction = clf.predict(query)
    return 'JSON posted'


if __name__ == '__main__':
    clf = joblib.load('model.pkl')
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", threaded=True, port=port)
