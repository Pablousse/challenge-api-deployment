import os

import joblib
from flask import Flask, request
from preprocessing.cleaning_json import preprocess
from flask import render_template

app = Flask(__name__)


@app.route("/")
def home() -> str:
    return "alive"


@app.route("/docs")
def index() -> str:
    return render_template("docs.html")


@app.route("/predict", methods=["POST"])
def postJsonHandler() -> str:
    try:
        if not request.is_json:
            raise ValueError("The input datas were not in a JSON format")
        content = request.get_json()
        df = preprocess(content)
    except ValueError as error:
        return "ValueError: " + format(error)
    except Exception as e:
        return "Exception: " + format(e)
    prediction = clf.predict(df)

    return str(prediction)


if __name__ == "__main__":
    clf = joblib.load("model.pkl")
    port = int(os.environ.get("PORT", 5000))
    app.debug = True
    app.run(host="0.0.0.0", threaded=True, port=port)
