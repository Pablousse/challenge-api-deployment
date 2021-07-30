import os
from typing import Any, Dict

import joblib
from flask import Flask, request
from preprocessing.cleaning_json import preprocess
from flask import render_template

app = Flask(__name__)


@app.route("/")
def home() -> str:
    return "It's alive!"


@app.route("/docs")
def docs() -> str:
    return render_template("docs.html")


@app.route("/predict", methods=["POST"])
def post_predict() -> Dict[str, Any]:
    try:
        prediction = ""
        error = ""
        if not request.is_json:
            raise Exception("The input data were not in a JSON format")
        content = request.get_json()
        df = preprocess(content)
        prediction = clf.predict(df)
    except Exception as e:
        return {"prediction": "", "error:": format(e)}

    if len(prediction) > 1:
        result_json = {"prediction": list(prediction), "error:": error}
    else:
        result_json = {"prediction": str(prediction[0]), "error:": error}

    return result_json


@app.route("/predict", methods=["GET"])
def get_predict() -> str:
    return render_template("data_information.html")


if __name__ == "__main__":
    clf = joblib.load("model/model.pkl")
    port = int(os.environ.get("PORT", 5000))
    app.env = "development"
    app.debug = True
    app.run(host="0.0.0.0", threaded=True, port=port)
