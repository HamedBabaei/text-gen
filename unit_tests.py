import unittest
import numpy as np
import psycopg2
from configuration import ModelConfig, DeployConfig
from generator import TextGenerator
from src import SpacyNER, CommentGeneratorDataset
import keys

model_config = ModelConfig().get_args()
deploy_config = DeployConfig().get_args()
model = TextGenerator(model_config, deploy_config)
ner_model =  SpacyNER(model_name=model_config.spacy_ner_model, ners=model_config.ners)

class TestDataHandlerMethods(unittest.TestCase):

    def test_text_generator(self):
        print("test text generator")
        text = "trump posthumously pardons boxer jack johnson"
        ners = ner_model.extract(text)
        ners = CommentGeneratorDataset.join_ners(ners, randomize=False)
        result = model.generate(text=text, ners=ners, num_return_sequences=3)
        self.assertEqual(len(result), 3)

    def test_deploy_model_config(self):
        print("test deploy config")
        self.assertEqual(deploy_config.inf_model, "main")
        self.assertNotEqual(deploy_config.inf_model, "finetuned")
    
    def test_ner_model(self):
        print("test ner model")
        text = "trump posthumously pardons boxer jack johnson"
        ners = ner_model.extract(text)
        self.assertEqual(len(ners), 1)    
    
    def test_db_connection(self):
        print("test db connection")
        conn = psycopg2.connect(database=keys.DATABASE, 
                                user=keys.USER, 
                                password=keys.PASSWORD, 
                                host=keys.HOST, 
                                port=keys.PORT)
        cursor = conn.cursor()
        cursor.execute("select version()")
        data = cursor.fetchone()
        self.assertNotEqual(len(str(data)), 0)
        conn.close()

if __name__ == '__main__':
    unittest.main()


# add unittest for database as well