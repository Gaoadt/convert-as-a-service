from flask import Flask, jsonify, request
from src.convert import ConvertService
from threading import Lock


# Creating convert service
convert = ConvertService()
convert_lock = Lock()

# Creating app instance
app = Flask(__name__)


# Convert embedding builder
@app.route("/convert", methods=["POST", "GET"])
def convert_route():
    try:
        dialogues = request.get_json(force=True)
        result = []

        with convert_lock:
            for dialogue in dialogues:
                result.append(convert.encode_context(dialogue).tolist())

        return jsonify({
            "code": 0,
            "message": "ok",
            "data": result
        })

    except Exception as ex:
        return jsonify({
            "code": 1,
            "message": "Error: '{}'".format(ex),
            "data": None
        })
    print(dialogues)
    return jsonify(["ok"])
