from flask import Flask, request, jsonify, Response
import json
from configuration import ModelConfig, DeployConfig
from datahandler import DataReader
from generator import TextGenerator
from src import (make_generation,
                 CommentGeneratorDataset,
                 SpacyNER,
                 PostgreSQLDatabase)
import keys


APP = Flask(__name__)

MODEL_CONFIG = ModelConfig().get_args()
DEPLOY_CONFIG = DeployConfig().get_args()

DATABASE = PostgreSQLDatabase(database=keys.DATABASE,
                              user=keys.USER, 
                              password=keys.PASSWORD, 
                              host=keys.HOST, 
                              port=keys.PORT)

GENERATOR_MODEL = TextGenerator(MODEL_CONFIG, DEPLOY_CONFIG)
NER_MODEL = SpacyNER(model_name=MODEL_CONFIG.spacy_ner_model, ners=MODEL_CONFIG.ners)

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
    predicts = make_generation(generator_model=GENERATOR_MODEL, 
                               ner_model=NER_MODEL, 
                               dataset=CommentGeneratorDataset,
                               input_text=text, 
                               database=DATABASE, 
                               num_sequences=num_sequences)
    result = {'result':predicts}
    return Response(json.dumps(result, ensure_ascii=False), content_type='application/json')

if __name__=="__main__":
    APP.run(debug=False, host='0.0.0.0')
