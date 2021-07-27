from preprocessing.cleaning_json import preprocess
import os
from flask import Flask
from flask import request
import joblib

app = Flask(__name__)


@app.route('/')
def home() -> str:
    return 'alive'


@app.route('/predict', methods=['POST'])
def postJsonHandler() -> str:
    print(request.is_json)
    try:
        content = request.get_json()
        df = preprocess(content)
    except ValueError as error:
        return "ValueError: " + format(error)
    except Exception as e:
        return "Exception: " + format(e)
    prediction = clf.predict(df)
    print(prediction[0])
    # return 'Json posted'
    return str(prediction[0])


if __name__ == '__main__':
    clf = joblib.load('model.pkl')
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host="0.0.0.0", threaded=True, port=port)
