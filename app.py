from flask import Flask, request, jsonify, Response
import json
from configuration import ModelConfig, DeployConfig
from datahandler import DataReader
from generator import TextGenerator
from src import make_generation

APP = Flask(__name__)

MODEL_CONFIG = ModelConfig().get_args()
DEPLOY_CONFIG = DeployConfig().get_args()

MODEL = TextGenerator(MODEL_CONFIG, DEPLOY_CONFIG)

@APP.route("/ping")
def ping():
    return "testing"

@APP.route("/gen-text", methods=['POST'])
def gen_text():
    """
    - requrest body:
            {
                "text": "this is a text",
                "num-sequences": 3
            }
    - output
            {
                "result": ["text-1", "text-2", "text-3"]
            }
    """
    data = request.get_json(force=True)
    text, num_sequences = data['text'], data['num-sequences']
    predicts = make_generation(model = MODEL, text = text, num_sequences=num_sequences)    
    result = {'result':predicts}
    return Response(json.dumps(result, ensure_ascii=False), content_type='application/json')


if __name__=="__main__":
    APP.run(debug=False, host='0.0.0.0')
