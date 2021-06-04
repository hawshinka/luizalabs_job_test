import flask
import json
from flask import Response
from log_parser import LogParser

app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route('/', defaults={'id': None}, methods=['GET'])
@app.route('/<id>', methods=['GET'])
def game_list(id):
    try:
        log_parser = LogParser()
        result = log_parser.parse_log("challenge/games.log")

        tag = f"game_{id}"
        if id and result.get(tag, None):
            return {tag: result[tag]}

        return Response(json.dumps(result), status=200, mimetype='application/json')
    except FileNotFoundError:
        return Response('{"Error": "Log file not found"}', status=404, mimetype='application/json')

if __name__ == "__main__":
    app.run()
